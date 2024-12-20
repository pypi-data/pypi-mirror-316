"""Core functionality for sequence processing and analysis."""

from Bio import SeqIO
from Bio.Seq import Seq
from collections import defaultdict
import numpy as np
from itertools import combinations
import edlib
from pathlib import Path
import gzip
import matplotlib.pyplot as plt
from Bio import Align
from kneed import KneeLocator
from Bio import AlignIO
from Bio.Align import MultipleSeqAlignment
from Bio.SeqRecord import SeqRecord
import random
import subprocess
import tempfile
import os
import click
import multiprocessing as mp
from functools import partial
from itertools import islice
import math
import concurrent.futures
from queue import Queue
from collections import Counter

# Global variables for multiprocessing
CPUS = max(1, mp.cpu_count() - 2)  # Leave 2 CPU free for system
CHUNK_SIZE = 100000  # Configurable chunk size for batch processing


def chunk_list(lst, n):
    """Split a list into n chunks of approximately equal size."""
    k, m = divmod(len(lst), n)
    return [lst[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n)]

def align_sequence_chunk(chunk_data):
    """Process a chunk of sequences for clustering."""
    sequences, rep_seqs, max_edit_distance, aligner = chunk_data
    results = defaultdict(int)
    
    for seq, count in sequences:
        assigned = False
        for rep_seq in rep_seqs:
            if abs(len(seq) - len(rep_seq)) <= max_edit_distance:
                alignment = aligner.align(seq, rep_seq)[0]
                perfect_score = len(seq)
                edit_dist = int((perfect_score - alignment.score) / 2)
                
                if edit_dist <= max_edit_distance:
                    results[rep_seq] += count
                    assigned = True
                    break
        
        if not assigned:
            results[seq] = count
    
    return dict(results)

