from setuptools import find_packages, setup


setup(
    name="widgetastic.patternfly4",
    use_scm_version=True,
    author="Dmitry Misharov",
    author_email="misharov@redhat.com",
    description="Patternfly4 widget library for Widgetastic",
    license="Apache license",
    url="https://github.com/quarckster/widgetastic.patternfly4",
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=[
        "widgetastic.core>=0.35",
    ],
    setup_requires=[
        "setuptools_scm",
    ],
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
        "Topic :: Software Development :: Testing",
    ],
)
