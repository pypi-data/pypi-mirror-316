"""Command-line interface for PROBETHEUS."""

import click
from pathlib import Path
import warnings
from . import core
import multiprocessing as mp

# Suppress Biopython deprecation warnings
warnings.filterwarnings('ignore', category=UserWarning, module='Bio')

@click.group()
def cli():
    """PROBETHEUS: Process and analyze sequence data with probe binding site detection."""
    pass

@cli.command()
@click.option('--input', '-i', required=True, multiple=True, type=click.Path(exists=True), help='Input FASTQ files (can be multiple)')
@click.option('--output', '-o', required=True, help='Output table file')
@click.option('--min-length', type=int, default=20, help='Minimum sequence length')
@click.option('--max-length', type=int, default=50, help='Maximum sequence length')
@click.option('--skip-length-filter', is_flag=True, help='Skip length filtering step')
@click.option('--edit-distance', type=int, default=1, help='Maximum edit distance for clustering')
@click.option('--top-n', type=int, default=50, help='Number of top sequences to output')
@click.option('--probe-length', type=int, default=25, help='Length of generated probes')
@click.option('--min-probe-length', type=int, default=20, help='Minimum acceptable probe length')
@click.option('--find-core', is_flag=True, help='Find core sequences')
@click.option('--core-length', type=int, default=25, help='Length for core sequence analysis')
@click.option('--min-core-occurrence', type=float, default=0.1,
              help='Minimum fraction of sequences a core must appear in')
@click.option('--reference', '-r', type=str, help='Reference FASTA file to check probe binding')
@click.option('--max-binding-dist', type=int, default=2,
              help='Maximum edit distance allowed for probe binding')
@click.option('--subsample', type=float, default=10.0, help='Subsample percentage (1-100) of reads from each file')
@click.option('--reads', type=int, help='Number of reads to take from each file (overrides --subsample if provided)')
@click.option('--cores', type=int, default=8, help='Number of CPU cores to use (default: 8)')
@click.option('--sampling-method', type=click.Choice(['reservoir', 'first']), 
              default='reservoir', help='Method to use for subsampling, first just takes the first X% and is faster but less random')
