"""
Usage:
    smrnatk-collapse <fastq> [options]

Options:

    --pseudo-fastq         Create a pseudo-fastq file instead of a fasta file
    -o FILE --output=FILE  Filename to output collapsed reads to, default is
                           the basename of the input fastq/fasta file with
                           _collapse added before the extension

"""

import collections
import json
import os
import sys

import pysam
from docopt import docopt

# TODO(labadorf, 2024-12-16): should refactor this function to accept a fastq iterator
# instead of filename
# TODO(labadorf, 2024-12-16): should allow collaps_fn to be any object that implements the
# io.RawIOBase interface
def collapse(fastq_fn: str, collapse_fn: str | None = None, pseudofq: bool = False) -> dict:
    """
    The collapse function reduces non-unique reads to solely unique reads and
    outputs the result to either a traditional fasta file, or if the user
    desires, a pseudo-fastq file.  The pseudo-fastq is named as such due to the
    fact that the quality score for each collapsed read is the maximum Phred
    score.
    """

    results_dict = collections.OrderedDict()
    total_reads = 0

    # organize the collapse starts
    seq_counts = {}

    # open the fastq file and store unique reads in dictionary with count of
    # occurance
    # TODO(labadorf, 2024-12-16): should possibly implement this as a trie instead of a
    # dict, this will break when all the reads in a file don't fit in memory
    # TODO(labadorf, 2024-12-16): should gracefully handle gzipped files as well
    with pysam.FastqFile(fastq_fn) as ff:
        for entry in ff:
            total_reads += 1

            if entry.sequence not in results_dict:
                results_dict[entry.sequence] = 1
            else:
                results_dict[entry.sequence] += 1

    # if user doesn't specify output name, don't output reads
    if collapse_fn is None:
        # TODO(labadorf, 2024-12-16): should gracefully handle gzipped files as well
        # write to the null device cross platform
        collapse_fn = os.devnull

    outfile = open(collapse_fn, "w")

    for i, (key, value) in enumerate(results_dict.items()):
        seq_name = f"sequence{i}_{value}"

        # keep track of the counts for each read to pass to
        # metamir function later
        seq_counts[seq_name] = value

        if pseudofq is False:
            # format the collapse data into fasta format
            outfile.write(f">{seq_name}\n{key}\n")

        else:
            read_len = len(key)

            # maximum quality in phred+33 is I
            # TODO: would be better to keep track of all the read qualities
            # and take the minimum in each position
            pseudo_qual = "I" * read_len

            outfile.write(f"@{seq_name}\n{key}\n+\n{pseudo_qual}\n")

    collapse_stats = {
        "counts": seq_counts,
        "unique_reads": len(seq_counts),
        "unique_content": round((len(seq_counts) / total_reads), 4),
        "total_reads": total_reads,
    }

    # TODO(labadorf, 2024-12-16): probably shouldn't write this out to json
    # use the file basename to write collapse stats to json
    #output_fn = collapse_fn.split(".")[0] + ".json"

    # output collapse stats to json
    #with open(output_fn, "w") as outfile:
    #    json.dump(collapse_stats, outfile, indent=4)
    outfile.close()

    # convert stats dict to pandas df
    # collapse_stats_df = pd.DataFrame.from_dict(collapse_stats,
    # orient='index', columns= ['results'])

    return collapse_stats


def main(argv=None):
    # read in command line variables
    args = docopt(__doc__, argv=argv)
    args["--output"] = args.get("--output")
    args["<fastq>"] = args.get("<fastq>")
    print(args["--pseudo-fastq"])
    if args["--output"] is not None:
        output = args["--output"]
    if args["--output"] is None:
        output = os.path.basename(args["<fastq>"]).split(".")[0]
    if args["--pseudo-fastq"]:
        output = output + "_collapse.fastq"
    else:
        output = output + "_collapse.fasta"

    stats = collapse(args["<fastq>"], output, pseudofq=args["--pseudo-fastq"])

    f = sys.stdout
    for k in ("total_reads", "unique_reads", "unique_content"):
        f.write(f"{k},{stats[k]}\n")
