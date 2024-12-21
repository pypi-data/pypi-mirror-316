"""
Usage:
        smrnatk-collate (<collapsed_fastq>... | --m <metadata_file>) [options]

Options:

    -b STRING --basename=STRING     Basename of the ouput fasta and csv

"""

# smrnatk-collate fastq [options] <fastq_file>...
# smrnatk-collate meta [options] <metadata_file>...
# smrnatk-collate (<fastq_file>... | -m <metadata_file>)

import os
from collections import Counter

import pandas as pd
from docopt import docopt


def collate(sample_name, collapsed, basename):
    """
    The collate function retains the number of reads in each individual
    collapsed fastq file. The result is a meta-collapsed fastq file and a
    matrix file with sum of shared sequences in all files along with number of
    reads for that sequence in each file.

    Accepts multiple fastq/fasta files in one go or a text/csv file with sample
    name on first column and file paths on second column. If multiple
    fastq/fasta files was the input, the file basename will be the sample
    names.
    """
    sample_counts = Counter()

    for i in range(len(collapsed)):
        with open(collapsed[i]) as f:
            for header in f:
                header = header[1:].strip()
                seq = next(f).replace("\n", "")
                # counts unique read occurence to find abundance
                if header.startswith("sequence"):
                    num_reads = int(header.split("_")[-1])
                    sample_counts[sample_name[i], seq] += num_reads

    # Makes complete dataframe with non-collapsed sequences, shows sequences in
    # each samples
    samples = [list(sample_counts.keys()), list(sample_counts.values())]
    df_samples = pd.DataFrame(
        {
            "sample": [_[0] for _ in samples[0]],
            "seqs": [_[1] for _ in samples[0]],
            "reads": samples[1],
        },
        columns=["sample", "seqs", "reads"],
    ).sort_values("sample")

    samp = list(df_samples["sample"].unique())  # list of all file names
    list(df_samples["seqs"].unique())

    concat = df_samples[df_samples["sample"] == samp[0]]
    concat.columns = ["sample", "seqs", samp[0]]
    concat = concat.drop(["sample"], axis=1).reset_index(drop=True)

    # Concatenated dataframe for all samples showing reads per sample for that
    # particular sequence
    for name in samp[1:]:
        s = df_samples[df_samples["sample"] == name]
        s.columns = ["sample", "seqs", name]
        s = s.drop(["sample"], axis=1).reset_index(drop=True)
        concat = pd.merge(concat, s, on="seqs", how="outer")

    concat = concat.fillna(0)
    concat["sum"] = (concat[samp]).sum(1).astype(int)
    concat = concat.sort_values("sum", ascending=False)
    concat["nonzeros"] = (concat[samp] != 0).sum(1)
    concat = concat.reset_index(drop=True)
    concat["id"] = (
        "sequence"
        + concat.index.astype(str)
        + "_"
        + concat["nonzeros"].astype(str)
        + "_"
        + concat["sum"].astype(str)
    )
    concat = concat.drop(
        [
            "sum",
            "nonzeros",
        ],
        axis=1,
    )
    concat = concat[["id", "seqs"] + samp]

    concat.to_csv(basename + ".csv", index=False)

    with open(basename + ".fasta", "w") as f:
        for i in range(len(concat)):
            f.write(">{}\n{}\n".format(concat["id"][i], concat["seqs"][i]))


def main(argv=None):
    # read in command line variables
    args = docopt(__doc__, argv=argv)
    args["--basename"] = args.get("--basename")
    args["<collapsed_fastq>"] = args.get("<collapsed_fastq>")
    args["--m"] = args.get("--m")
    args["<metadata_file>"] = args.get("<metadata_file>")
    collate_fn = None
    if args["--basename"] is None:
        collate_fn = "all_samples_collate"
    if args["--basename"] is not None:
        collate_fn = args["--basename"]
    if args["--m"]:
        files = pd.read_csv(
            args["<metadata_file>"], sep=None, engine="python", header=None
        )
        files = files.dropna(axis="columns")  # if tab isn't sniffed correctly
        sample_name, collapsed = (
            files[list(files)[0]].tolist(),
            files[list(files)[-1]].tolist(),
        )
        collate(sample_name, collapsed, collate_fn)
    if args["<collapsed_fastq>"]:
        sample_name = [os.path.basename(file) for file in args["<collapsed_fastq>"]]
        collate(sample_name, args["<collapsed_fastq>"], collate_fn)
