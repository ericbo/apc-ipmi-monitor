#https://packaging.python.org/tutorials/packaging-projects/

import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apc-ipmi-monitor-ericbo", # Replace with your own username
    version=os.getenv("RELEASE_VERSION"),
    author="Eric Bottazzi",
    author_email="author@example.com",
    description="Trigger a graceful shutdown on all servers in the event there is an extended power outage.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ericbo/apc-ipmi-monitor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Operating System :: POSIX :: Linux"
    ],
    python_requires='>=3.6',
    scripts=['bin/apc-ipmi-monitor'],
)