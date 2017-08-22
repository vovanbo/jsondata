from setuptools import setup

__vers__ = (0, 2, 18)
__version__ = "%02d.%02d.%03d" % (__vers__[0], __vers__[1], __vers__[2],)


url = 'https://github.com/vovanbo/jsondata'

keywords = 'JSON json json-schema jsonschema json-pointer jsonpointer ' \
           'JSONschema JSONPointer JSONPatch RFC7159 RFC4627 RFC6901 ' \
           'RFC6902 ECMA-262 ECMA-404 pointer schema path patch persistence ' \
           'serialization configuration plugins dynamic modules operations ' \
           'calculations'

description = "The 'jsondata' package provides for the modular in-memory " \
              "processing of JSON data by trees, branches, pointers, " \
              "and patches in accordance to the standards JSON/RFC7951, " \
              "JSON pointer / RFC6901, and JSON patch / RFC6902. " \
              "The syntax primitives build on the standard packages " \
              "'json' and 'jsonschema'. "

requirements = [
    'jsonschema',
]

test_requirements = [
    'pytest'
]

with open('README.rst') as readme_file:
    readme = readme_file.read()

setup(
    name='jsondata',
    version=__version__,
    description=description,
    long_description=readme + '\n\n',
    author='Arno-Can Uestuensoez',
    author_email='acue_sf2@sourceforge.net',
    maintainer='Vladimir Bolshakov',
    maintainer_email='vovanbo@gmail.com',
    url=url,
    download_url=url,
    packages=['jsondata'],
    package_data={
        'jsondata': [
            'README.rst', 'ArtisticLicense20.html', 'licenses-amendments.txt',
            'data.json', 'schema.jsd', 'datacheck.json', 'datacheck.jsd',
            'selftest.json', 'selftest.jsd', 'rfc6902.jsonp'
        ],
    },
    scripts=('bin/jsondc.py',),
    include_package_data=True,
    install_requires=requirements,
    license='Artistic-License-2.0 + Forced-Fairplay-Constraints',
    zip_safe=False,
    keywords=keywords,
    platforms=['Linux', 'Windows', 'darwin'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Free To Use But Restricted",
        "License :: OSI Approved :: Artistic License",
        "Natural Language :: English",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: BSD :: OpenBSD",
        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Unix Shell",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
    setup_requires=['pytest-runner'],
    test_suite='tests',
    tests_require=test_requirements
)
