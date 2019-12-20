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
    if not classes:
      return False

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
