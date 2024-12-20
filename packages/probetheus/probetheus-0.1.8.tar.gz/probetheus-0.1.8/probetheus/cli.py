"""Command-line interface for PROBETHEUS."""

import click
import glob
from . import core
from . import __version__

@click.group()
@click.version_option(version=__version__)
def cli():
    """PROBETHEUS: Process FASTQ files to find and analyze sequences."""
    pass

@cli.command()
@click.argument('input_files', nargs=-1, type=click.Path(exists=True))
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
              default='reservoir', help='Method to use for subsampling')
def process(input_files, output, min_length, max_length, skip_length_filter, edit_distance, top_n,
           probe_length, min_probe_length, find_core, core_length, min_core_occurrence, 
           reference, max_binding_dist, subsample, reads, cores, sampling_method):
    """Process FASTQ files to find and analyze sequences.
    
    INPUT_FILES: One or more FASTQ files (supports wildcards like *.fastq.gz)
    """
    if not input_files:
        raise click.UsageError("No input files provided")
        
    # Process the input files
    output_prefix = output.rsplit('.', 1)[0]
    
    probes, filtered_coverage, total_coverage = core.process_fastq(
        list(input_files),  # Convert tuple to list
        output_prefix,
        min_length=min_length,
        max_length=max_length,
        edit_distance=edit_distance,
        num_sequences=top_n,
        probe_length=probe_length,
        min_probe_length=min_probe_length,
        find_core=find_core,
        core_length=core_length,
        min_core_occurrence=min_core_occurrence,
        reference_file=reference,
        max_binding_dist=max_binding_dist,
        subsample=subsample
    )
    
    # Check probe binding if reference is provided
    if reference:
        click.echo(click.style("\nChecking probe binding...", fg='blue'))
        reference_seqs = core.read_reference_sequences(reference)
        core.write_binding_results(probes, reference_seqs, max_binding_dist, output_prefix)
    
    click.echo(click.style("\nProcessing complete!", fg='green', bold=True))

def main():
    cli()

if __name__ == '__main__':
    main() 