from setuptools import setup, find_packages

setup(
    name='FundaDeliverSample',
    version='0.1.2',
    author='Vons',
    author_email='zb8cvonsdeliver@icloud.com',
    description='A script for delivering the FundaDeliverSample project',
    py_modules=['validator'],
    packages=find_packages(),
    include_package_data=True,
    package_data={
        '': ['configs/*', 'pyarmor_runtime_000000/*'],
    },
    install_requires=[
        'gin-config',
        'cryptography',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'run-validator=validator:main',
        ],
    },
)