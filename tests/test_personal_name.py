# -*- coding: utf-8 -*-

import pytest

from onomaspy import *

names = [
  "Franco",
  "Leonardo",
  "Agustín",
  "Federico",
  "Alfredo",
  "Laura",
  "Mónica",
  "Judith",
  "Nadia",
  "Giselle",
  "Julián",
  "Luis",
  "Tomás",
  "Rocío",
  "Carolina",
  "Luisa",
  "Gustavo",
  "Ernesto",
  "Ivana",
  "Daniela",
  "Felipe",
  "Andres",
  "Daniela",
  "Veronica",
  "Rodrigo",
  "Alfonso"
]

surnames = [
  "Bulgarelli",
  "Pina",
  "Scarpa",
  "Mangifesta",
  "Gruszczanski",
  "Finzi",
  "Berbel",
  "Alt",
  "Cannavó",
  "Gonzalez",
  "Baldino",
  "Trucco",
  "Feldfeber",
  "Kivelsky",
  "Szklanny",
  "Calvo",
  "Villani",
  "Alfonso",
  "Rodrigo"
]

sample_registry = Registry.make(names, surnames, RegistryOptions(transliterate_names = True))

def run(personal_name, families_greedy = False):
  return personal_name.fix(sample_registry, NameBreaker(families_greedy))

def try_run(personal_name, families_greedy = False):
  return personal_name.try_fix(sample_registry, NameSplitter(families_greedy))

def test_N_S():
  assert run(GivenAndFamily(["Rocío"], ["Gonzalez"])) == GivenAndFamily(["Rocío"], ["Gonzalez"])

def test_S_N():
  assert run(GivenAndFamily(["Calvo"], ["Felipe"])) == GivenAndFamily(["Felipe"], ["Calvo"])

def test_NN_S():
  assert run(GivenAndFamily(["Federico", "Alfredo"], ["Scarpa"])) == GivenAndFamily(["Federico", "Alfredo"], ["Scarpa"])
def test_S_NN():
  assert run(GivenAndFamily(["Scarpa"], ["Federico", "Alfredo"])) == GivenAndFamily(["Federico", "Alfredo"], ["Scarpa"])

def test_N_SS():
  assert run(GivenAndFamily(["Ivana"], ["Feldfeber", "Kivelsky"])) == GivenAndFamily(["Ivana"], ["Feldfeber", "Kivelsky"])
def test_SS_N():
  assert run(GivenAndFamily(["Feldfeber", "Kivelsky"], ["Ivana"])) == GivenAndFamily(["Ivana"], ["Feldfeber", "Kivelsky"])

def test_try_S_S():
  assert try_run(GivenAndFamily(["Bulgarelli"], ["Alt"])) == None

def test_try_N_N():
  assert try_run(GivenAndFamily(["Laura"], ["Giselle"])) == None

def test_A_A():
  assert run(GivenAndFamily(["Rodrigo"], ["Alfonso"])) == GivenAndFamily(["Rodrigo"], ["Alfonso"])
def test_A_A():
  assert run(GivenAndFamily(["Alfonso"], ["Rodrigo"])) == GivenAndFamily(["Alfonso"], ["Rodrigo"])

def test_A_AS():
  assert run(GivenAndFamily(["Alfonso"], ["Rodrigo", "Trucco"])) == GivenAndFamily(["Alfonso"], ["Rodrigo", "Trucco"])

def test_AS_A():
  assert run(GivenAndFamily(["Rodrigo", "Trucco"], ["Alfonso"])) == GivenAndFamily(["Alfonso"], ["Rodrigo", "Trucco"])

def test_A_SA():
  assert run(GivenAndFamily(["Alfonso"], ["Pina", "Rodrigo"])) == GivenAndFamily(["Alfonso"], ["Pina", "Rodrigo"])

def test_SA_A():
  assert run(GivenAndFamily(["Pina", "Rodrigo"], ["Alfonso"])) == GivenAndFamily(["Alfonso"], ["Pina", "Rodrigo"])

