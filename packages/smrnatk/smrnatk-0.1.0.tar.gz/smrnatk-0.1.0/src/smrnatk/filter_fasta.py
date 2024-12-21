"""
Usage:
    smrnatk-filter <collapsed fasta> <n_reads> [options]

Options:
    -o FILE --output=FILE  Filename to output
"""

import os

import pandas as pd
from docopt import docopt

def filter_fasta(dat, min_count, output_fn: str | None):
    """
    Function allows the user to input a collapsed fasta or fastq file and
    remove sequences with less than n_reads.  Outputs a fasta file with
    sequences abundance that is higher than n_reads.
    """
    seqs = {}

    with open(dat) as f:
        for header in f:
            header = header[1:].strip()
            seq = next(f).replace("\n", "")
            # counts unique read occurence to find abundance
            # Note: only works with collapsed fasta files with name as sequence
            # and _ splits
            if header.startswith("sequence") and int(header.split("_")[-1]) >= min_count:
                seqs[header] = seq

    df_seq = pd.DataFrame(
        {"seqid": list(seqs.keys()), "seqs": list(seqs.values())},
        columns=["seqid", "seqs"],
    )

    with open(output_fn, "w") as f:
        for i in range(len(df_seq)):
            f.write(">{}\n{}\n".format(df_seq["seqid"][i], df_seq["seqs"][i]))


def main(argv=None):
    # read in command line variables
    args = docopt(__doc__, argv=argv)

    if args["--output"] is None:
        basename = os.path.basename(args["<collapsed fasta>"]).split(".")[0]
        filter_fn = basename + "_filtered.fasta"
    else:
        filter_fn = args["--output"]

    filter_fasta(args["<collapsed fasta>"], args["<n_reads>"], filter_fn)
