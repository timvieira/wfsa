from setuptools import setup

setup(
    name='wfsa',
    version='0.1',
    description=(
        "Implementation of field-weighted finite state automata."
    ),
    project_url = 'https://github.com/timvieira/wfsa',
    install_requires = [
        'numpy',
        'pytest',
        'graphviz',   # for notebook visualization of left-recursion graph
        'arsenal @ git+https://github.com/timvieira/arsenal',
    ],
    authors = [
        'Tim Vieira',
    ],
    readme=open('README.md').read(),
    scripts=[],
    packages=['wfsa'],
)
