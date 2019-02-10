from setuptools import setup, find_packages
import sys
try:
    from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
    class bdist_wheel(_bdist_wheel):
        def finalize_options(self):
            _bdist_wheel.finalize_options(self)
            self.root_is_pure = True
except ImportError:
    bdist_wheel = None

with open('version', 'r') as f:
    version = f.read()
    version = version.strip()

with open('README.md', 'r') as f:
    long_description = f.read()

setup(name='murmuration',
      version=version,
      description="encryption primitives for use with aws",
      long_description=long_description,
      long_description_content_type='text/markdown',
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'License :: OSI Approved :: BSD License',
          'Topic :: Security :: Cryptography',
          'Topic :: Utilities',
      ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      cmdclass={'bdist_wheel': bdist_wheel},
      keywords='aws python encryption cryptography kms',
      author='Preetam Shingavi',
      author_email='p.shingavi@yahoo.com',
      url='https://github.com/angry-penguins/murmuration',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          'boto3>=1.9.0',
          'pycryptodome>=3.7.3',
      ],
      entry_points={

      })
