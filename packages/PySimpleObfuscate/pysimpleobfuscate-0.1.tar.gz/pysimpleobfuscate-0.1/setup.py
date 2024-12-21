import setuptools

# pip install ../../Azure/PyObfuscate --upgrade -t ./.venv/lib/python3.10/site-packages/PyObfuscate
  
setuptools.setup(
    name='PySimpleObfuscate',
    version='0.1',
    description='A Simple Python Obfuscator',
    packages=setuptools.find_packages('src'),
    install_requires=[],
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'pyobfuscate=PyObfuscate.lib.cli:cli',
        ],
    },
    include_package_data=True,
)