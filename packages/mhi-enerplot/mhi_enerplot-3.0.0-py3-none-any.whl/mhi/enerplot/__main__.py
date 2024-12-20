"""
Enerplot Automation Library - main
"""

from argparse import ArgumentParser, Namespace
from pathlib import Path

import mhi.common
from mhi.common.help import HelpCommand
from mhi.enerplot import VERSION
from mhi.enerplot.buildtime import BUILD_TIME


def version(args: Namespace):                  # pylint: disable=unused-argument
    """Display package version info"""

    print(f"MHI Enerplot Library v{VERSION} ({BUILD_TIME})")
    print("(c) Manitoba Hydro International Ltd.")
    print()
    print(mhi.common.version_msg())


def main():
    """Main: Command Line Interface"""

    parser = ArgumentParser(prog='py -m mhi.enerplot')
    parser.set_defaults(func=version)
    subparsers = parser.add_subparsers()

    help_cmd = HelpCommand(Path(__file__).parent / 'Enerplot_AL_doc.chm')
    help_cmd.add_subparser(subparsers)

    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
