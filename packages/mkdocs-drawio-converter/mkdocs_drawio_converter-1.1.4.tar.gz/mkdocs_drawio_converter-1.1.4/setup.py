from setuptools import setup, find_packages

setup(
    name='mkdocs-drawio-converter',
    version='1.1.4',
    description='MkDocs plugin to convert Drawio files to SVG format',
    author='Rajneesh Kumar/Subhanshu Shukla',
    author_email='rajneesh.aggarwal@gmail.com',
    packages=find_packages(),
    install_requires=[
        'mkdocs>=1.0.0'
    ],
    entry_points={
        'mkdocs.plugins': [
            'drawio-converter = mkdocs_drawio_converter.plugin:DrawioConverterPlugin',
        ]
    }
)