def test_AN_AS():
  assert run(GivenAndFamily(["Alfonso", "Julián"], ["Rodrigo", "Trucco"])) == GivenAndFamily(["Alfonso", "Julián"], ["Rodrigo", "Trucco"])

def test_AS_AN():
  assert run(GivenAndFamily(["Rodrigo", "Trucco"], ["Alfonso", "Julián"])) == GivenAndFamily(["Alfonso", "Julián"], ["Rodrigo", "Trucco"])

def test_NA_SA():
  assert run(GivenAndFamily(["Leonardo", "Alfonso"], ["Finzi", "Rodrigo"])) == GivenAndFamily(["Leonardo", "Alfonso"], ["Finzi", "Rodrigo"])

def test_SA_NA():
  assert run(GivenAndFamily(["Finzi", "Rodrigo"], ["Leonardo", "Alfonso"])) == GivenAndFamily(["Leonardo", "Alfonso"], ["Finzi", "Rodrigo"])

def test_A_SS():
  assert run(GivenAndFamily(["Alfonso"], ["Villani", "Trucco"])) == GivenAndFamily(["Alfonso"], ["Villani", "Trucco"])

def test_SS_A():
  assert run(GivenAndFamily(["Villani", "Trucco"], ["Alfonso"])) == GivenAndFamily(["Alfonso"], ["Villani", "Trucco"])

def test_NN_AS():
  assert run(GivenAndFamily(["Nadia", "Rocío"], ["Rodrigo", "Trucco"])) == GivenAndFamily(["Nadia", "Rocío"], ["Rodrigo", "Trucco"])

def test_AS_NN():
  assert run(GivenAndFamily(["Rodrigo", "Trucco"], ["Nadia", "Rocío"])) == GivenAndFamily(["Nadia", "Rocío"], ["Rodrigo", "Trucco"])

def test_nn_s():
  assert run(GivenAndFamily(["carolina", "veronica"], ["gruszczanski"])) == GivenAndFamily(["carolina", "veronica"], ["gruszczanski"])

def test_s_nn():
  assert run(GivenAndFamily(["gruszczanski"], ["carolina", "veronica"])) == GivenAndFamily(["carolina", "veronica"], ["gruszczanski"])

def test_Ń_Ś():
  assert run(GivenAndFamily(["Monica"], ["Cannavo"])) == GivenAndFamily(["Monica"], ["Cannavo"])

def test_Ś_Ń():
  assert run(GivenAndFamily(["Cannavo"], ["Monica"])) == GivenAndFamily(["Monica"], ["Cannavo"])

def test_NS():
  assert run(FullName(["Rocío", "Gonzalez"])) == GivenAndFamily(["Rocío"], ["Gonzalez"])
def test_SN():
  assert run(FullName(["Calvo", "Felipe"])) == GivenAndFamily(["Felipe"], ["Calvo"])

def test_NNS():
  assert run(FullName(["Federico", "Alfredo", "Scarpa"])) == GivenAndFamily(["Federico", "Alfredo"], ["Scarpa"])
def test_SNN():
  assert run(FullName(["Scarpa", "Federico", "Alfredo"])) == GivenAndFamily(["Federico", "Alfredo"], ["Scarpa"])

def test_NSS():
  assert run(FullName(["Ivana", "Feldfeber", "Kivelsky"])) == GivenAndFamily(["Ivana"], ["Feldfeber", "Kivelsky"])
def test_SSN():
  assert run(FullName(["Feldfeber", "Kivelsky", "Ivana"])) == GivenAndFamily(["Ivana"], ["Feldfeber", "Kivelsky"])

def test_try_SS():
  assert try_run(FullName(["Bulgarelli", "Alt"])) == None

def test_NN():
  assert try_run(FullName(["Laura", "Giselle"])) == None

def test_AA():
  assert run(FullName(["Rodrigo", "Alfonso"])) == GivenAndFamily(["Rodrigo"], ["Alfonso"])
def test_AA():
  assert run(FullName(["Alfonso", "Rodrigo"])) == GivenAndFamily(["Alfonso"], ["Rodrigo"])

