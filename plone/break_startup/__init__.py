# -*- coding: utf-8 -*-

from plone.break_core import VulnerabilityCheck as VC
from plone.break_core import SecurityError

import logging
import pkg_resources

def initialize(context):
    """Initializer called when used as a Zope 2 product."""



    logger = logging.getLogger("plone.break_startup")
    
    installed_patches_list = []
    ws = pkg_resources.working_set

    for pkg in ws:
    	if pkg.project_name.startswith("Products.PloneHotfix"):
    		installed_patches_list.append(pkg.project_name)

    plone_version = pkg_resources.get_distribution("Plone").version

    vc = VC(plone_version, installed_patches_list)

    if not vc.isSecure():
    	logger.error("""
You try to start a Plone Instance that is not secure.
You have Plone {0} installed, for this version apply following patches:
 * {1}
    		""".format(plone_version, "\n * ".join(vc.getPatches())))
    	raise SecurityError("User attemped to start an insecure Plone instance.")