def cluster_sequences(sorted_seqs, max_edit_distance):
    """Cluster sequences using advanced multi-stage filtering approach."""
    if max_edit_distance <= 0:
        return dict(sorted_seqs)
    
    click.echo("Filtering similar sequences using advanced multi-stage approach...")
    
    # Stage 0: Initial abundance-based filtering
    min_count_threshold = max(2, len(sorted_seqs) // 10000)  # Adaptive threshold
    initial_seqs = [(seq, count) for seq, count in sorted_seqs if count >= min_count_threshold]
    
    if len(initial_seqs) < len(sorted_seqs):
        click.echo(f"Filtered out {len(sorted_seqs) - len(initial_seqs)} low-abundance sequences")
    
    # Stage 1: Group by length and multiple prefixes/suffixes
    click.echo("Stage 1: Advanced sequence grouping...")
    sequence_groups = defaultdict(list)
    
    for seq, count in initial_seqs:
        # Create composite key using multiple sequence features
        length = len(seq)
        prefix = seq[:4]
        suffix = seq[-4:]
        gc_content = calculate_gc_content(seq[:10])  # GC content of first 10 bases
        
        # Group key combines multiple sequence features
        group_key = f"{length}_{prefix}_{gc_content}"
        sequence_groups[group_key].append((seq, count))
    
    # Stage 2: Enhanced pre-filtering within groups
    click.echo("Stage 2: Enhanced pre-filtering...")
    intermediate_results = defaultdict(int)
    processed_seqs = set()
    
    # Pre-compute minimizers for all sequences
    minimizers_dict = {seq: compute_minimizers(seq) for seq, _ in initial_seqs}
    
    with click.progressbar(sequence_groups.items(), label='Processing sequence groups') as group_items:
        for group_key, group_seqs in group_items:
            if len(group_seqs) == 1:
                seq, count = group_seqs[0]
                intermediate_results[seq] = count
                processed_seqs.add(seq)
                continue
            
            # Sort by count (descending) and length
            group_seqs.sort(key=lambda x: (-x[1], len(x[0])))
            
            # Process sequences within group using sliding window
            window_size = 1000  # Adjustable window size
            for i in range(0, len(group_seqs), window_size):
                window_seqs = group_seqs[i:i + window_size]
                
                for j, (seq, count) in enumerate(window_seqs):
                    if seq in processed_seqs:
                        continue
                    
                    current_cluster = [(seq, count)]
                    processed_seqs.add(seq)
                    
                    # Use minimizers for quick similarity estimation
                    seq_minimizers = minimizers_dict[seq]
                    
                    for comp_seq, comp_count in window_seqs[j+1:]:
                        if comp_seq in processed_seqs:
                            continue
                        
                        # Multi-level filtering
                        if abs(len(seq) - len(comp_seq)) > max_edit_distance:
                            continue
                        
                        # Quick minimizer-based similarity check
                        if minimizer_similarity(seq_minimizers, minimizers_dict[comp_seq]):
                            # Secondary k-mer similarity check
                            if quick_similarity_check(seq, comp_seq):
                                current_cluster.append((comp_seq, comp_count))
                                processed_seqs.add(comp_seq)
                    
                    total_count = sum(c for _, c in current_cluster)
                    intermediate_results[seq] = total_count
    
    # Stage 3: Optimized final clustering
    click.echo("Stage 3: Optimized final clustering...")
    filtered_counts = {}
    sequences_to_process = list(intermediate_results.items())
    
    # Optimize chunk size based on sequence length
    avg_seq_len = sum(len(seq) for seq, _ in sequences_to_process) / len(sequences_to_process)
    optimal_chunk_size = max(100, int(1000000 / avg_seq_len))  # Adjust chunk size based on sequence length
    
    chunks = chunk_list(sequences_to_process, min(CPUS * 2, len(sequences_to_process)))
    
    with click.progressbar(length=len(sequences_to_process), label='Final clustering') as bar:
        with mp.Pool(CPUS) as pool:
            chunk_args = [(chunk, sequences_to_process, max_edit_distance) for chunk in chunks]
            for result in pool.imap_unordered(cluster_sequences_chunk, chunk_args):
                filtered_counts.update(result)
                bar.update(len(result))
    
    return filtered_counts

def calculate_gc_content(seq):
    """Calculate GC content bucket (0-10)."""
    gc = sum(1 for base in seq if base in 'GC')
    return int((gc / len(seq)) * 10)

def compute_minimizers(seq, w=10, k=5):
    """Compute sequence minimizers for quick comparison."""
    minimizers = set()
    for i in range(len(seq) - w + 1):
        window = seq[i:i+w]
        min_kmer = min(window[j:j+k] for j in range(w-k+1))
        minimizers.add(min_kmer)
    return minimizers

def minimizer_similarity(min1, min2):
    """Quick check if two sequences might be similar based on minimizers."""
    return len(min1 & min2) / len(min1 | min2) >= 0.3

def quick_similarity_check(seq1, seq2, k=7):
    """Enhanced quick k-mer based similarity check."""
    # Use rolling hash for faster k-mer generation
    kmers1 = rolling_hash_kmers(seq1, k)
    kmers2 = rolling_hash_kmers(seq2, k)
    
    # Calculate Jaccard similarity
    intersection = len(kmers1 & kmers2)
    union = len(kmers1 | kmers2)
    similarity = intersection / union if union > 0 else 0
    
    return similarity >= 0.8

def rolling_hash_kmers(seq, k):
    """Generate k-mers using rolling hash for better performance."""
    kmers = set()
    if len(seq) < k:
        return kmers
    
    # Initial hash
    current_hash = hash(seq[:k])
    kmers.add(seq[:k])
    
    # Rolling hash for remaining k-mers
    for i in range(len(seq) - k):
        # Update hash by removing first character and adding next character
        current_hash = hash(seq[i+1:i+k+1])
        kmers.add(seq[i+1:i+k+1])
    
    return kmers

def cluster_sequences_chunk(args):
    """Process a chunk of sequences for clustering."""
    sequences, comparable_seqs, max_edit_distance = args
    filtered_counts = {}
    
    # Pre-compute k-mers for all sequences in the chunk
    kmers_dict = {seq: get_kmers(seq) for seq, _ in sequences}
    comparable_kmers = {seq: get_kmers(seq) for seq, _ in comparable_seqs if seq not in kmers_dict}
    kmers_dict.update(comparable_kmers)
    
    for seq, count in sequences:
        # Skip if sequence is already processed
        if seq in filtered_counts:
            continue
            
        # Get k-mers for current sequence
        seq_kmers = kmers_dict[seq]
        assigned = False
        
        # First try exact matches
        for comp_seq, comp_count in comparable_seqs:
            if comp_seq in filtered_counts and seq == comp_seq:
                filtered_counts[comp_seq] += count
                assigned = True
                break
        
        if not assigned:
            for comp_seq, comp_count in comparable_seqs:
                if comp_seq in filtered_counts:
                    # Quick length check
                    if abs(len(seq) - len(comp_seq)) > max_edit_distance:
                        continue
                    
                    # Use pre-computed k-mers
                    comp_kmers = kmers_dict[comp_seq]
                    
                    # Calculate Jaccard similarity
                    intersection = len(seq_kmers & comp_kmers)
                    union = len(seq_kmers | comp_kmers)
                    similarity = intersection / union if union > 0 else 0
                    
                    if similarity >= 0.9:
                        filtered_counts[comp_seq] += count
                        assigned = True
                        break
        
        if not assigned:
            filtered_counts[seq] = count
    
    return filtered_counts

def get_kmers(seq, k=7):
    """Get k-mers from a sequence."""
    return set(seq[i:i+k] for i in range(len(seq)-k+1))

def check_probe_binding_chunk(sequences, reference_seqs, max_distance):
    """Process a chunk of sequences for probe binding.
    
    Args:
        sequences: List of sequences to check
        reference_seqs: Dictionary of reference sequences
        max_distance: Maximum edit distance allowed
    """
    results = []
    
    for seq in sequences:
        for ref_id, ref_seq in reference_seqs.items():
            if check_probe_binding(seq, ref_seq, max_distance):
                results.append((seq, ref_id))
    
    return results

def write_binding_results(sequences, reference_seqs, max_distance, output_prefix):
    """Write probe binding results using parallel processing."""
    output_file = f"{output_prefix}_binding_sites.tsv"
    total_bindings = 0
    
    # Split sequences into chunks for parallel processing
    chunks = [sequences[i:i+CHUNK_SIZE] for i in range(0, len(sequences), CHUNK_SIZE)]
    
    with open(output_file, 'w') as f:
        f.write("Sequence\tReference\tBinding_Sites\n")
        
        with click.progressbar(length=len(sequences), label='Checking probe binding') as bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=CPUS) as executor:
                # Create a partial function with the fixed arguments
                chunk_fn = partial(check_probe_binding_chunk, reference_seqs=reference_seqs, max_distance=max_distance)
                
                futures = [
                    executor.submit(chunk_fn, chunk)
                    for chunk in chunks
                ]
                
                for future in concurrent.futures.as_completed(futures):
                    chunk_results = future.result()
                    for seq, ref_id in chunk_results:
                        f.write(f"{seq}\t{ref_id}\tTrue\n")
                        total_bindings += 1
                    bar.update(len(chunk_results))
    
    click.echo(f"Found {click.style(str(total_bindings), fg='green')} binding sites")

