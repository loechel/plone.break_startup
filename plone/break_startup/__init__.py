# -*- coding: utf-8 -*-

from plone.vulnerabilitychecks.core import VulnerabilityError
from plone.vulnerabilitychecks.core import VulnerabilityChecker as VC
from plone.vulnerabilitychecks.core.utils import getLatestVersion
from plone.vulnerabilitychecks.core.utils import getLatestBugfixRelease
from plone.vulnerabilitychecks.core.version_utils import parse_version

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

    if not vc.is_secure():
        logger.error("""
You try to start a Plone Instance that is not secure.
You have Plone {version} installed, for this version apply following patches: {patches}
            """.format(version=plone_version, patches="\n * ".join(vc.getPatches())))
        raise VulnerabilityError("User attemped to start an insecure Plone instance.")

    latest_bugfix_version = getLatestBugfixRelease(package='Plone', version=plone_version)
    vcb = VC(latest_bugfix_version)
    if not vc.is_in_security_support():

        if vcb.is_in_security_support():
            logger.warning('''
You try to start a Plone Instance that seems secure, but is not in security support anymore.
You have Plone %s installed, please update to latest bugfix release %s.
            ''', plone_version, latest_bugfix_version)

        else:       
            latest_version = getLatestVersion(package='Plone')
            logger.warning('''
You try to start a Plone Instance that seems secure, but neigther this version
nor the whole release group is in security support anymore. 
You have Plone %s installed, please update to latest release %s.
            ''', plone_version, latest_version)

    else: 
        if parse_version(latest_bugfix_version) > parse_version(plone_version) and vcb.is_in_security_support():
            logger.warning('''
You try to start a Plone Instance that seems secure, but is not latest bugfix release.
You have Plone %s installed, please update to latest bugfix release %s.
            ''', plone_version, latest_bugfix_version)
