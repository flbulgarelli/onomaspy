# -*- coding: utf-8 -*-

import pytest
from onomaspy.skeleton import fib

__author__ = "Franco Bulgarelli"
__copyright__ = "Franco Bulgarelli"
__license__ = "gpl3"

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

class Registry:
  def __init__(self, givens, families, ambiguous, options):
      self.givens = givens
      self.families = families
      self.ambiguous = ambiguous
      self.options = options

  @staticmethod
  def make(givens, families, options):
    givens_set = set(options.encode_many(givens))
    families_set = set(options.encode_many(families))
    ambiguous = givens_set.intersection(families_set)
    return Registry(givens_set - ambiguous, families_set - ambiguous, ambiguous, options)

  def registered_as_given(self, n):
    return n in self.givens

  def registered_as_family(self, n):
    return n in self.families

  def registered_as_ambiguous(self, n):
    return n in self.ambiguous

  def classify(self, n):
    en = self.options.encode(n)

    if self.registered_as_given(en):
      return Class.GIVEN

    if self.registered_as_family(en):
      return Class.FAMILY

    if self.registered_as_ambiguous(en):
      return Class.OTHER

    if self.options.treat_unknown_as_family:
      return Class.FAMILY

    return Class.OTHER

  def classify_many(self, ns):
    return Class.merge(maplist(lambda n: self.classify(n), ns))

import unidecode

class RegistryOptions:
  def __init__(self, transliterate_names = False, treat_unknown_as_family = False):
    self.transliterate_names = transliterate_names
    self.treat_unknown_as_family = treat_unknown_as_family

  def encode(self, n):
    return (unidecode.unidecode(n) if self.transliterate_names else n).lower()

  def encode_many(self, ns):
    return set(map(lambda n: self.encode(n), ns))

class PersonalName:
  def fix(self, registry, divider):
    result = self.try_fix(registry, divider)
    return result if result else self

  def try_fix(self, registry, divider):
    if not self.valid():
      return None

    result = self.analyze(registry, divider)
    return PersonalName.make(result) if result else None


  @staticmethod
  def make(pair):
    first, second = pair
    first_class = first.klass
    second_class = second.klass

    if ((first_class, second_class) == (Class.GIVEN, Class.GIVEN) or
        (first_class, second_class) == (Class.FAMILY, Class.FAMILY) or
        first_class == Class.BAD or
        second_class == Class.BAD):
      return None

    if first_class == Class.FAMILY or second_class == Class.GIVEN:
      return GivenAndFamily(second.value, first.value)

    return GivenAndFamily(first.value, second.value)


class GivenAndFamily(PersonalName):
  def __init__(self, givens, families):
    self.givens = givens
    self.families = families

  def as_tuple(self):
    return (self.givens, self.families)

  def __hash__(self):
    return hash(self.as_tuple())

  def __eq__(self, other):
      return self.__class__ == other.__class__ and self.as_tuple() == other.as_tuple()

  def analyze(self, registry, divider):
    return (Name.make(registry, self.givens), Name.make(registry, self.families))

  def valid(self):
    return self.givens and self.families

  def __repr__(self):
    return 'GivenAndFamily(%s, %s)' % (self.givens, self.families)


class FullName(PersonalName):
  def __init__(self, names):
    self.names = names

  def __hash__(self):
    return hash(self.names)

  def __eq__(self, other):
      return self.__class__ == other.__class__ and self.names == other.names

  def analyze(self, registry, divider):
    return divider.try_divide(list(map(lambda n: Name.make_singleton(registry, n), self.names)))

  def valid(self):
    return len(self.names) > 1

from enum import Enum

