========
onomaspy
========


Make inferences about personal names


Description
===========

onomastic` is an algorithm for classifying personal names deterministically, using given and family names lists. `onomastic` tries to minimize misclassifications, and does not make inferences about ambiguous personal names unless forced to do so.


Note
====


.. code-block:: bash

    usage: onomaspy [-h] [-v] [-F FILE] [-o tagged|csv|padded] [-t TRANSLITERATE]
                    [-u UNKNOWN_AS_FAMILY] [-b BREAK_FULL_NAMES]
                    givens_file families_file

    Make inferences about personal names

    positional arguments:
      givens_file           givens filename
      families_file         families filename

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -F FILE, --file FILE  input filename
      -o tagged|csv|padded, --output-format tagged|csv|padded
                            output format. `tagged` by default
      -t TRANSLITERATE, --transliterate TRANSLITERATE
                            transliterate names
      -u UNKNOWN_AS_FAMILY, --unknown-as-family UNKNOWN_AS_FAMILY
                            Treat unknown names as family names
      -b BREAK_FULL_NAMES, --break-full-names BREAK_FULL_NAMES
                            Force split of ambiguous full names
