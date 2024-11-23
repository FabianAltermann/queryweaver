# /// script
# dependencies = [
#   "toml",
# ]
# ///

import argparse
import logging
import re
from typing import Literal

import toml

parser = argparse.ArgumentParser()
parser.add_argument(
    "part",
    nargs="?",
    type=str,
    choices=["major", "minor", "patch"],
    default="patch",
    help="Part of the version to bump",
)
parser.add_argument(
    "--suffix",
    required=False,
    nargs="?",
    type=str,
    default="",
    help="Suffix to append to the version",
)

args = parser.parse_args()

ALLOWED_SUFFIXES = ["dev", "rc", r"a(lpha)?", r"b(eta)?", "post", r"pre(view)?"]
suffix_pattern = re.compile(
    rf"({'|'.join(ALLOWED_SUFFIXES)}).?\d*", flags=re.IGNORECASE
)


def bump_version(
    part: Literal["major", "minor", "patch"] = "patch",
    suffix: str = "",
) -> None:
    FILE_PATH = "./pyproject.toml"

    with open(FILE_PATH) as f:
        pyproject = toml.load(f)

    version = pyproject["project"]["version"]

    major, minor, patch, *_ = re.split(r"[.-]", version)
    major, minor, patch = map(int, [major, minor, patch])

    if part == "major":
        major += 1
        minor = 0
        patch = 0
    elif part == "minor":
        minor += 1
        patch = 0
    elif part == "patch":
        patch += 1
    else:
        raise ValueError("Invalid part value. Choose 'major', 'minor', or 'patch'.")

    new_version = f"{major}.{minor}.{patch}"
    if suffix:
        if not re.fullmatch(suffix_pattern, suffix):
            raise ValueError(f"Invalid suffix. Choose {ALLOWED_SUFFIXES}.")
        new_version += f"-{suffix.lower()}"

    pyproject["project"]["version"] = new_version

    with open(FILE_PATH, "w") as f:
        toml.dump(pyproject, f)

    logging.info(f"Version bumped to {new_version}")


if __name__ == "__main__":
    bump_version(part=args.part, suffix=args.suffix)
