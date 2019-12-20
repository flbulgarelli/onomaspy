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

__author__ = "Franco Bulgarelli"
__copyright__ = "Franco Bulgarelli"
__license__ = "gpl3"




# Available options:
#   -b,--break-full-names    Force split of ambiguous full names


def parse_args(args):
  """Parse command line parameters

  Args:
    args ([str]): command line parameters as list of strings

  Returns:
    :obj:`argparse.Namespace`: command line parameters namespace
  """
  parser = argparse.ArgumentParser(
      description="Make inferences about personal names")
  parser.add_argument(
      "-v",
      "--version",
      action="version",
      version="onomaspy {ver}".format(ver=__version__))
  parser.add_argument(
      "-g",
      "--givens",
      dest="givens_file",
      help="givens filename",
      type=str,
      metavar="FILE")
  parser.add_argument(
      "-f",
      "--families",
      dest="families_file",
      help="families filename",
      type=str,
      metavar="FILE")
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
  return parser.parse_args(args)

def read_lines(path):
  with open(path) as f:
    return f.readlines()

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
  contents = sys.stdin.readlines() if args.file == "--" else read_lines(args.file)


  # print("The {}-th Fibonacci number is {}".format(args.n, fib(args.n)))


def run():
  """Entry point for console_scripts
  """
  main(sys.argv[1:])


if __name__ == "__main__":
  run()


 # for_ (lines contents) (processLine registry (selectFormat outputFormat) (selectDivider breakFullNames))
# selectDivider :: Bool -> NameDivider
# selectDivider False = splitNames
# selectDivider _     = justBreakNames

# processLine :: Registry -> Format ->  NameDivider -> String -> IO ()
# processLine registry format divider = putStrLn  . format . fix registry divider . FullName . map unpack . prepare . pack

# type Format = PersonalName -> String

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

# prepare :: Text -> [Text]
# prepare = filter (not . T.null) . map (toTitle . strip) . splitOn " " . replace "," " "
