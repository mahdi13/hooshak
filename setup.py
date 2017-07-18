from setuptools import setup, find_packages

dependencies = [
    # 'gremlinpython',
    'numpy',
    'scipy',
    'boost',
    # 'graph-tool',
    # 'python-igraph',
    'pymlconf >= 0.7.1',

    # Testing
    'nose',
]


setup(
    name='hooshak',
    version='0.0.1',
    description='A recommender system uses implicit social network analyzing',
    author='M.Perfect',
    author_email='m.aali.pro@gmail.com',
    install_requires=dependencies,
    packages=find_packages(),
)
