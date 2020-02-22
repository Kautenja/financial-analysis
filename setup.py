"""The setup script for installing and distributing the package."""
from setuptools import setup, find_packages


# read the contents from the README file
with open('README.md') as README_file:
    README = README_file.read()


setup(
    name='financial-analysis',
    version='1.1.3',
    description='A pandas extension for performing financial analysis on trade data.',
    long_description=README,
    long_description_content_type='text/markdown',
    keywords='Finance Data Equity Option Future Index',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Office/Business :: Financial',
        'Topic :: Office/Business :: Financial :: Investment'
    ],
    url='https://github.com/Kautenja/financial-analysis',
    author='Christian Kauten',
    author_email='kautencreations@gmail.com',
    license='MIT',
    install_requires=[
        'numpy>=1.16.2',
        'pandas>=0.25.0',
    ],
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    zip_safe=False,
)