def process(input, output, min_length, max_length, skip_length_filter, edit_distance, top_n,
           probe_length, min_probe_length, find_core, core_length, min_core_occurrence, 
           reference, max_binding_dist, subsample, reads, cores, sampling_method):
    """Process FASTQ files to find and analyze sequences."""
    
    # Set number of cores
    core.CPUS = min(cores, max(1, mp.cpu_count() - 2))  # Ensure at least 1 core and max of available-2
    
    # Print processing information
    if reads is not None:
        click.echo(click.style(f"Taking {reads:,} reads from each file", fg='blue'))
    elif subsample == 100:
        click.echo(click.style("Processing all reads (no subsampling)", fg='blue'))
    else:
        click.echo(click.style(f"Subsampling {subsample}% of reads from each file", fg='blue'))
    
    click.echo("Starting sequence processing...")
    
    # Read and process sequences
    seq_counts, total_sequences = core.read_fastq_files(
        input,
        subsample=subsample,
        reads=reads,
        min_length=None if skip_length_filter else min_length,
        max_length=None if skip_length_filter else max_length,
        sampling_method=sampling_method
    )
    
    # Sort sequences by count
    sorted_seqs = sorted(seq_counts.items(), key=lambda x: x[1], reverse=True)
    
    click.echo(f"\nProcessed {total_sequences:,} sequences")
    click.echo(f"Found {len(sorted_seqs):,} unique sequences\n")
    
    # Get total reads for percentage calculations
    total_reads = sum(count for seq, count in sorted_seqs)
    
    # Cluster similar sequences if requested
    if edit_distance > 0:
        click.echo(click.style("\nClustering similar sequences...", fg='blue'))
        clusters = core.cluster_sequences(sorted_seqs, edit_distance)
        sorted_results = sorted(clusters.items(), key=lambda x: x[1], reverse=True)[:top_n]
    else:
        sorted_results = sorted_seqs[:top_n]
    
    # Calculate percentages
    results = [(seq, (count, (count/total_reads)*100)) 
              for seq, count in sorted_results]
    
    # Check probe binding if reference is provided
    binding_info = {}
    if reference:
        click.echo(click.style("\nChecking probe binding...", fg='blue'))
        reference_seqs = core.read_reference_sequences(reference)
        for seq, _ in results:
            for ref_id, ref_seq in reference_seqs.items():
                if core.check_probe_binding(seq, ref_seq, max_binding_dist):
                    binding_info[seq] = True
                    break
            if seq not in binding_info:
                binding_info[seq] = False

    # Write results
    output_prefix = Path(output).stem
    with click.progressbar(length=1, label='Writing results') as bar:
        with open(output, 'w') as f:
            f.write("Sequence\tCount\tPercentage\tCumulative_Count\tCumulative_Percentage\tBinding\n")
            cumulative_count = 0
            cumulative_percentage = 0
            for seq, (count, percentage) in results:
                cumulative_count += count
                cumulative_percentage += percentage
                binding = "Yes" if binding_info.get(seq, False) else "No"
                f.write(f"{seq}\t{count}\t{percentage:.4f}\t{cumulative_count}\t{cumulative_percentage:.4f}\t{binding}\n")
        bar.update(1)
    
    click.echo(f"Wrote {click.style(str(len(results)), fg='green')} sequences to {click.style(output, fg='blue')}")
    
    # Generate cumulative plot
    with click.progressbar(length=1, label='Generating cumulative plot') as bar:
        elbow_point = core.plot_cumulative_percentages(results, output_prefix)
        bar.update(1)
    
    # Get optimal sequences (up to elbow point)
    optimal_sequences = results[:elbow_point]
    
    # Generate probes from optimal sequences
    click.echo(click.style("\nGenerating probes...", fg='blue'))
    probes, filtered_coverage, total_coverage = core.write_probe_sequences(
        optimal_sequences, 
        output_prefix,
        num_sequences=top_n,
        probe_length=probe_length,
        min_probe_length=min_probe_length,
        original_total_reads=total_reads
    )
    
    # Find core sequences if requested
    if find_core:
        click.echo(click.style("\nAnalyzing core sequences...", fg='blue'))
        conserved_regions = core.find_core_sequences(
            [seq for seq, _ in optimal_sequences],
            min_core_occurrence
        )
        
        output_file = f"{output_prefix}_core_sequences.txt"
        core.write_core_sequences(conserved_regions, optimal_sequences, output_prefix, 
                                reference_seqs=None, max_binding_dist=None)
    
    # Check probe binding if reference is provided
    if reference:
        click.echo(click.style("\nChecking probe binding...", fg='blue'))
        reference_seqs = core.read_reference_sequences(reference)
        core.write_binding_results(probes, reference_seqs, max_binding_dist, output_prefix)
    
    click.echo(click.style("\nProcessing complete!", fg='green', bold=True))

@cli.command()
@click.option('--input', '-i', required=True, help='Input results.tsv file')
@click.option('--elbow', '-e', type=int, required=True, help='New elbow point (number of sequences)')
@click.option('--output-prefix', '-o', help='Output prefix for new files')
def reanalyze(input, elbow, output_prefix):
    """Reanalyze results with a new elbow point."""
    click.echo(click.style("Starting reanalysis...", fg='blue', bold=True))
    
    try:
        core.reanalyze_results(input, elbow, output_prefix)
        click.echo(click.style("\nReanalysis complete!", fg='green', bold=True))
    except ValueError as e:
        click.echo(click.style(f"Error: {e}", fg='red'))
        return 1
    return 0

def main():
    """Main entry point for the command-line interface."""
    cli() 