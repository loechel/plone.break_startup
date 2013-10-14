from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(name='plone.break_startup',
      version=version,
      description="Add-on that will prevent startup of a Zope Instance with an unpatched Plone Version",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        ],
      keywords='',
      author='Alexander Loechel',
      author_email='Alexander.Loechel@lmu.de',
      url='https://github.com/collective/plone.break_startup',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
          'plone.break_core',
      ],
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
