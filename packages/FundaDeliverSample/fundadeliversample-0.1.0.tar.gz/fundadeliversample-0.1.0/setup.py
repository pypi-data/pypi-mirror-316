__author__ = 'Xuanli CHEN'
"""
Xuanli Chen
Research Domain: Computer Vision, Machine Learning
Email: xuanli(dot)chen(at)icloud.com
LinkedIn: https://be.linkedin.com/in/xuanlichen
"""
from setuptools import setup, find_packages

setup(
    name='FundaDeliverSample',
    version='0.1.0',
    author='Vons',
    author_email='zb8cvonsdeliver@icloud.com',
    description='A package for delivering the FundaDeliverSample project',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'gin-config',
        'cryptography',
        # Add other dependencies here
    ],
    entry_points={
        'console_scripts': [
            'run-validator=FundaDeliverSample.validator:main',
        ],
    },
)