"""Kivy barfs on unknown command line flags, such as those provided to pytest."""

from sys import argv

__clean_args = []  # pylint: disable=invalid-name
for arg in argv[1:]:
    if not "--cov" in arg:
        __clean_args.append(arg)
argv[1:] = __clean_args
