from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='allforgraphs',
  version='0.3.2',
  author='katya,maria,olga',
  author_email='1132236136@pfur.ru',
  description='Library for graphs.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com/Katerok27153/allforgraphs.git',
  packages=find_packages('.'),
  install_requires=['requests>=2.25.1', 'numpy>=2.2.0', 'networkx>=3.4.2'],
  classifiers=[
    'Programming Language :: Python :: 3.11',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='files speedfiles ',
  project_urls={
    'GitHub': 'https://github.com/Katerok27153/allforgraphs.git'
  },
  python_requires='>=3.6'
)