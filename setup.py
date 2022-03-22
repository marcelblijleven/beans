from setuptools import find_packages, setup

# Get README content
try:
    with open("README.md", "r") as f:
        readme_description = "\n".join(f.readlines())
except IOError:
    readme_description = ""

setup(
    name="beans",
    version="",
    author="Marcel Blijleven",
    url="https://github.com/marcelblijleven/beans",
    description="",
    long_description=readme_description,
    zip_safe=False,
    install_requires=[],
    extras_require={},
    setup_requires=["setuptools_scm==3.1.0"],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    scripts=["manage.py"],
)