def estimate_records(file_path, sample_size=100000):
    """Estimate total records using file size and sampling."""
    opener = gzip.open if file_path.endswith('.gz') else open
    file_size = os.path.getsize(file_path)
    
    with opener(file_path, 'rt') as handle:
        # Read a sample of the file
        sample = handle.read(sample_size)
        if not sample:
            return 0
        
        # Count complete FASTQ records (must have 4 lines)
        record_count = 0
        lines = sample.count('\n')
        complete_records = lines // 4
        
        if file_path.endswith('.gz'):
            # For gzipped files, use compressed size ratio
            sample_compressed = gzip.compress(sample.encode())
            compression_ratio = len(sample_compressed) / file_size
            estimated_records = int(complete_records / compression_ratio)
        else:
            # For uncompressed files
            bytes_per_record = len(sample.encode()) / complete_records
            estimated_records = int(file_size / bytes_per_record)
        
        # Add 10% buffer to ensure we don't underestimate
        return int(estimated_records * 1.1)

def read_fastq_files(file_paths, subsample=None, min_length=None, max_length=None, sampling_method='reservoir'):
    """Read and process FASTQ files."""
    seq_counts = Counter()
    total_sequences = 0
    CHUNK_SIZE = 100000  # Process 100k sequences at a time
    
    def get_file_size(file_path):
        """Get file size in bytes."""
        return os.path.getsize(file_path)
    
    def format_size(bytes):
        """Convert bytes to human readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}TB"
    
    def process_file(file_path):
        file_counter = Counter()
        processed_seqs = 0
        sequences_chunk = []
        
        # Determine file opener
        opener = gzip.open if file_path.endswith('.gz') else open
        
        # First pass to count sequences
        with opener(file_path, 'rt') as f:
            total_seqs = sum(1 for _ in f) // 4
        
        with click.progressbar(length=total_seqs, 
                             label=f'Reading {os.path.basename(file_path)}',
                             show_percent=True,
                             item_show_func=lambda x: f"{x:,} sequences" if x is not None else '') as bar:
            with opener(file_path, 'rt') as f:
                # Read file in chunks of 4 lines (FASTQ format)
                while True:
                    # Read chunk of FASTQ entries
                    chunk = [f.readline().strip() for _ in range(4 * CHUNK_SIZE)]
                    if not chunk[0]:  # End of file
                        break
                    
                    # Process sequences in chunk
                    for i in range(0, len(chunk), 4):
                        if not chunk[i]:  # Partial chunk at end of file
                            break
                        
                        seq = chunk[i+1]  # Sequence is second line
                        
                        # Apply length filters
                        if min_length and len(seq) < min_length:
                            continue
                        if max_length and len(seq) > max_length:
                            continue
                            
                        sequences_chunk.append(seq)
                        processed_seqs += 1
                        
                        if len(sequences_chunk) >= CHUNK_SIZE:
                            file_counter.update(sequences_chunk)
                            sequences_chunk = []
                    
                    # Update progress every chunk
                    bar.update(CHUNK_SIZE)
        
        # Process any remaining sequences
        if sequences_chunk:
            file_counter.update(sequences_chunk)
            
        return file_counter, processed_seqs

    # Process each file
    total_size = sum(get_file_size(f) for f in file_paths)
    click.echo(f"\nProcessing {len(file_paths)} file(s) totaling {format_size(total_size)}")
    
    # Process files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=CPUS) as executor:
        futures = [executor.submit(process_file, f) for f in file_paths]
        
        for future in concurrent.futures.as_completed(futures):
            file_counts, file_total = future.result()
            seq_counts.update(file_counts)
            total_sequences += file_total
    
    click.echo(f"\nProcessed {total_sequences:,} sequences")
    click.echo(f"Found {len(seq_counts):,} unique sequences")

    return sorted(seq_counts.items(), key=lambda x: x[1], reverse=True)

def filter_by_length(sequences, min_length, max_length):
    """Filter sequences by length."""
    with click.progressbar(sequences, label='Filtering sequences by length') as bar:
        filtered = [seq for seq in bar if min_length <= len(seq) <= max_length]
    
    click.echo(f"Kept {click.style(str(len(filtered)), fg='green')} sequences after length filtering")
    return filtered

def calculate_percentages(clusters, total_reads):
    """Calculate percentages for each cluster."""
    return {seq: (count, (count/total_reads)*100) 
            for seq, count in clusters.items()}

def find_elbow_point(x, y):
    """Find the elbow point in the curve using the kneedle algorithm."""
    x_norm = np.array(x) / np.max(x)
    y_norm = np.array(y) / np.max(y)
    
    kn = KneeLocator(
        x_norm, y_norm,
        curve='concave',
        direction='increasing',
        interp_method='polynomial',
        online=True
    )
    
    elbow_x = int(kn.knee * np.max(x))
    elbow_y = float(kn.knee_y * np.max(y))
    
    return elbow_x, elbow_y

def plot_cumulative_percentages(sorted_results, output_prefix):
    """Create a cumulative percentage plot with elbow point."""
    counts = [x[1][0] for x in sorted_results]
    percentages = [x[1][1] for x in sorted_results]
    
    cumulative_percentages = np.cumsum(percentages)
    sequence_numbers = range(1, len(cumulative_percentages) + 1)
    
    elbow_x, elbow_y = find_elbow_point(sequence_numbers, cumulative_percentages)
    
    plt.figure(figsize=(10, 6))
    plt.plot(sequence_numbers, cumulative_percentages, 'b-')
    plt.xlabel('Number of Sequences')
    plt.ylabel('Cumulative Percentage')
    plt.title('Cumulative Percentage vs Number of Sequences')
    plt.grid(True)
    
    plt.plot([elbow_x], [elbow_y], 'go', markersize=10)
    plt.annotate(f'Elbow: {elbow_x} seqs ({elbow_y:.1f}%)', 
                xy=(elbow_x, elbow_y),
                xytext=(30, 30), textcoords='offset points',
                arrowprops=dict(arrowstyle='->'))
    
    for pct in [25, 50, 75, 90]:
        if max(cumulative_percentages) >= pct:
            idx = np.where(cumulative_percentages >= pct)[0][0]
            plt.plot([idx+1], [cumulative_percentages[idx]], 'ro')
            plt.annotate(f'{pct}% at {idx+1} seqs', 
                        xy=(idx+1, cumulative_percentages[idx]),
                        xytext=(10, 10), textcoords='offset points')
    
    plt.tight_layout()
    plt.savefig(f"{output_prefix}_cumulative.png", dpi=300, bbox_inches='tight')
    plt.close()
    
    return elbow_x

def find_core_sequences(sequences, min_occurrence_fraction):
    """Find core sequences through parallel multiple sequence alignment."""
    click.echo("Finding core sequences through multiple sequence alignment...")
    
    sample_size = min(1000, len(sequences))
    sample_seqs = random.sample(sequences, sample_size)
    
    # Split sequences into chunks for parallel processing
    chunks = [sample_seqs[i:i+CHUNK_SIZE] for i in range(0, len(sample_seqs), CHUNK_SIZE)]
    
    def process_alignment_chunk(chunk):
        """Process a chunk of sequences for alignment."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as temp_in, \
             tempfile.NamedTemporaryFile(suffix='.aln', delete=False) as temp_out:
            
            for i, seq in enumerate(chunk):
                temp_in.write(f">seq{i}\n{seq}\n")
            temp_in.flush()
            
            try:
                subprocess.run(
                    ['muscle', '-align', temp_in.name, '-output', temp_out.name],
                    check=True, capture_output=True, text=True
                )
                
                alignment = AlignIO.read(temp_out.name, "fasta")
                return process_alignment(alignment, min_occurrence_fraction)
            finally:
                os.unlink(temp_in.name)
                os.unlink(temp_out.name)
    
    # Process chunks in parallel
    all_conserved_regions = []
    all_core_sequences = []
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=CPUS) as executor:
        futures = [executor.submit(process_alignment_chunk, chunk) for chunk in chunks]
        
        with click.progressbar(length=len(chunks), label='Processing alignments') as bar:
            for future in concurrent.futures.as_completed(futures):
                conserved_regions, core_sequences = future.result()
                all_conserved_regions.extend(conserved_regions)
                all_core_sequences.extend(core_sequences)
                bar.update(1)
    
    # Merge results
    merged_core_sequences = merge_core_sequences(all_core_sequences)
    
    return all_conserved_regions, merged_core_sequences

