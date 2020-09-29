from setuptools import find_packages, setup

with open('VERSION') as version_file:
    version = version_file.read().strip()

setup(
    name='{{cookiecutter.package_name}}',
    packages=find_packages(),
    version=version,
    description='{{cookiecutter.description}}',
    author='{{cookiecutter.author}}',
    license='',
    python_requires='>=3',
    package_data={'{{cookiecutter.package_name}}': ['configuration/*.json']},
    classifiers=[
    'Programming Language :: Python :: 3.7',
    ],
)
