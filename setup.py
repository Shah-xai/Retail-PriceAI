import setuptools
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()
__version__="0.0.1"
setuptools.setup(
    name="NLP-regression",
    version=__version__,
    author="Shah",
    author_email="abedinn.shah@gmail.com",
    description="A NLP regression model for retail price prediction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shah-xai/Retail-PriceAI",
)
package_dir={"":"src"}
setuptools.find_packages(where="src")