def merge_core_sequences(sequences):
    """Merge similar core sequences."""
    merged = []
    seen = set()
    
    for seq in sequences:
        if seq not in seen:
            merged.append(seq)
            seen.add(seq)
    
    return merged

def process_alignment(alignment, min_occurrence_fraction):
    """Process the multiple sequence alignment to find conserved regions."""
    alignment_length = alignment.get_alignment_length()
    seq_count = len(alignment)
    min_occurrences = int(seq_count * min_occurrence_fraction)
    
    conserved_regions = []
    current_region = []
    
    for i in range(alignment_length):
        column = alignment[:, i]
        base_counts = defaultdict(int)
        for base in column:
            if base != '-':
                base_counts[base] += 1
        
        most_common_base = max(base_counts.items(), key=lambda x: x[1], default=('-', 0))
        
        if most_common_base[1] >= min_occurrences:
            current_region.append((i, most_common_base[0]))
        elif current_region:
            conserved_regions.append(current_region)
            current_region = []
    
    if current_region:
        conserved_regions.append(current_region)
    
    # Convert regions to sequences
    core_sequences = []
    for region in conserved_regions:
        if len(region) >= 10:  # Only keep regions of at least 10 bp
            seq = ''.join(base for _, base in region)
            core_sequences.append(seq)
    
    return conserved_regions, core_sequences

