from onomaspy.klass import Class
from onomaspy.name import Name
from onomaspy.listy import maplist, partitions

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
