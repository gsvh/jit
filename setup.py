from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='jit-cli',
    version='0.1.1',
    description='A command line tool to automatically create pull requests on GitHub',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url='https://github.com/gsvh/jit',
    author='George S. van Heerden',
    author_email='georgesebastiaan.vh@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.11',
        'Topic :: Software Development :: Version Control :: Git',
        'Topic :: Terminals',
        'Topic :: Text Processing :: Markup',
        'Topic :: Utilities'
    ],
    install_requires=[
        'click==8.1.7',
        'GitPython==3.1.43',
        'rich==13.7.1',
        'ollama==0.3.0',

    ],
    entry_points={
        'console_scripts': [
            'jit=jit.cli:jit',
        ],
    },
)