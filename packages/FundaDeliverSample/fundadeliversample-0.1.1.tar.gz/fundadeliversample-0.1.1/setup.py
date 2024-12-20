from setuptools import setup

setup(
    name='FundaDeliverSample',
    version='0.1.1',
    author='Vons',
    author_email='zb8cvonsdeliver@icloud.com',
    description='A script for delivering the FundaDeliverSample project',
    py_modules=['validator'],
    include_package_data=True,
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