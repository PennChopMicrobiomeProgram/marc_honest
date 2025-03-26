import argparse
import sys
from marc_honest import __version__
from marc_honest.broker import main as Broker
from marc_honest.db import init as Init
from marc_honest.mock import main as Mock


def main():
    usage_str = "%(prog)s [-h/--help,-v/--version] <subcommand>"
    description_str = (
        "subcommands:\n"
        "  broker       \tIngest a sample list and provide an anonymized output.\n"
        "  init         \tInitialize the database.\n"
        "  mock_db      \tFill mock values into an empty db (for testing).\n"
    )

    parser = argparse.ArgumentParser(
        prog="marc_honest",
        usage=usage_str,
        description=description_str,
        epilog="",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False,
    )

    parser.add_argument("command", help=argparse.SUPPRESS, nargs="?")
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
    )

    args, remaining = parser.parse_known_args()

    if args.command == "broker":
        Broker(remaining)
    elif args.command == "init":
        Init(remaining)
    elif args.command == "mock_db":
        Mock(remaining)
    else:
        parser.print_help()
        sys.stderr.write("Unrecognized command.\n")