def test_AAS():
  assert run(FullName(["Alfonso", "Rodrigo", "Trucco"])) == GivenAndFamily(["Alfonso", "Rodrigo"], ["Trucco"])

def test_ASA():
  assert run(FullName(["Rodrigo", "Trucco", "Alfonso"])) == GivenAndFamily(["Alfonso"], ["Rodrigo", "Trucco"])

def test_ASA():
  assert run(FullName(["Rodrigo", "Trucco", "Alfonso"]), families_greedy = True) == GivenAndFamily(["Rodrigo"], ["Trucco", "Alfonso"])

def test_SAA():
  assert run(FullName(["Pina", "Rodrigo", "Alfonso"])) == GivenAndFamily(["Alfonso"], ["Pina", "Rodrigo"])

def test_ANAS():
  assert run(FullName(["Alfonso", "Julián", "Rodrigo", "Trucco"])) == GivenAndFamily(["Alfonso", "Julián", "Rodrigo"], ["Trucco"])

def test_ASAN():
  assert run(FullName(["Rodrigo", "Trucco", "Alfonso", "Julián"])) == GivenAndFamily(["Julián"], ["Rodrigo", "Trucco", "Alfonso"])

def test_NASA():
  assert run(FullName(["Leonardo", "Alfonso", "Finzi", "Rodrigo"])) == GivenAndFamily(["Leonardo", "Alfonso"], ["Finzi", "Rodrigo"])

def test_SANA():
  assert run(FullName(["Finzi", "Rodrigo", "Leonardo", "Alfonso"])) == GivenAndFamily(["Leonardo", "Alfonso"], ["Finzi", "Rodrigo"])

def test_SANA_greedy():
  assert run(FullName(["Finzi", "Rodrigo", "Leonardo", "Alfonso"]), families_greedy = True) == GivenAndFamily(["Rodrigo", "Leonardo", "Alfonso"], ["Finzi"])

def test_try_ANAS():
  assert try_run(FullName(["Alfonso", "Julián", "Rodrigo", "Trucco"])) == None

def test_try_ASAN():
  assert try_run(FullName(["Rodrigo", "Trucco", "Alfonso", "Julián"])) == None

def test_try_ANSAS():
  assert try_run(FullName(["Alfonso", "Julián", "Berbel", "Rodrigo", "Trucco"])) == (GivenAndFamily(["Alfonso","Julián"], ["Berbel","Rodrigo","Trucco"]))

def test_try_ASNAN():
  assert try_run(FullName(["Rodrigo", "Trucco", "Luis", "Alfonso", "Julián"])) == (GivenAndFamily(["Luis", "Alfonso","Julián"], ["Rodrigo","Trucco"]))

def test_try_NASA():
  assert try_run(FullName(["Leonardo", "Alfonso", "Finzi", "Rodrigo"])) == None

def test_try_SANA():
  assert try_run(FullName(["Finzi", "Rodrigo", "Leonardo", "Alfonso"])) == None

def test_ASS():
  assert run(FullName(["Alfonso", "Villani", "Trucco"])) == GivenAndFamily(["Alfonso"], ["Villani", "Trucco"])

def test_SSA():
  assert run(FullName(["Villani", "Trucco", "Alfonso"])) == GivenAndFamily(["Alfonso"], ["Villani", "Trucco"])

def test_NNAS():
  assert run(FullName(["Nadia", "Rocío", "Rodrigo", "Trucco"])) == GivenAndFamily(["Nadia", "Rocío", "Rodrigo"], ["Trucco"])

def test_NNAS_greedy():
  assert run(FullName(["Nadia", "Rocío", "Rodrigo", "Trucco"]), families_greedy = True) == GivenAndFamily(["Nadia", "Rocío"], ["Rodrigo", "Trucco"])

def test_ASNN():
  assert run(FullName(["Rodrigo", "Trucco", "Nadia", "Rocío"])) == GivenAndFamily(["Nadia", "Rocío"], ["Rodrigo", "Trucco"])

def test_N():
  assert run(FullName(["Nadia"])) == FullName(["Nadia"])
