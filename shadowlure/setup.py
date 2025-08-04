from setuptools import setup, find_packages

setup(
    name='shadowlure',
    version='1.0.0',
    url='',
    author='Windro xd',
    author_email='windroexe@gmail.com',
    description='A simple and extensible honeypot framework for logging network attacks.',
    long_description='A simple and extensible honeypot framework for logging network attacks.',
    install_requires=[
        'Twisted',
        'pyasn1',
        'cryptography',
        'passlib',
        'Jinja2',
        'zope.interface',
        'hpfeeds',
        'paramiko'
    ],
    setup_requires=[
        'setuptools_git'
    ],
    packages=find_packages(exclude=['docs', 'docs.*']),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'shadowlure = decoynet.entry:main'
        ]
    },
)
