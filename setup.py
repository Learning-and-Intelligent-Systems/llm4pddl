from setuptools import setup, find_packages

setup(
    name='llm4pddl',
    version='0.1.0',
    packages=find_packages(include=['llm4pddl', 'llm4pddl.*']),
    install_requires=[
        'absl-py',
        'PyYAML',
    ],
)

