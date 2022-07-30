from setuptools import setup, find_packages

setup(
    name="llm4pddl",
    version="0.1.0",
    packages=find_packages(include=["llm4pddl", "llm4pddl.*"]),
    install_requires=[
        "absl-py",
        "PyYAML",
    ],
    extras_require={"develop": [
        "mypy",
        "pytest-cov>=2.12.1",
        "pytest-pylint>=0.18.0",
        "yapf==0.32.0",
        "docformatter",
        "isort"
    ]}
)

