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
    packages=['shadowlure'],
    package_dir={'shadowlure': 'shadowlure'},
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'shadowlure = shadowlure.entry:main'
        ]
    },
)