class Class(Enum):
  GIVEN = 1
  FAMILY = 2
  OTHER = 3
  BAD = 4

  def is_givenish(self):
    return self == Class.GIVEN or self == Class.OTHER

  def is_familish(self):
    return self == Class.FAMILY or self == Class.OTHER

  @staticmethod
  def merge(classes):
    if len(classes) == 1:
      return classes[0]

    if classes[0] == Class.GIVEN and all(x.is_givenish() for x in classes[1:]):
      return Class.GIVEN

    if classes[0] == Class.FAMILY and all(x.is_familish() for x in classes[1:]):
      return Class.FAMILY

    if classes[0] == Class.OTHER:
      return Class.merge(classes[1:])

    return Class.BAD

  @staticmethod
  def confidence(pair):
    if pair == (Class.GIVEN, Class.FAMILY):
      return 8
    if pair == (Class.FAMILY, Class.GIVEN):
      return 8
    if pair == (Class.FAMILY, Class.OTHER):
      return 7
    if pair == (Class.OTHER, Class.FAMILY):
      return 7
    if pair == (Class.GIVEN, Class.OTHER):
      return 6
    if pair == (Class.OTHER, Class.GIVEN):
      return 6
    if pair == (Class.OTHER, Class.OTHER):
      return 5
    if pair == (Class.FAMILY, Class.FAMILY):
      return 4
    if pair == (Class.GIVEN, Class.GIVEN):
      return 4
    if pair == (Class.BAD, Class.FAMILY):
      return 3
    if pair == (Class.FAMILY, Class.BAD):
      return 3
    if pair == (Class.BAD, Class.GIVEN):
      return 2
    if pair == (Class.GIVEN, Class.BAD):
      return 2
    if pair == (Class.BAD, Class.OTHER):
      return 1
    if pair == (Class.OTHER, Class.BAD):
      return 1
    if pair == (Class.BAD, Class.BAD):
      return 0

  @staticmethod
  def ambiguous_center(classes):
    if classes[0] == Class.OTHER:
      return Class.ambiguous_center(classes[1:])

    if classes[0] == Class.GIVEN:
      return Class.ambiguous_given_center(False, classes[1:])

    if classes[0] == Class.FAMILY:
      return Class.ambiguous_family_center(False, classes[1:])

    return False

  @staticmethod
  def ambiguous_given_center(found, classes):
    if not classes:
      return False

    if classes[0] == Class.GIVEN:
      return Class.ambiguous_given_center(False, classes[1:])

    if classes[0] == Class.FAMILY:
      return found

    if classes[0] == Class.OTHER:
      return Class.ambiguous_given_center(True, classes[1:])

    return False

  @staticmethod
  def ambiguous_family_center(found, classes):
    if not classes:
      return False

    if classes[0] == Class.FAMILY:
      return Class.ambiguous_family_center(False, classes[1:])

    if classes[0] == Class.GIVEN:
      return found

    if classes[0] == Class.OTHER:
      return Class.ambiguous_family_center(True, classes[1:])

    return False


def flatmap(f, xss):
  return flatten(map(f, xss))

def flatten(xss):
  return [x for y in xss for x in y]

def partitions(xss):
  return [(xss[:i], xss[i:]) for i in range(1, len(xss))]

def maplist(f, xs):
  return list(map(f, xs))

class Name:
  def __init__(self, value, klass):
    self.value = value
    self.klass = klass


  def __repr__(self):
    return 'Name(%s, %s)' % (self.value, self.klass)

  @staticmethod
  def merge(ns):
    return Name(
      list(flatmap(lambda n: n.value, ns)),
      Class.merge(maplist(lambda n:n.klass, ns)))

  @staticmethod
  def confidence(pair):
    return Class.confidence((pair[0].klass, pair[1].klass))

  @staticmethod
  def make(registry, ns):
    return Name(ns, registry.classify_many(ns))

  @staticmethod
  def make_singleton(registry, n):
    return Name([n], registry.classify(n))

class NameDivider:
  def __init__(self, families_greedy = False):
    self.families_greedy = families_greedy

  def try_divide(self, names):
    return None if self.atomic(names) else self.divide(names)

  def divide(self, names):
    divisions = self.divisions(names)

    if not self.families_greedy:
      divisions = list(divisions)
      divisions.reverse()

    return max(divisions, key = lambda p: Name.confidence(p))

  def divisions(self, names):
    return map(lambda p: (Name.merge(p[0]), Name.merge(p[1])), partitions(names))

class NameSplitter(NameDivider):
  def atomic(self, names):
    return Class.ambiguous_center(maplist(lambda n: n.klass, names))

class NameBreaker(NameDivider):
  def atomic(self, names):
    False

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
