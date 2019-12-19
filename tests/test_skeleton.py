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

def makeRegistry(givens, families):
  return None

sample_registry = makeRegistry(names, surnames)


class Registry:
  def __init__(self, givens, families, ambiguous, options):
      self.givens = givens
      self.families = families
      self.ambiguous = ambiguous
      self.options = options

  @staticmethod
  def make(givens, families, options = None):
    givens_set = set(givens)
    families_set = set(families)
    ambiguous = givens.intersection(families)
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
    return Class.merge(map(lambda n: self.classify(n), ns))


import unidecode


class RegistryOptions:
  def __init__(self, transliterate_names = False, treat_unknown_as_family = False):
    self.transliterate_names = transliterate_names
    self.treat_unknown_as_family = treat_unknown_as_family

  def encode(self, n):
    return (unidecode.unidecode(n) if self.transliterate_names else n).lower()

  def encode_many(self, ns):
    return set(map(lambda n: self.encode(n)), ns)

class GivenAndFamily:
  def __init__(self, givens, families):
    self.givens = givens
    self.families = families

  def as_tuple(self):
    return (self.givens, self.families)

  def __hash__(self):
    return hash(self.as_tuple())

  def __eq__(self, other):
      return self.__class__ == other.__class__ and self.as_tuple() == other.as_tuple()


from enum import Enum

class Class(Enum):
  GIVEN = 1
  FAMILY = 2
  OTHER = 3
  BAD = 4

  def is_givenish(self):
    return self == GIVEN or self == OTHER

  def is_familish(self):
    return self == FAMILY or self == OTHER

  @staticmethod
  def merge(classes):
    if len(classes) == 1:
      return classes[0]

    if classes[0] == GIVEN and all(x.is_givenish() for x in classes[1:]):
      return GIVEN

    if classes[0] == FAMILY and all(x.is_familish() for x in classes[1:]):
      return FAMILY

    if classes[0] == OTHER:
      return Class.merge(classes[1:])

    return BAD

  @staticmethod
  def confidence(pair):
    first, second = pair

    if first == GIVEN and second == FAMILY:
      return 8
    if first == FAMILY and second == GIVEN:
      return 8
    if first == FAMILY and second == OTHER:
      return 7
    if first == OTHER and second == FAMILY:
      return 7
    if first == GIVEN and second == OTHER:
      return 6
    if first == OTHER and second == GIVEN:
      return 6
    if first == OTHER and second == OTHER:
      return 5
    if first == FAMILY and second == FAMILY:
      return 4
    if first == GIVEN and second == GIVEN:
      return 4
    if first == BAD and second == FAMILY:
      return 3
    if first == FAMILY and second == BAD:
      return 3
    if first == BAD and second == GIVEN:
      return 2
    if first == GIVEN and second == BAD:
      return 2
    if first == BAD and second == OTHER:
      return 1
    if first == OTHER and second == BAD:
      return 1
    if first == BAD and second == BAD:
      return 0


def flatten(xss):
  return [x for y in xss for x in y]

class Name:
  def __init__(self, value, klass):
    self.value = value
    self.klass = klass

  @staticmethod
  def merge(ns):
    return Name(flatten(map(lambda n: n.value, ns)), Class.merge(map(lambda n:n.klass, ns)))

  @staticmethod
  def confidence(pair):
    return Class.confidence((pair[0].klass, pair[1].klass))

# class NameSplitter:
# def divide(self):
# splitNames :: NameDivider
# splitNames names | ambiguousNamesCenter names = Nothing
# ambiguousNamesCenter :: [Name] -> Bool
# ambiguousNamesCenter = ambiguousCenter . map cls
# splitNames names = Just $ breakNames names

class NameBreaker:
  def divide(self, names):
    return max(Name.confidence(partition) for partition in self.divisions(names))

  def divisions(self, names):
    return map(lambda p: (Name.merge(p[0]), Name.merge(p[1])), partitions(names))


# makeName :: Registry -> [String] -> Name
# makeName registry n = Name n (classifyMany registry n)

# makeSingletonName :: Registry -> String -> Name
# makeSingletonName registry n = Name [n] (classify registry n)


# partitions :: [a] -> [([a], [a])]
# partitions xs = [splitAt x xs| x <- [1 .. (length xs - 1)]]


# ambiguousCenter :: [Class] -> Bool
# ambiguousCenter (Other:xs)  = ambiguousCenter xs
# ambiguousCenter (Given:xs)  = ambiguousGivenCenter [] xs
# ambiguousCenter (Family:xs) = ambiguousFamilyCenter [] xs
# ambiguousCenter _           = False

# ambiguousGivenCenter :: [Class] -> [Class] -> Bool
# ambiguousGivenCenter os (Given:xs)  = ambiguousGivenCenter [] xs
# ambiguousGivenCenter os (Family:xs) = not . null $ os
# ambiguousGivenCenter os (Other:xs)  = ambiguousGivenCenter (Other:os) xs
# ambiguousGivenCenter os _           = False

# ambiguousFamilyCenter :: [Class] -> [Class] -> Bool
# ambiguousFamilyCenter os (Family:xs) = ambiguousFamilyCenter [] xs
# ambiguousFamilyCenter os (Given:xs)  = not . null $ os
# ambiguousFamilyCenter os (Other:xs)  = ambiguousFamilyCenter (Other:os) xs
# ambiguousFamilyCenter os _           = False


def run(personal_name):
  return personal_name

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

