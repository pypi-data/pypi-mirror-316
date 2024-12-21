import setuptools

# pip install ../../Azure/PyObfuscate --upgrade -t ./.venv/lib/python3.10/site-packages/PyObfuscate
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setuptools.setup(
    name='PySimpleObfuscate',
    version='0.4',
    description='A Simple Python Obfuscator',
    packages=setuptools.find_packages('src'),
    install_requires=[],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'pyobfuscate=src.lib.cli:cli',
        ],
    },
    include_package_data=True,
    # other arguments omitted
    long_description=long_description,
    long_description_content_type='text/markdown'
)
