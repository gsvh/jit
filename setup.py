from setuptools import find_packages, setup


# Function to read requirements from a file
def load_requirements(filename='requirements.txt'):
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

setup(
    name='jit',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=load_requirements(),
    entry_points={
        'console_scripts': [
            'jit=jit.cli:jit',
        ],
    },
)