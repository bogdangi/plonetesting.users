from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='plonetesting.users',
      version=version,
      description="plonetesting users data extention",
      long_description=open("README.rst").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Framework :: Plone :: 4.3",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Bogdan Girman',
      author_email='bogdan.girman@gmail.com',
      url='https://github.com/bogdangi/plonetesting.policy',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plonetesting'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'python-linkedin',
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      extras_require={
          'test': [
              'plone.app.robotframework',
              'plone.app.testing[robot]',
          ],
      },
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      setup_requires=["PasteScript"],
      paster_plugins=["ZopeSkel"],
      )
