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

# Global variables for multiprocessing
CPUS = max(1, mp.cpu_count() - 1)  # Leave one CPU free for system

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
    """Cluster sequences based on k-mer similarity."""
    if max_edit_distance <= 0:
        return dict(sorted_seqs)
    
    click.echo("Filtering similar sequences using k-mer similarity...")
    filtered_counts = {}
    kmers_cache = {}
    total_seqs = len(sorted_seqs)
    
    # Create a progress bar without showing ETA
    with click.progressbar(
        sorted_seqs,
        label='Analyzing sequences',
        length=len(sorted_seqs),
        show_eta=False
    ) as sequences:
        for seq, count in sequences:
            # Skip if very similar to an existing sequence
            skip = False
            seq_kmers = kmers_cache.get(seq) or get_kmers(seq)
            kmers_cache[seq] = seq_kmers
            
            for existing_seq in filtered_counts:
                # Quick length check
                if abs(len(seq) - len(existing_seq)) > max_edit_distance:
                    continue
                
                # Check k-mer similarity
                existing_kmers = kmers_cache.get(existing_seq) or get_kmers(existing_seq)
                kmers_cache[existing_seq] = existing_kmers
                
                similarity = len(seq_kmers & existing_kmers) / len(seq_kmers | existing_kmers)
                if similarity >= 0.9:  # High threshold for better accuracy
                    filtered_counts[existing_seq] += count
                    skip = True
                    break
            
            if not skip:
                filtered_counts[seq] = count
    
    return filtered_counts

def get_kmers(seq, k=7):
    """Get k-mers from a sequence."""
    return set(seq[i:i+k] for i in range(len(seq)-k+1))

def check_probe_binding_chunk(args):
    """Process a chunk of sequences for probe binding."""
    sequences, reference_seqs, max_distance = args
    results = []
    
    for seq in sequences:
        for ref_id, ref_seq in reference_seqs.items():
            if check_probe_binding(seq, ref_seq, max_distance):
                results.append((seq, ref_id))
    
    return results

def write_binding_results(sequences, reference_seqs, max_distance, output_prefix):
    """Write probe binding results to a file using parallel processing."""
    output_file = f"{output_prefix}_binding_sites.tsv"
    total_bindings = 0
    
    # Split sequences into chunks for parallel processing
    chunks = chunk_list(sequences, CPUS)
    chunk_args = [(chunk, reference_seqs, max_distance) for chunk in chunks]
    
    with open(output_file, 'w') as f:
        f.write("Sequence\tReference\tBinding_Sites\n")
        
        with click.progressbar(length=len(sequences), label='Checking probe binding') as bar:
            with mp.Pool(CPUS) as pool:
                for chunk_results in pool.imap_unordered(check_probe_binding_chunk, chunk_args):
                    for seq, ref_id in chunk_results:
                        f.write(f"{seq}\t{ref_id}\tTrue\n")
                        total_bindings += 1
                    bar.update(len(chunk_results))
    
    click.echo(f"Found {click.style(str(total_bindings), fg='green')} binding sites")

