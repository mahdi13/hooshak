from setuptools import setup, find_packages

dependencies = [
    'gremlinpython',

    # Testing
    'nose',
]


setup(
    name='hooshak',
    version='0.0.1',
    description='A toolchain for developing REST APIs',
    author='M.Perfect',
    author_email='m.aali.pro@gmail.com',
    install_requires=dependencies,
    packages=find_packages(),
)
