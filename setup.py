from setuptools import setup, find_packages


def scm_version():
    def local_scheme(version):
        return version.format_choice("+{node}", "+{node}.dirty")
    return {
        "relative_to": __file__,
        "version_scheme": "guess-next-dev",
        "local_scheme": local_scheme,
    }


setup(
    name="nmigen-boards",
    use_scm_version=scm_version(),
    author="whitequark",
    author_email="whitequark@whitequark.org",
    description="Board and connector definitions for nMigen",
    #long_description="""TODO""",
    license="BSD",
    setup_requires=["wheel", "setuptools", "setuptools_scm"],
    install_requires=["nmigen>=0.1,<0.5"],
    packages=find_packages(),
    project_urls={
        "Source Code": "https://github.com/nmigen/nmigen-boards",
        "Bug Tracker": "https://github.com/nmigen/nmigen-boards/issues",
    },
)
