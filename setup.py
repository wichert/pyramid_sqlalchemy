from setuptools import setup
from setuptools import find_packages

version = '1.0'

requires = [
    'SQLAlchemy >= 0.8.0',
    'zope.sqlalchemy',
    ]

tests_require = [
    'mock',
    ]

setup(name='pyramid_sqlalchemy',
      version=version,
      description='SQLAlchemy integration for pyramid',
      long_description=open('README.rst').read() + '\n' +
              open('changes.rst').read(),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Framework :: Pyramid',
          'Programming Language :: Python :: 2',
          'Programming Language :: Python :: 2.6',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.3',
          'Programming Language :: Python :: 3.4',
          'Topic :: Database',
          'Topic :: Software Development :: Libraries :: Python Modules',
        ],
      author='Wichert Akkerman',
      author_email='wichert@wiggy.net',
      url='https://pyramid-sqlalchemy.readthedocs.org',
      license='BSD',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=True,
      install_requires=requires,
      tests_require=tests_require,
      extras_require={
          'docs': ['sphinx'],
          'tests': tests_require,
          },
      )
