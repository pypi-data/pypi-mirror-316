from setuptools import setup, find_packages

# leer el contenido de README.md
with open("README.md", "r", encoding="utf-8") as fh:
	long_description = fh.read()

setup(
	name="paquete889",
	version="0.1.2",
	packages=find_packages(),
	install_requires=[],
	author="Aaron tests",
	description="test",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://hack4u.io",
)
