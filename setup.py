from setuptools import setup, find_packages

version = '0.0'

setup(name='invoiceuploader',
      version=version,
      description="",
      long_description="""\
""",
      # Get strings from http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[],
      keywords="",
      author="",
      author_email="",
      url="",
      license="",
      package_dir={'': 'src'},
      packages=find_packages('src'),
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'grokcore.view',
                        'fanstatic',
                        'zope.fanstatic',
                        'grokcore.chameleon',
                        'grokcore.startup',
                        'zope.principalregistry',
                        'zope.securitypolicy',
                        'grokcore.error',
                        'dolmen.beaker',
                        'zeam.form.base',
                        'zeam.form.ztk',
                        'waitress',
                        # Add extra requirements here
                        ],
      entry_points={
          'fanstatic.libraries': [
              'loginserver = invoiceuploader.resource:library',
          ]
      })
