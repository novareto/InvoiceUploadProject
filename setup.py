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
                        'uvc.tbskin',
                        'uvc.layout',
                        'zeam.form.base',
                        'zeam.form.ztk',
                        'zeam.form.layout',
                        'ukhtheme.grok',
                        'ukhtheme.resources',
                        'waitress',
                        'megrok.z3ctable',
                        'dolmen.forms.wizard',
                        'dolmen.forms.base',
                        'uvc.api',
                        'uvc.protectionwidgets',
                        'uvc.uploader',
                        'reportlab',
                        'PyPDF2',
                        'img2pdf',
                        'backports.tempfile'
                        ],
      entry_points={
          'fanstatic.libraries': [
              'invoiceuploader = invoiceuploader.resource:library',
          ]
      })
