"""
Main CLI entrypoint.

Copyright 2024 Vlad Emelianov
"""

import sys


def print_info() -> None:
    """
    Print package info to stdout.
    """
    print(
        "Type annotations for aiobotocore ImportExport 2.16.0\n"
        "Version:         2.16.0\n"
        "Builder version: 8.6.4\n"
        "Docs:            https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_importexport//\n"
        "Boto3 docs:      https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/importexport.html#importexport\n"
        "Other services:  https://pypi.org/project/boto3-stubs/\n"
        "Changelog:       https://github.com/youtype/mypy_boto3_builder/releases"
    )


def print_version() -> None:
    """
    Print package version to stdout.
    """
    print("2.16.0")


def main() -> None:
    """
    Main CLI entrypoint.
    """
    if "--version" in sys.argv:
        return print_version()
    print_info()


if __name__ == "__main__":
    main()
