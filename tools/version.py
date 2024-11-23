# /// script
# dependencies = [
#   "toml",
# ]
# ///

import argparse

import toml

parser = argparse.ArgumentParser()
parser.add_argument(
    "--version",
    required=False,
    default=False,
    action="store_true",
    help="Get the project version",
)
parser.add_argument(
    "--info",
    required=False,
    default=False,
    action="store_true",
    help="Get the project info",
)
parser.add_argument(
    "--name",
    required=False,
    default=False,
    action="store_true",
    help="Get the project name",
)
args = parser.parse_args()


def get_info() -> None:
    FILE_PATH = "./pyproject.toml"

    with open(FILE_PATH) as f:
        pyproject = toml.load(f)

    if args.version:
        version = pyproject["project"]["version"]
        print(version)
    if args.info:
        info = pyproject["project"]["description"]
        print(info)
    if args.name:
        name = pyproject["project"]["name"]
        print(name)


if __name__ == "__main__":
    get_info()
