# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
from onomaspy.personal_name import PersonalName, FullName, GivenAndFamily
from onomaspy.registry import Registry, RegistryOptions
from onomaspy.name_divider import NameBreaker, NameSplitter

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = get_distribution(dist_name).version
except DistributionNotFound:
    __version__ = 'unknown'
finally:
    del get_distribution, DistributionNotFound
