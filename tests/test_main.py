# -*- coding: utf-8 -*-

import pytest
from onomaspy.main import main

def test_main_help():
  with pytest.raises(SystemExit):
    main(["-h"])


def test_main_ok(capsys):
  main(["tests/data/givens.txt", "tests/data/families.txt", "-F", "tests/data/names.txt"])
  assert "GivenAndFamily(['Masculas'], ['Herrera'])" in capsys.readouterr().out

