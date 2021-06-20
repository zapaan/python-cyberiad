import re
from typing import Iterable, Iterator, TextIO

from packaging.requirements import InvalidRequirement, Requirement


def parse_requirements_file(file: TextIO, /) -> Iterator[Requirement]:
    reqs = []
    for line in file:
        line = line.strip()
        # ignore comments and empty lines
        if not line or line.startswith("#"):
            continue
        # remove inline comment
        if " #" in line:
            line = re.sub(r" #.*$", "", line)
        reqs.append(line)
    return parse_requirements(reqs)


def parse_requirements(strings: Iterable[str], /) -> Iterator[Requirement]:
    for s in strings:
        try:
            yield Requirement(s)
        except InvalidRequirement:
            pass
