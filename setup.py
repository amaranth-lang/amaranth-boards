import sys
from setuptools import setup, find_packages
import versioneer


setup(
    name="nmigen-boards",
    version=versioneer.get_version(),
    author="whitequark",
    author_email="whitequark@whitequark.org",
    description="Board and connector definitions for nMigen",
    #long_description="""TODO""",
    license="BSD",
    install_requires=["nmigen"],
    packages=find_packages(),
    project_urls={
        "Source Code": "https://github.com/m-labs/nmigen-boards",
        "Bug Tracker": "https://github.com/m-labs/nmigen-boards/issues",
    },
    cmdclass=versioneer.get_cmdclass()
)
