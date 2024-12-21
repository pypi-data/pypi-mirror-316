"""
Usage:
    smrnatk-quality_parse quality_report <fastq> [options]
    smrnatk-quality_parse quality_filter <fastq> [options]

Options:

    -b FILE --basename=FILE       Basename of the ouput csv
    -p INT --phred-threshold=INT  Phred value threshold
    -a INT --bp-allowance=INT     quality_filter: Number of bases allowed to
                                  have sub-threshold Phred value


"""

import collections
import json
import os
import sys

import numpy as np
import pandas as pd
import pysam
from docopt import docopt

# TODO(labadorf, 2024-12-20): the quality report code assumes Phred33, should be configurable
def convert_phred(qual):
    """
    The convert_phred function converts the ASCII_Base=33 Phred score to the Q
    score value.
    """

    # convert from ASCII to quality value
    answer = [ord(_) - 33 for _ in qual]
    return answer


def quality_report(dat, phred=None, output=None):
    """
    The quality_report function parses the per-read quality of fastq files. If
    given a specific Phred score, the function will return a table. The table
    index is the number of bases allowed to have a sub-theshold Phred score and
    the table values are the cumulative sums of the percentage of reads that
    fall into that bin. If no Phred score is specified, the same output is
    given but with the three columns representing a Phred threshold of 10, 20,
    and 30, respectively.
    """

    results_dict_default = collections.OrderedDict({10: {}, 20: {}, 30: {}})
    results_dict_user = collections.OrderedDict()
    total_reads = 0

    # parse the fastq file and collect the quality data
    with pysam.FastqFile(dat) as ff:
        for entry in ff:
            if len(entry.sequence) != 0:
                total_reads += 1
                qvals = convert_phred(entry.quality)

            # if user does not define a specific Phred score, use 10, 20, and 30
            if phred is None:
                total_bad_10 = sum(i < 10 for i in qvals)
                total_bad_20 = sum(i < 20 for i in qvals)
                total_bad_30 = sum(i < 30 for i in qvals)

                if total_bad_10 in results_dict_default[10]:
                    results_dict_default[10][total_bad_10] += 1
                else:
                    results_dict_default[10][total_bad_10] = 1

                if total_bad_20 in results_dict_default[20]:
                    results_dict_default[20][total_bad_20] += 1
                else:
                    results_dict_default[20][total_bad_20] = 1

                if total_bad_30 in results_dict_default[30]:
                    results_dict_default[30][total_bad_30] += 1
                else:
                    results_dict_default[30][total_bad_30] = 1

            # else if user does specify a Phred score
            if phred is not None:
                user_bad = sum(i < phred for i in qvals)

                if user_bad not in results_dict_user:
                    results_dict_user[user_bad] = 1
                else:
                    results_dict_user[user_bad] += 1

    # if no phred indicated, output default [10,20,30]
    if phred is None:
        results = results_dict_default
        results_df = pd.DataFrame.from_dict(results)
        results_df.fillna(0, inplace=True)
        results_df = results_df / total_reads
    # else output indicated phred
    else:
        results = results_dict_user
        results_df = pd.DataFrame.from_dict(results, orient="index")
        results_df.sort_index(inplace=True)
        results_df.rename({0: phred}, axis="columns", inplace=True)
        results_df = results_df / total_reads

    # format the data to be cumulative sum
    results_df = round(np.cumsum(results_df), 3)

    phred = "[10,20,30]" if phred is None else f"[{phred}]"

    if output is None:
        basename = os.path.splitext(os.path.splitext(dat)[0])[0]
        output_fn = basename + "_quality_report.json"
    elif output is not None:
        output_fn = output + "_quality_report.json"

    with open(output_fn, "w") as outfile:
        json.dump(
            {
                "Version": 0.1,
                "Type": "Cumulative Table",
                "Phred": phred,
                "Report": results_df.values.tolist(),
            },
            outfile,
            indent=4,
        )
    outfile.close()

    return results_df


def quality_filter(dat, bp, phred, output=None):
    """
    The quality_filter function filters reads based on the specified Phred
    threshold and base pair allowance, returning a filtered fastq.
    """

    total_reads = 0
    poor_reads = 0

    # handle output file logic for both the fastq and the json
    if output is None:
        basename = os.path.splitext(os.path.splitext(dat)[0])[0]
        filter_output = basename + "_filtered.fastq"
        output_fn = basename + "_quality_filter.json"
    elif output is not None:
        filter_output = output + "_filtered.fastq"
        output_fn = output + "_quality_filter.json"

    # filter the reads and output to a new fastq file
    with pysam.FastxFile(dat) as ff, open(filter_output, "w") as myfile:
        for entry in ff:
            if len(entry.sequence) != 0:  # some empty sequences in SRR files
                # counter to track total reads in file
                total_reads += 1

                qvals = convert_phred(entry.quality)

                under_phred = sum(i < phred for i in qvals)

                if under_phred > bp:
                    poor_reads += 1

                if under_phred <= bp:
                    myfile.write(str(entry) + "\n")
    myfile.close()

    # get fraction of good reads
    good_reads = round(((total_reads - poor_reads) / total_reads), 4)

    results = {
        "total_reads:": total_reads,
        "poor_quality_reads": poor_reads,
        "frac_high_quality_reads": good_reads,
        "phred_threshold:": phred,
        "base_pair_allowance": bp,
    }

    # put the filtering stats in a df for stdout
    results_stats = pd.DataFrame.from_dict(results, orient="index", columns=["results"])

    with open(output_fn, "w") as outfile:
        json.dump(results, outfile, indent=4)
    outfile.close()

    return results_stats


def main(argv=None):
    # read in command line variables
    args = docopt(__doc__, argv=argv)
    args["<fastq>"] = args.get("<fastq>")
    args["--basename"] = args.get("--basename")
    args["--phred-threshold"] = args.get("--phred-threshold")
    args["--bp-allowance"] = args.get("--bp-allowance")

    # ensure variables are the correct datatype
    prd = (
        int(args["--phred-threshold"])
        if args["--phred-threshold"] is not None
        else None
    )
    bpallow = (
        int(args["--bp-allowance"]) if args["--bp-allowance"] is not None else None
    )

    # handles quality_report output
    if args["quality_report"]:
        report = quality_report(args["<fastq>"], phred=prd, output=args["--basename"])

        f = sys.stdout
        report.to_csv(f, sep="\t")

    # handles quality_filter output
    elif args["quality_filter"]:
        # Sets default Phred threshold and bp-allowance if none supplied
        if prd is None:
            prd = 13
        if bpallow is None:
            bpallow = 3

        filtering_stats = quality_filter(
            args["<fastq>"], bpallow, prd, output=args["--basename"]
        )

        f = sys.stdout
        filtering_stats.to_csv(f, sep="\t")
