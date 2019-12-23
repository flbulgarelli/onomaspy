# -*- coding: utf-8 -*-
"""
Then run `python setup.py install` which will install the command `fibonacci`
inside your current environment.
also be used as template for Python modules.

Note: This skeleton file can be safely removed if not needed!
"""

import argparse
import sys
import logging

from onomaspy import __version__
from onomaspy import *

__author__ = "Franco Bulgarelli"
__copyright__ = "Franco Bulgarelli"
__license__ = "gpl3"

def parse_args(args):
  """Parse command line parameters

  Args:
    args ([str]): command line parameters as list of strings

  Returns:
    :obj:`argparse.Namespace`: command line parameters namespace
  """
  parser = argparse.ArgumentParser(
      description="Deterministic classifier for personal names")
  parser.add_argument(
      "givens_file",
      help="givens filename",
      type=str)
  parser.add_argument(
      "families_file",
      help="families filename",
      type=str)
  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version="onomaspy {ver}".format(ver=__version__))
  parser.add_argument(
      "-F",
      "--file",
      dest="input_file",
      help="input filename",
      type=str,
      default="--",
      metavar="FILE")
  parser.add_argument(
      "-o",
      "--output-format",
      dest="output_format",
      help="output format. `tagged` by default",
      type=str,
      default="tagged",
      metavar="tagged|csv|padded")
  parser.add_argument(
      "-t",
      "--transliterate",
      dest="transliterate",
      help="transliterate names",
      type=bool)
  parser.add_argument(
      "-u",
      "--unknown-as-family",
      dest="unknown_as_family",
      help="Treat unknown names as family names",
      type=bool)
  parser.add_argument(
      "-b",
      "--break-full-names",
      dest="break_full_names",
      help="Force split of ambiguous full names",
      type=bool)
  return parser.parse_args(args)

def read_lines(path):
  with open(path) as f:
    return map(lambda l:l.strip(), f.readlines())

def select_divider(break_names):
  return BreakNames() if break_names else NameSplitter()

def format_name(format, name):
  return name
# selectFormat :: String -> Format
# selectFormat "tagged" = tagged
# selectFormat "csv"    = csv
# selectFormat _        = padded


# tagged :: Format
# tagged (FullName names)       = "FullName:" ++ intercalate " " names
# tagged (GivenAndFamily gs fs) = "GivenAndFamily:" ++ intercalate " " gs ++ "," ++ intercalate " " fs

# csv :: Format
# csv (FullName names)       = intercalate " " names
# csv (GivenAndFamily gs fs) = intercalate " " gs ++ "," ++ intercalate " " fs

# padded :: Format
# padded (FullName names)       = ",," ++ intercalate " " names
# padded (GivenAndFamily gs fs) = intercalate " " gs ++ "," ++ intercalate " " fs


def process_line(registry, format, divider, line):
  print(format_name(format, line_to_name(line).fix(registry, divider)))

def line_to_name(line):
  return FullName(prepare(line))

def prepare(line):
  return list(
          filter(lambda l: l,
            map(lambda l: l.strip().title(),
              line.replace(",", "").split(" "))))

def main(args):
  """Main entry point allowing external calls

  Args:
    args ([str]): command line parameter list
  """
  args = parse_args(args)

  givens = read_lines(args.givens_file)
  familes = read_lines(args.families_file)

  options = RegistryOptions(transliterate_names = args.transliterate, treat_unknown_as_family = args.unknown_as_family)
  registry = Registry.make(givens, familes, options)
  contents = sys.stdin.readlines() if args.input_file == "--" else read_lines(args.input_file)

  for line in contents:
    process_line(registry, args.output_format, select_divider(args.break_full_names), line)

def run():
  """Entry point for console_scripts
  """
  main(sys.argv[1:])


if __name__ == "__main__":
  run()



