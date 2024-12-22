from setuptools import setup, find_packages

setup(
  name='msordinal',
  version='0.2',
  author='Paul77ms',
  # package_data=find_packages(),
  entry_points={
      'console_scripts': [
      'msordinal = msordinal.main:main',
    ],
  },
  install_requires=[
  ],
)