def read_reference_sequences(fasta_file):
    """Read reference sequences from a FASTA file."""
    reference_seqs = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        reference_seqs[record.id] = str(record.seq)
    return reference_seqs

def check_probe_binding(probe_seq, reference_seq, max_distance):
    """Check if a probe sequence binds to a reference sequence."""
    result = edlib.align(probe_seq, reference_seq, task="locations", mode="HW", k=max_distance)
    return result["editDistance"] <= max_distance if result["editDistance"] != -1 else False

def reanalyze_results(results_file, new_elbow_point, output_prefix=None):
    """Reanalyze results with a new elbow point."""
    # Read the results file
    sequences = []
    click.echo("Reading results file...")
    with open(results_file) as f:
        header = f.readline()  # Skip header
        for line in f:
            seq, count, percentage = line.strip().split('\t')
            sequences.append((seq, (int(count), float(percentage))))
    
    # Validate the new elbow point
    if new_elbow_point <= 0 or new_elbow_point > len(sequences):
        raise ValueError(f"Elbow point must be between 1 and {len(sequences)}")
    
    # Select sequences up to the new elbow point
    selected_sequences = sequences[:new_elbow_point]
    
    # Set output prefix
    if output_prefix is None:
        output_prefix = Path(results_file).stem
    
    # Write new results file
    new_results_file = f"{output_prefix}_reanalyzed.tsv"
    with click.progressbar(length=1, label='Writing new results file') as bar:
        with open(new_results_file, 'w') as f:
            f.write("Sequence\tCount\tPercentage\n")
            for seq, (count, percentage) in selected_sequences:
                f.write(f"{seq}\t{count}\t{percentage:.4f}\n")
        bar.update(1)
    
    click.echo(f"Wrote {click.style(str(len(selected_sequences)), fg='green')} sequences to {click.style(new_results_file, fg='blue')}")
    
    # Generate new cumulative plot
    with click.progressbar(length=1, label='Generating cumulative plot') as bar:
        plot_cumulative_percentages(selected_sequences, f"{output_prefix}_reanalyzed")
        bar.update(1)
    
    return selected_sequences

