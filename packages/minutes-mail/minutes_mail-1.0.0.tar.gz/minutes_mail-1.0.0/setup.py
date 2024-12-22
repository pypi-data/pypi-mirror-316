from setuptools import setup, find_packages


def read_version():
    version = {}
    with open("minutes_mail/version.py", "r") as f:
        exec(f.read(), version)
        return version["__version__"]


setup(
    name="minutes_mail",
    version=read_version(),
    description="Get temp mails and verification codes.",
    author="Sina",
    author_email="sinaorojlo53@gmail.com",
    packages=find_packages(include=["mail", "mail.*"]),
    install_requires=open("requirements.txt").readlines(),
    python_requires=">=3.6.0",
    license="MIT",
)
