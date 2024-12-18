from setuptools import find_packages, setup

setup(
    name="libcove2",
    version="0.2.1",
    author="Open Data Services",
    author_email="code@opendataservices.coop",
    url="https://github.com/OpenDataServices/lib-cove-2",
    description="A data review library",
    packages=find_packages(),
    long_description="A data review library",
    python_requires=">=3.8",
    install_requires=["requests"],
    classifiers=[],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "isort",
            "flake8",
            "mypy",
            "sphinx",
            "odsc-default-sphinx-theme",
        ],
    },
)