def generate_probes(sequence, probe_length=25, min_probe_length=20):
    """Generate all possible probes of specified length from a sequence."""
    probes = []
    if len(sequence) < min_probe_length:
        return probes
        
    # If sequence is shorter than or equal to probe_length, return it as-is
    if len(sequence) <= probe_length:
        return [sequence]
        
    # Generate all possible probes of probe_length
    for i in range(len(sequence) - probe_length + 1):
        probes.append(sequence[i:i + probe_length])
    return probes

def write_probe_sequences(sorted_results, output_prefix, num_sequences=20, probe_length=25, min_probe_length=20, original_total_reads=None):
    """Generate and write probe sequences from top sequences."""
    probe_coverage = {}  # Maps probe -> set of sequences it can detect
    total_unique_seqs = len(sorted_results)
    filtered_total_reads = sum(count_or_tuple[0] if isinstance(count_or_tuple, tuple) else count_or_tuple 
                             for _, count_or_tuple in sorted_results)
    sequence_counts = {}  # Maps sequence -> read count
    
    # First pass: collect all sequences and their counts
    for seq, count_or_tuple in sorted_results:
        count = count_or_tuple[0] if isinstance(count_or_tuple, tuple) else count_or_tuple
        sequence_counts[seq] = count
    
    # Generate all possible probes and track which sequences they cover
    for seq in sequence_counts:
        seq_probes = generate_probes(seq, probe_length, min_probe_length)
        for probe in seq_probes:
            if probe not in probe_coverage:
                probe_coverage[probe] = set()
            probe_coverage[probe].add(seq)
    
    # Select minimal set of probes that maximizes coverage
    final_probes = set()
    uncovered_seqs = set(sequence_counts.keys())
    covered_reads = 0
    covered_seqs = 0
    
    while uncovered_seqs and probe_coverage:
        best_probe = max(
            probe_coverage.keys(),
            key=lambda p: sum(sequence_counts[seq] for seq in 
                            (probe_coverage[p] & uncovered_seqs))
        )
        
        # Add the probe and update coverage
        final_probes.add(best_probe)
        newly_covered = probe_coverage[best_probe] & uncovered_seqs
        covered_reads += sum(sequence_counts[seq] for seq in newly_covered)
        covered_seqs += len(newly_covered)
        uncovered_seqs -= probe_coverage[best_probe]
        
        del probe_coverage[best_probe]
        
        if len(final_probes) > len(sorted_results):
            break
    
    # Write probes to file
    output_file = f"{output_prefix}_probes.fasta"
    with open(output_file, 'w') as f:
        for i, probe in enumerate(sorted(final_probes), 1):
            f.write(f">probe_{i}\n{probe}\n")
    
    filtered_coverage = (covered_reads / filtered_total_reads * 100) if filtered_total_reads > 0 else 0
    total_coverage = (covered_reads / original_total_reads * 100) if original_total_reads else None
    seq_coverage = (covered_seqs / total_unique_seqs * 100) if total_unique_seqs > 0 else 0
    
    click.echo(f"\nGenerated {click.style(str(len(final_probes)), fg='green')} optimized probes")
    click.echo(f"These probes cover:")
    click.echo(f"  {click.style(f'{filtered_coverage:.2f}%', fg='green')} of filtered reads "
               f"({covered_reads:,} out of {filtered_total_reads:,} filtered reads)")
    if total_coverage is not None:
        click.echo(f"  {click.style(f'{total_coverage:.2f}%', fg='green')} of total reads "
               f"({covered_reads:,} out of {original_total_reads:,} total reads)")
    click.echo(f"  {click.style(f'{seq_coverage:.2f}%', fg='green')} of unique sequences "
               f"({covered_seqs:,} out of {total_unique_seqs:,} sequences)")
    click.echo(f"Probes written to: {click.style(output_file, fg='blue')}")
    
    return list(final_probes), filtered_coverage, total_coverage

