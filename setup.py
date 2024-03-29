"""Setup script.

Usage examples:

pip install -e . pip install -e .[develop]
"""
from setuptools import find_packages, setup

setup(name="llm4pddl",
      version="0.1.0",
      packages=find_packages(include=["llm4pddl", "llm4pddl.*"]),
      install_requires=[
          "PyYAML", "types-PyYAML", "numpy", "pandas", "pandas-stubs",
          "openai", "transformers", "matplotlib", "sentence-transformers"
      ],
      setup_requires=['setuptools_scm'],
      include_package_data=True,
      extras_require={
          "develop": [
              "mypy", "pytest-cov>=2.12.1", "pytest-pylint>=0.18.0",
              "yapf==0.32.0", "docformatter", "isort"
          ]
      })
