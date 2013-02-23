from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name='genepi',
      version='0.1',
      description='Genetici algorithms in python',
      long_description=readme(),
      url='http://github.com/bianchimro/genepi',
      author='Mauro Bianchi',
      author_email='bianchimro@gmail.com',
      license='MIT',
      packages=['genepi'],
      install_requires=[],
      tests_require=['nose'],
      #maybe a bug: https://github.com/nose-devs/nose/issues/629
      #test_suite='nose.collector',
      zip_safe=False)