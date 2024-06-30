from setuptools import find_packages, setup

setup(
    name='jit',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'GitPython',
    ],
    entry_points={
        'console_scripts': [
            'jit=jit.cli:jit',
        ],
    },
)