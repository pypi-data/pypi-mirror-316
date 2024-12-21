"""
Usage:
    smrnatk quality_parse  [options] <args...>
    smrnatk collapse [options] <args...>
    smrnatk collate [options] <args...>
    smrnatk align [options] <args...>
    smrnatk filter [options] <args...>

"""

import sys

from docopt import docopt


def main(argv=sys.argv):
    cmds = "quality_parse", "collapse", "align"

    if len(argv) < 2 or (len(argv) > 1 and argv[1] not in cmds):
        docopt(__doc__)
    cmd = argv[1]

    # the individual main methods expect an executable of the form
    # smrnatk-<mode>, but here the smrnatk and mode come as separate arguments
    # concatenate them together and pass them on
    cli_args = ["-".join(argv[:2])] + argv[2:]

    if cmd == "quality_parse":
        from .quality_parse import main

        main(cli_args)
    elif cmd == "collapse":
        from .collapse import main

        main(cli_args)
    elif cmd == "collate":
        from .collate import main

        main(cli_args)
    elif cmd == "align":
        from .align import main

        main(cli_args)
    elif cmd == "filter":
        from .filter_fasta import main

        main(cli_args)
    elif cmd == "help":
        docopt(__doc__, ["-h"])


if __name__ == "__main__":
    main()
