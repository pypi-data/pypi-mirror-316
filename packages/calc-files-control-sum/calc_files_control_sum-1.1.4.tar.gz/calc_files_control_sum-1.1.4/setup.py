#!/usr/bin/env python
import setuptools

with open("README.md") as file:
    read_me_description = file.read()

setuptools.setup(
    name="calc_files_control_sum",
    version="1.1.4",
    author="Roman Shevchik",
    author_email="kolbasilyvasily@yandex.ru",
    description="Calculate files control sum",
    long_description=read_me_description,
    long_description_content_type="text/markdown",
    url="https://github.com/octaprog7/CalcFilesControlSum",
    packages = setuptools.find_packages(where='src'),
    package_dir = {'': 'src'},
    package_data={"": ["*.csv", "*.zzz"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    python_requires='>=3.7.2,<3.12',
    entry_points={
        'console_scripts': [
            'cfcs = calc_files_control_sum.cfcs:main',
        ],
    }
)
