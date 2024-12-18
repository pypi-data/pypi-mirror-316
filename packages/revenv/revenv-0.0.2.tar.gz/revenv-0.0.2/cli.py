import argparse
from revenv.func import reset


def cli_reset(args):
    reset(args.path)


def main():
    # PART create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help="actions")

    # PART create the parser for the "reset" command
    parser_reset = subparsers.add_parser("reset", help="reset a venv")
    parser_reset.add_argument("path", type=str, help="the venv path")
    parser_reset.set_defaults(reset)

    # PART run
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    pass
