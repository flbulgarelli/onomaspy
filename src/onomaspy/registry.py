from onomaspy.klass import Class
from onomaspy.listy import maplist
import unidecode


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


class RegistryOptions:
  def __init__(self, transliterate_names = False, treat_unknown_as_family = False):
    self.transliterate_names = transliterate_names
    self.treat_unknown_as_family = treat_unknown_as_family

  def encode(self, n):
    return (unidecode.unidecode(n) if self.transliterate_names else n).lower()

  def encode_many(self, ns):
    return set(map(lambda n: self.encode(n), ns))
