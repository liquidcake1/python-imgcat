#!/usr/bin/env python

import sys
import os
import re

from setuptools import setup, Command


__PATH__ = os.path.abspath(os.path.dirname(__file__))


def read_readme():
    with open('README.md') as f:
        return f.read()

def read_version():
    # importing the package causes an ImportError :-)
    with open(os.path.join(__PATH__, 'imgcat/__init__.py')) as f:
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                                  f.read(), re.M)
    if version_match:
        return str(version_match.group(1))
    raise RuntimeError("Unable to find __version__ string")


install_requires = [
]

tests_requires = [
    'pytest',
    'numpy',
    'torch',
    'tensorflow>=2.0',
    'matplotlib>=3.3',
    'Pillow',
]

__version__ = read_version()


# brought from https://github.com/kennethreitz/setup.py
class DeployCommand(Command):
    description = 'Build and deploy the package to PyPI.'
    user_options = []

    def initialize_options(self): pass
    def finalize_options(self): pass

    @staticmethod
    def status(s):
        print(s)

    def run(self):
        import twine  # we require twine locally  # type: ignore  # noqa

        assert 'dev' not in __version__, \
            "Only non-devel versions are allowed. __version__ == {}".format(__version__)

        with os.popen("git status --short") as fp:
            git_status = fp.read().strip()
            if git_status:
                print("Error: git repository is not clean.\n")
                os.system("git status --short")
                sys.exit(1)

        try:
            from shutil import rmtree
            self.status('Removing previous builds ...')
            rmtree(os.path.join(__PATH__, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        os.system('twine upload dist/*')

        self.status('Creating git tags ...')
        os.system('git tag v{0}'.format(__version__))
        os.system('git tag --list')
        sys.exit()


setup(
    name='imgcat',
    version=__version__,
    license='MIT',
    description='imgcat as Python API and CLI',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/wookayin/python-imgcat',
    author='Jongwook Choi',
    author_email='wookayin@gmail.com',
    keywords='imgcat iterm2 matplotlib',
    classifiers=[
        # https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    packages=['imgcat'],
    python_requires='>=3.6',
    install_requires=install_requires,
    extras_require={'test': tests_requires},
    setup_requires=['pytest-runner<5.0'],
    tests_require=tests_requires,
    entry_points={
        'console_scripts': ['imgcat=imgcat:main'],
    },
    include_package_data=True,
    zip_safe=False,
    cmdclass={
        'deploy': DeployCommand,
    }
)
