from setuptools import setup, find_packages

setup(
    name='dynata-demandapi-client',
    version="1.0.1",
    license="MIT",
    description="A Python client library for the Dynata Demand API",
    long_description="A Python client library for the Dynata Demand API",
    author="Ridley Larsen",
    author_email="Ridley.Larsen@Dynata.com",
    url="https://github.com/dynata/python-demandapi-client",
    download_url="https://pypi.python.org/pypi/dynata-demandapi-client",
    packages=find_packages(exclude=('tests', )),
    platforms=['Any'],
    install_requires=['requests', 'jsonschema'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    keywords='dynata demand api',
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
