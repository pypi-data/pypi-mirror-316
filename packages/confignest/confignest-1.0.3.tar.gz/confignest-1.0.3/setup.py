import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="confignest",
    version="1.0.3",
    keywords=("pip", "confignest"),
    author="github.com/0-1CxH",
    author_email="h0.1c@foxmail.com",
    description="Managing Complex Configs in Nested Way.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0-1CxH/ConfigNest",
    packages=setuptools.find_packages(),
    license = "MIT Licence",
    platforms = "any",
)