def process_fastq(input_files, output_prefix, min_length=None, max_length=None, 
                 edit_distance=1, num_sequences=20, probe_length=25, min_probe_length=20,
                 find_core=False, core_length=25, min_core_occurrence=0.1,
                 reference_file=None, max_binding_dist=2, subsample=None):
    """Process FASTQ files and generate probes."""
    
    # Read and process FASTQ files
    sequences = read_fastq_files(input_files, subsample, min_length, max_length)
    total_sequences = sum(count for _, count in sequences)
    
    # Cluster similar sequences
    if edit_distance > 0:
        click.echo("\nClustering similar sequences...")
        filtered_counts = cluster_sequences(sequences, edit_distance)
        sorted_results = sorted(
            [(seq, (count, (count/total_sequences)*100)) 
             for seq, count in filtered_counts.items()],
            key=lambda x: x[1][0], reverse=True
        )
    else:
        sorted_results = sorted(
            [(seq, (count, (count/total_sequences)*100)) 
             for seq, count in sequences],
            key=lambda x: x[1][0], reverse=True
        )
    
    # Write results
    click.echo("\nWriting results...")
    with open(f"{output_prefix}.tsv", 'w') as f:
        f.write("Sequence\tCount\tPercentage\n")
        for seq, (count, percentage) in sorted_results:
            f.write(f"{seq}\t{count}\t{percentage:.4f}\n")
    
    click.echo(f"Wrote {click.style(str(len(sorted_results)), fg='green')} sequences to {output_prefix}.tsv")
    
    # Generate cumulative plot
    click.echo("Generating cumulative plot...")
    elbow_point = plot_cumulative_percentages(sorted_results, output_prefix)
    
    # Generate probes
    click.echo("\nGenerating probes...")
    probes, filtered_coverage, total_coverage = write_probe_sequences(
        sorted_results[:num_sequences], 
        output_prefix, 
        num_sequences=num_sequences,
        probe_length=probe_length,
        min_probe_length=min_probe_length,
        original_total_reads=total_sequences
    )
    
    # Process reference sequences if provided
    if reference_file:
        click.echo("\nChecking probe binding...")
        reference_seqs = read_reference_sequences(reference_file)
        write_binding_results(probes, reference_seqs, max_binding_dist, output_prefix)
    
    return probes, filtered_coverage, total_coverage