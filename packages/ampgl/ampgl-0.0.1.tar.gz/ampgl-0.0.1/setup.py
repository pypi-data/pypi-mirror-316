from setuptools import setup, find_packages


def readme():
  with open('README.md', 'r') as f:
    return f.read()


setup(
  name='ampgl',
  version='0.0.1',
  author='loggys-MetsA',
  author_email='albertmetsler3008@gmail.com',
  description='Pygame library with a lot of useful utilities.',
  long_description=readme(),
  long_description_content_type='text/markdown',
  url='https://github.com',
  packages=find_packages(),
  install_requires=['requests>=2.25.1'],
  classifiers=[
    'Programming Language :: Python :: 3.9',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
  ],
  keywords='ampgl games am pgl',
  project_urls={
    'GitHub': 'https://github.com/LoggysGit'
  },
  python_requires='>=3.6'
)