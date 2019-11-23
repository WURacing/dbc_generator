import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dbc_generator",
    version="0.1.0",
    author="WURacing",
    author_email="wuracing@gmail.com",
    description="DBC Generation Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WURacing/dbc_generator",
)
