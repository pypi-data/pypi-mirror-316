# smrnatk

This project implements a de novo clustering methology for
analyzing and interpreting smRNA-Seq data.

## Introduction

The small RNA toolkit (smRNAtk) is a comprehensive set of utilities built for the purpose of cleaning and analyzing raw RNA NGS data   

## Documentation

Full documentation is in progress. For the time being here are the command line options that are currently implemented:

### Quality Report

Produce plots of quality for a number of different phred score thresholds.

`smrnatk-quality_report [options] <fastq>`

### Quality Filter

Filter fastq reads if they contain more than N bases less than a given phred score

`smrnatk-quality_filter [options] <fastq>`

### Collapse

Collapse fastq reads into a fasta file. The number of original reads collapsed per sequence is recorded in the fasta header.

`smrnatk-collapse <fastq>`

### Align

Align the sequences in the fasta file provided against a reference genome. The default behavior assumes bowtie is installed, but the user may provide their own alignment command as an optional argument.

`smrnatk-align <fasta> --align-cmd=CMD`

### Compute metaMir matrices

Using the given alignments, compute metaMir matrices for every annotation in the provided GTF file, e.g. the one provided by mirBase.

`smrnatk-metamir <annotation_gtf> <bam> --output=<metamir_data>`

The output is a JSON formatted file that contains all of the metaMir matrices for a single BAM file (e.g. sample). These JSON files are used in the merge and aggregate step.

### Merge metaMir matrices

Concatenate individual results from the `metamir` command into a single file. The resulting JSON file contains the individual metaMir matrices for each sample for each annotation. This is useful for grouping samples together for later aggregation, e.g. into disease and control conditions.

`smrnatk-merge <metamir_data>...`

### Aggregate metaMir matrices

Aggregate metaMir matrices that were merged into a single file with `merge`. This operation sums the metaMir matrices for every sample in a given JSON output file and produces a single result per annotation.

`smrnatk-aggregate <metamir_data>`

### Quantify metaMir matrices into a counts file

Sum different portions of the metaMir matrices to produce a traditional counts matrix with samples (i.e. `merge`'ed metaMir matrices) as columns and annotations as rows. The optional `--window` argument allows the user three options for summing matrices:

- `canonical`: default, use only the count in the canonical annotation coordinates (0,0)
- `seed`: sum the column (0,*), which includes all species that have the same seed sequence as the annotation
- `whole`: sum the entire matrix, which includes all alignments in a 10x10 window around the annotated start positions

`smrnatk-quant [options] <merged_metamir_data>`

## Installing

Currently the only way to install this software is as follows:

```
$ git clone https://bitbucket.org/rtingram/smrnatk.git
$ cd smrnatk
$ python setup.py install
```

We recommend using [conda](https://conda.io/miniconda.html) to create an isolated environment when installing:

```
$ conda create -n my_smallrna_project
$ source activate my_smallrna_project
$ python setup.py install
```

