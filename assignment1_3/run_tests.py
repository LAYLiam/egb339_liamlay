#!/usr/bin/env python

import os
import sys

import pytest


def pytest_args(argv: list[str]) -> list[str]:
    if not argv:
        return ["-k", "not test_submitted_files", "."]

    question = argv[0].lower()
    rest = argv[1:]
    if question == "all":
        return ["-k", "not test_submitted_files", ".", *rest]

    question = question.removeprefix("q")
    if question.isdigit():
        question = str(int(question))
        return [".", "-k", f"question_{question}_", *rest]

    return [".", *argv]


if __name__ == "__main__":
    # Change to directory of this file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    pytest.main(pytest_args(sys.argv[1:]))
