from setuptools import setup

requires = [
    "colander",
    "sqlalchemy",
]

tests_require = [
    "pytest",
    "testfixtures",
]

example_require = [
    "pyramid_jinja2",
    "pyramid_sqlalchemy",
    "pyramid_tm",
    "deform",
    "peppercorn",
    "webtest",
]

dev_requires = [
    "flake8",
    "yapf",
    "tox",
]

setup(
    name="rebecca.search",
    packages=["rebecca.search"],
    namespace_packages=["rebecca"],
    install_requires=requires,
    extras_require={
        "dev": dev_requires,
        "testing": tests_require,
        "example": example_require
    })
