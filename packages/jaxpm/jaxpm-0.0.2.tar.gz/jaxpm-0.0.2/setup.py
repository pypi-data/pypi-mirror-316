from setuptools import find_packages, setup

setup(
    name='jaxpm',
    version='0.0.2',
    url='https://github.com/DifferentiableUniverseInitiative/JaxPM',
    author='JaxPM developers',
    description='A dead simple FastPM implementation in JAX',
    packages=find_packages(),
    install_requires=['jax', 'jax_cosmo'],
)
