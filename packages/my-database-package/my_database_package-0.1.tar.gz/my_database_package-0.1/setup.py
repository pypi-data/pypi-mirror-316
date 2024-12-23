from setuptools import setup, find_packages

setup(
    name='my_database_package',  # Name of the package
    version='0.1',
    packages=find_packages(),  # Automatically discovers all the packages in the directory
    install_requires=[
        'pg8000',  # External package dependencies
    ],
    description='A package to query data from a PostgreSQL database',
    author='Your Name',
    author_email='your_email@example.com',
    url='https://github.com/yourusername/my_database_package',  # Optional, for GitHub or PyPI
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
