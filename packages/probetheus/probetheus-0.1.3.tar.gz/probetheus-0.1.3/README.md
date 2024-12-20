# PROBETHEUS

A Python package to detect overrepresented sequences in a fastq file and design probes against them. Designed for single read sequencing from immunoprecipitation experiments, riboSeq, and other single read sequencing experiments.

## Installation

```bash
pip install probetheus
```

## Features

- Process single-end FASTQ files to find top represented sequences
- Generate probes from top sequences with customizable lengths
- Cluster sequences based on edit distance
- Detect probe binding sites against reference sequences
- Generate cumulative percentage plots with elbow point detection
- Reanalyze results with custom elbow points
- Subsample input files for faster analysis or testing

## Usage

### Processing FASTQ Files and Generating Probes

```bash
# Basic usage
probetheus process --input input.fastq.gz --output results.tsv

# With core sequence analysis
probetheus process --input input.fastq.gz --output results.tsv --find_core --core_length 25

# Process without length filtering
probetheus process --input input.fastq.gz --output results.tsv --skip_length_filter

# Check probe binding against reference
probetheus process --input input.fastq.gz --output results.tsv --reference ref.fasta --max_binding_dist 2

# Process with subsampling (e.g., use 20% of reads)
probetheus process --input input.fastq.gz --output results.tsv --subsample 20
```

### Reanalyzing Results

After initial processing, you can reanalyze the results with a different elbow point:

```bash
# Reanalyze with a new elbow point
probetheus reanalyze --input results.tsv --elbow 5 --output-prefix new_results
```

This will create:
- `new_results_reanalyzed.tsv`: New results file with selected sequences
- `new_results_reanalyzed_cumulative.png`: Updated cumulative plot

## Arguments

### Process Command
- `--input`, `-i`: Input FASTQ files (can be multiple)
- `--output`, `-o`: Output table file
- `--min-length`: Minimum sequence length (default: 20)
- `--max-length`: Maximum sequence length (default: 50)
- `--top-n`: Number of top sequences to use for probe generation (default: 20)
- `--probe-length`: Length of generated probes (default: 25)
- `--min-probe-length`: Minimum acceptable probe length (default: 20)
- `--edit-distance`: Maximum edit distance for clustering (default: 1)
- `--find-core`: Find core sequences
- `--core-length`: Length for core sequence analysis (default: 25)
- `--min-core-occurrence`: Minimum fraction of sequences a core must appear in (default: 0.1)
- `--reference`, `-r`: Reference FASTA file to check probe binding
- `--max-binding-dist`: Maximum edit distance allowed for probe binding (default: 2)
- `--subsample`: Subsample percentage (1-100) of reads from each file
- `--cpus`: Number of CPU cores to use (default: 8, max: number of cores - 1)

### Reanalyze Command
- `--input`, `-i`: Input results.tsv file from previous analysis
- `--elbow`, `-e`: New elbow point (number of sequences to keep)
- `--output-prefix`, `-o`: Prefix for output files (optional)

## License

This project is licensed under the MIT License - see the LICENSE file for details. 