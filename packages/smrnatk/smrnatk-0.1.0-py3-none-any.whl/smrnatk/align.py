"""
Usage:
    smrnatk-align <fastx> [options]

Options:
    -w PATH --bowtie=PATH         Path to local install of Bowtie
    -f STRING --fastx=STRING      Specify fasta or fastq
    -s PATH --samtools=PATH       Path to local install of Samtools
    -t T --threads=T              Number of threads for Bowtie
    -r STRING --reference=STRING  The reference genome
    -o STRING --output=STRING     Name for bam file output

"""

import os

from docopt import docopt


def mapping(
    bwtie=None, smtools=None, fstx=None, threads=None, ref=None, dat=None, outname=None
):
    """
    The mapping function aligns small RNA data using Bowtie1 with no allowed mismatches,
    multimapping of 200, and best-strata. These settings have been optimized to
    collect the most accurate small RNA isoform data from the fastx.
    """

    # handles fastx alignment
    if fstx == "fasta":
        os.system(
            f"{bwtie} -f --sam -v0 -m 200 --best --strata --threads {threads} {ref} {dat} | {smtools} view -b -o {outname}"  # noqa: E501
        )
    elif fstx == "fastq":
        os.system(
            f"{bwtie} --sam -v0 -m 200 --best --strata --threads {threads} {ref} {dat} | {smtools} view -b -o {outname}"  # noqa: E501
        )


def main(argv=None):
    # read in command line variables
    args = docopt(__doc__, argv=argv)
    args["<fastx>"] = args.get("<fastx>")
    args["--bowtie"] = args.get("--bowtie")
    args["--fastx"] = args.get("--fastx")
    args["--samtools"] = args.get("--samtools")
    args["--threads"] = args.get("--threads")
    args["--reference"] = args.get("--reference")
    args["--output"] = args.get("--output")

    if args["<fastx>"] is None:
        raise Exception("Please specify a valid Fastx file")

    if args["--fastx"] == "fasta" or args["--fastx"] == "fastq":
        pass
    else:
        raise Exception("Please specify either fasta or fastq")

    if args["--bowtie"] is None:
        raise Exception("Please specify a valid path to local Bowtie")

    if args["--samtools"] is None:
        raise Exception("Please specify a valid path to local Samtools")

    # if no threads are specified, make the default 8
    if args["--threads"] is None:
        args["--threads"] = 8
    else:
        args["--threads"] = int(args["--threads"])

    # if no reference is given, raise exception
    if args["--reference"] is None:
        raise Exception("Please specify a valid Bowtie1 reference genome")

    # if no output name is given, create one using data basename
    if args["--output"] is None:
        basename = os.path.splitext(os.path.splitext(args["<fastx>"])[0])[0]
        args["--output"] = basename + ".bam"

    # run the mapping function with the parameters now set
    mapping(
        bwtie=args["--bowtie"],
        fstx=args["--fastx"],
        threads=args["--threads"],
        ref=args["--reference"],
        dat=args["<fastx>"],
        smtools=args["--samtools"],
        outname=args["--output"],
    )
