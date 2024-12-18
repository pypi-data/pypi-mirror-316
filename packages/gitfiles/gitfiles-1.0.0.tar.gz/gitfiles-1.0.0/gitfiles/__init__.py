from typing import Iterator, Iterable
import os
import fnmatch

__version__ = "1.0.0"

__ignore_filter__ = None


class IgnoreFilter:
    def __init__(self, path=os.getcwd(), ignore_file=".gitignore"):
        self.path = path
        self.ignore_file = ignore_file
        self.patterns = set([])
        self.__read()

    def match(self, name: str) -> bool:
        name = os.path.relpath(name, self.path)
        for pattern in self.patterns:
            if fnmatch.fnmatch(name, pattern):
                return True
        return False

    def match_case(self, name: str) -> bool:
        name = os.path.relpath(name, self.path)
        for pattern in self.patterns:
            if fnmatch.fnmatchcase(name, pattern):
                return True
        return False

    def filter(self, names: Iterable[str]) -> list[str]:
        return [name for name in names if not self.match(name)]

    def __parse(self, fp: str) -> Iterator[str]:
        with open(fp) as fd:
            for line in fd.readlines():
                if line == "\n" or line.startswith("#"):
                    continue
                yield line.replace("\n", "")

    def __read(self):
        for dir, dirs, files in os.walk(os.getcwd()):
            for file in files:
                if file.endswith(self.ignore_file):
                    fp = os.path.join(dir, file)
                    for pattern in self.__parse(fp):
                        p = os.path.relpath(dir + os.path.sep + pattern, self.path)
                        self.patterns.add(p)


def load_gitignore() -> None:
    """
    Load all .gitignore files in working directory.
    """
    global __ignore_filter__
    __ignore_filter__ = IgnoreFilter()


def match(name: str) -> bool:
    """
    Test whether FILENAME matches pattern in .gitignore.
    """
    return __ignore_filter__.match(name)


def match_case(name: str) -> bool:
    """
    Test whether FILENAME matches pattern in .gitignore, including case.
    """
    return __ignore_filter__.match_case(name)


def filter(names: Iterable[str]) -> list[str]:
    """
    Construct a list from those elements of the iterable NAMES that match pattern in .gitignore.

    :param names: A list of path names.
    :type names: Iterable[str]
    :return: A filtered list of valid path names.
    :rtype: list[str]
    """
    return __ignore_filter__.filter(names)
