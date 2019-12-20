from onomaspy.name import Name
from onomaspy.klass import Class


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

  def __repr__(self):
    return 'FullName(%s)' % self.names

  def analyze(self, registry, divider):
    return divider.try_divide(list(map(lambda n: Name.make_singleton(registry, n), self.names)))

  def valid(self):
    return len(self.names) > 1