def read_fastq_files(file_paths, subsample=None, min_length=None, max_length=None):
    """Read and process FASTQ files on-the-fly."""
    seq_counts = defaultdict(int)
    total_sequences = 0
    
    # Create a single progress bar for all files
    with click.progressbar(
        file_paths,
        label='Processing files',
        show_pos=True,
        item_show_func=lambda x: f"Processing {x}" if x else None
    ) as files:
        for file_path in files:
            file_counter = defaultdict(int)
            
            # Get file size and setup opener
            opener = gzip.open if file_path.endswith('.gz') else open
            
            # Process sequences in chunks
            with opener(file_path, 'rt') as handle:
                chunk_size = 100000
                current_chunk = []
                processed_seqs = 0
                
                # Get total records count for accurate progress estimation
                total_records = sum(1 for _ in SeqIO.parse(handle, 'fastq'))
                handle.seek(0)  # Reset file pointer
                
                with click.progressbar(
                    SeqIO.parse(handle, 'fastq'),
                    length=total_records,
                    label=f'Reading {os.path.basename(file_path)}',
                    show_pos=True,
                    update_min_steps=1000
                ) as records:
                    for record in records:
                        if subsample is not None and random.random() * 100 > subsample:
                            continue
                        
                        seq = str(record.seq)
                        
                        if min_length and len(seq) < min_length:
                            continue
                        if max_length and len(seq) > max_length:
                            continue
                        
                        current_chunk.append(seq)
                        processed_seqs += 1
                        
                        if len(current_chunk) >= chunk_size:
                            for s in current_chunk:
                                file_counter[s] += 1
                            current_chunk = []
                
                # Process remaining sequences
                if current_chunk:
                    for s in current_chunk:
                        file_counter[s] += 1
            
            # Update total counts (no minimum count filter)
            for seq, count in file_counter.items():
                seq_counts[seq] += count
            total_sequences += processed_seqs
    
    total_reads = sum(count for seq, count in seq_counts.items())
    click.echo(f"Processed {total_sequences:,} sequences")
    click.echo(f"Found {len(seq_counts):,} unique sequences with {total_reads:,} total reads")
    
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
    """Find core sequences through multiple sequence alignment."""
    click.echo("Finding core sequences through multiple sequence alignment...")
    
    sample_size = min(1000, len(sequences))
    sample_seqs = random.sample(sequences, sample_size)
    click.echo(f"Using {click.style(str(len(sample_seqs)), fg='green')} sequences for alignment")
    click.echo(f"Sequence length range: {click.style(str(min(len(s) for s in sample_seqs)), fg='yellow')} - "
               f"{click.style(str(max(len(s) for s in sample_seqs)), fg='yellow')} bp")
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.fasta', delete=False) as temp_in, \
         tempfile.NamedTemporaryFile(suffix='.aln', delete=False) as temp_out:
        
        with click.progressbar(enumerate(sample_seqs), length=len(sample_seqs),
                             label='Writing sequences for alignment') as bar:
            for i, seq in bar:
                temp_in.write(f">seq{i}\n{seq}\n")
        temp_in.flush()
        
        with click.progressbar(length=1, label='Running MUSCLE alignment') as bar:
            try:
                # Use subprocess directly instead of Bio.Application
                result = subprocess.run(
                    ['muscle', '-align', temp_in.name, '-output', temp_out.name],
                    check=True, capture_output=True, text=True
                )
                bar.update(1)
                click.echo(click.style("MUSCLE alignment completed successfully", fg='green'))
            except subprocess.CalledProcessError as e:
                click.echo(click.style(f"Error running MUSCLE: {e}", fg='red'))
                return [], []
            except FileNotFoundError:
                click.echo(click.style("MUSCLE not found. Please install MUSCLE alignment tool", fg='red'))
                return [], []
        
        try:
            alignment = AlignIO.read(temp_out.name, "fasta")
        except Exception as e:
            click.echo(click.style(f"Error reading alignment: {e}", fg='red'))
            return [], []
        finally:
            os.unlink(temp_in.name)
            os.unlink(temp_out.name)
        
        conserved_regions, core_sequences = process_alignment(alignment, min_occurrence_fraction)
        
        # Add output of results
        if core_sequences:
            click.echo(f"\nFound {click.style(str(len(core_sequences)), fg='green')} core sequences:")
            for i, seq in enumerate(core_sequences, 1):
                click.echo(f"{i}. Length: {len(seq)} bp\n   Sequence: {seq}")
            
            # Write core sequences to a FASTA file
            output_file = f"{output_prefix}_core_sequences.fasta"
            with open(output_file, 'w') as f:
                for i, seq in enumerate(core_sequences, 1):
                    f.write(f">core_sequence_{i}\n{seq}\n")
            click.echo(f"\nCore sequences written to: {click.style(output_file, fg='blue')}")
        else:
            click.echo(click.style("No core sequences found meeting the criteria", fg='yellow'))
        
        return conserved_regions, core_sequences

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
    """Generate probes of specified length from a sequence.
    
    Args:
        sequence: Input DNA sequence
        probe_length: Desired length of probes (default: 25)
        min_probe_length: Minimum acceptable probe length (default: 20)
    
    Returns:
        List of probe sequences
    """
    # For the new approach, we just return the sequence as-is if it's the right length
    if len(sequence) == probe_length:
        return [sequence]
    elif len(sequence) >= min_probe_length:
        # If sequence is longer, take the middle portion
        start = (len(sequence) - probe_length) // 2
        return [sequence[start:start + probe_length]]
    return []

def write_probe_sequences(sorted_results, output_prefix, num_sequences=20, probe_length=25, min_probe_length=20):
    """Generate and write probe sequences from top sequences."""
    probes = []
    total_percentage = 0
    sequences_used = 0
    
    # Process sequences - each entry should already be a probe
    for probe, count_or_tuple in sorted_results:
        if len(probe) >= min_probe_length:
            probes.append(probe)
            # Handle both simple counts and (count, percentage) tuples
            if isinstance(count_or_tuple, tuple):
                count = count_or_tuple[0]  # Use the count from the tuple
            else:
                count = count_or_tuple
            sequences_used += 1
    
    # Write probes to file
    output_file = f"{output_prefix}_probes.fasta"
    with open(output_file, 'w') as f:
        for i, probe in enumerate(probes, 1):
            f.write(f">probe_{i}\n{probe}\n")
    
    click.echo(f"\nGenerated {click.style(str(len(probes)), fg='green')} probes "
               f"from {click.style(str(sequences_used), fg='green')} sequences")
    click.echo(f"These sequences represent {click.style(f'{sequences_used}', fg='green')} "
               f"unique sequences")
    click.echo(f"Probes written to: {click.style(output_file, fg='blue')}")
    
    return probes, sequences_used