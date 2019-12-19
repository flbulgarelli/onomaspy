def flatmap(f, xss):
  return flatten(map(f, xss))

def flatten(xss):
  return [x for y in xss for x in y]

def partitions(xss):
  return [(xss[:i], xss[i:]) for i in range(1, len(xss))]

def maplist(f, xs):
  return list(map(f, xs))
