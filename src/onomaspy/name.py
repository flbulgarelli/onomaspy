from onomaspy.klass import Class
from onomaspy.listy import flatmap, maplist

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
