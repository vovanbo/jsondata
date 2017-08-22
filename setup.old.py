"""Distribute 'jsondata', a thin layer for the management of JSON data branches.

   Installs 'jsondata', adds/modifies the following helper features to standard
   'setuptools' options.

   Args:
      build_doc: Creates Sphinx based documentation with embeded javadoc-style
          API documentation, html only.

      build_sphinx: Creates documentation for runtime system by Sphinx,
        html only. Calls 'callDocSphinx.sh'.

      build_epydoc: Creates standalone documentation for runtime system
        by Epydoc, html only.

      project_doc: Install a local copy into the doc directory of the project.

      instal_doc: Install a local copy of the previously build documents in 
          accordance to PEP-370.

      test: Runs PyUnit tests by discovery.

      usecases: Runs PyUnit UseCases by discovery, a lightweight
          set of unit tests.

      --no-install-required: Suppresses installation dependency checks, 
          requires appropriate PYTHONPATH.
      --offline: Sets online dependencies to offline, or ignores online
          dependencies.

      --exit: Exit 'setup.py'.

      --help-jsondata: Displays this help.

   Returns:
      Results for success in installed 'jsondata'.

   Raises:
      ffs.

"""
import os
import sys
import re
import shutil
import tempfile

from setuptools import setup
import fnmatch


__author__ = 'Arno-Can Uestuensoez'
__maintainer__ = 'Arno-Can Uestuensoez'
__author_email__ = 'acue_sf2@sourceforge.net'
__license__ = "Artistic-License-2.0 + Forced-Fairplay-Constraints"
__copyright__ = "Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez"
# __version__ = '0.2.18'
__uuid__ = '63b597d6-4ada-4880-9f99-f5e0961351fb'


_NAME = 'jsondata'

__sdk = False
"""Set by the option "--sdk". Controls the installation environment."""
if '--sdk' in sys.argv:
    _sdk = True
    sys.argv.remove('--sdk')

# required for various interfaces, thus just do it
_mypath = os.path.dirname(os.path.abspath(__file__))
"""Path of this file."""
sys.path.insert(0, os.path.abspath(_mypath))

# --------------------------------------
#
# Package parameters for setuptools
#
# --------------------------------------
_name = 'jsondata'
__pkgname__ = "jsondata"
"""package name"""

__vers__ = [0, 2, 18, ]
"""version parts for easy processing"""

__version__ = "%02d.%02d.%03d" % (__vers__[0], __vers__[1], __vers__[2],)
"""assembled version string"""

__author__ = "acue"
"""author of the package"""

_packages = ["jsondata"]
"""Python packages to be installed."""

_scripts = ("bin/jsondc.py",)
"""Scripts to be installed."""

_package_data = {
    'jsondata': ['README.md', 'ArtisticLicense20.html',
                 'licenses-amendments.txt',
                 'data.json', 'schema.jsd', 'datacheck.json', 'datacheck.jsd',
                 'selftest.json', 'selftest.jsd',
                 'rfc6902.jsonp',
                 ],
}
"""Provided data of the package."""

_platforms = ['Linux', 'Windows', 'darwin', ]
"""provided platforms"""

_url = 'https://sourceforge.net/projects/jsondata/'
"""URL of this package"""

# _download_url="https://github.com/ArnoCan/filesysobjects/"
_download_url = "https://sourceforge.net/projects/jsondata/files/"

_install_requires = []
"""prerequired non-standard packages"""

_keywords = 'JSON json json-schema jsonschema json-pointer jsonpointer ' \
            'JSONschema JSONPointer JSONPatch RFC7159 RFC4627 RFC6901 ' \
            'RFC6902 ECMA-262 ECMA-404 pointer schema path patch persistence ' \
            'serialization configuration plugins dynamic modules operations ' \
            'calculations'

"""keywords for search index"""

_description = "The 'jsondata' package provides for the modular in-memory " \
               "processing of JSON data by trees, branches, pointers, " \
               "and patches in accordance to the standards JSON/RFC7951, " \
               "JSON pointer / RFC6901, and JSON patch / RFC6902. " \
               "The syntax primitives build on the standard packages " \
               "'json' and 'jsonschema'. "

# def read(fname):
#     return open(os.path.join(os.path.dirname(__file__), fname)).read()
_README = os.path.join(os.path.dirname(__file__), 'README.md')
_long_description = open(_README).read() + 'nn'
"""detailed description of this package"""

_classifiers = [
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
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Unix Shell",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities"
]
"""the classification of this package"""

_epydoc_api_patchlist = [
    'path_syntax.html',
    'usecases.html',
    'shortcuts.html',
    'filesysobjects.html',
    'pyfilesysobjects.html',
]

"""Patch list of Sphinx documents for the insertion of links to API documentation."""

_profiling_components = _mypath + os.sep + 'bin' + os.sep + '*.py ' + _mypath + os.sep + __pkgname__ + os.sep + '*.py'
"""Components to be used for the creation of profiling information for Epydoc."""

_doc_subpath = 'en' + os.path.sep + 'html' + os.path.sep + 'man7'
"""Relative path under the documents directory."""

_sharepath = os.path.expanduser(
    os.path.sep + 'share' + os.path.sep + 'projdata' + os.path.sep + 'twint' + os.path.sep + 'devops' + os.path.sep + __pkgname__)
"""Project specific common network directory on the AdNovum share."""

# runtime dependencies - RHEL6.x standard is sufficient
_install_requires = [
    'jsonschema',
    #    'functools32', # 7.x
    #    'repoze.lru',  # 6.x
    #    'termcolor',
    'pyfilesysobjects >=0.1.12',
    'pysourceinfo >=0.1.12',
]

if __sdk:  # pragma: no cover
    _install_requires.extend(
        [
            'sphinx >= 1.4',
            'epydoc >= 3.0',
        ]
    )


def usage():
    if __name__ == '__main__':
        import pydoc
        # FIXME: literally displayed '__main__'
        print(pydoc.help(__name__))
    else:
        help(str(os.path.basename(sys.argv[0]).split('.')[0]))


#
# * shortcuts
#

exit_code = 0

# custom doc creation by sphinx-apidoc
if 'build_sphinx' in sys.argv or 'build_doc' in sys.argv:
    try:
        os.makedirs('build' + os.sep + 'apidoc' + os.sep + 'sphinx')
    except:
        pass

    print("#---------------------------------------------------------")
    exit_code = os.system('./callDocSphinx.sh')  # create apidoc
    print("#---------------------------------------------------------")
    print("Called/Finished callDocSphinx.sh => exit=" + str(exit_code))
    if 'build_sphinx' in sys.argv:
        sys.argv.remove('build_sphinx')

# common locations
src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
dst0 = os.path.normpath("build/apidoc/" + str(_NAME))

# custom doc creation by sphinx-apidoc with embeded epydoc
if 'build_doc' in sys.argv:

    # copy sphinx to mixed doc
    if not os.path.exists(src0):
        raise Exception("Missing generated sphinx document source:" + str(src0))
    if os.path.exists(dst0):
        shutil.rmtree(dst0)
    shutil.copytree(src0, dst0)

    print("#---------------------------------------------------------")
    exit_code = os.system('epydoc --config docsrc/epydoc.conf')  # create apidoc
    print("#---------------------------------------------------------")
    print("Called/Finished epydoc --config docsrc/epydoc.conf => exit=" + str(
        exit_code))


    def _sed(filename, pattern, repl, flags=0):
        pattern_compiled = re.compile(pattern, flags)
        fname = os.path.normpath(filename)
        with tempfile.NamedTemporaryFile(mode='w', delete=False) as ftmp:
            with open(fname) as src_file:
                for line in src_file:
                    ftmp.write(pattern_compiled.sub(repl, line))

        shutil.copystat(fname, ftmp.name)
        shutil.move(ftmp.name, fname)


    pt = '<a target="moduleFrame" href="toc-everything.html">Everything</a>'
    rp = r'<a href="../index.html" target="_top">Home</a>'
    rp += r' - '
    rp += r'<a href="./index.html" target="_top">Top</a>'
    rp += r' - '
    rp += pt

    fn = dst0 + '/epydoc/toc.html'
    _sed(fn, pt, rp, re.MULTILINE)

    pt = '<h4>Next topic</h4>'
    rp = r'<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>'
    rp += pt

    fn = dst0 + '/index.html'
    _sed(fn, pt, rp, re.MULTILINE)

    pt = '<h4>Previous topic</h4>'
    rp = r'<h4>API</h4><p class="topless"><a href="epydoc/index.html" title="API">Programming Interface</a></p>'
    rp += pt

    patchlist = [
        'shortcuts.html',
        'usecases.html',
        'jsondata.html',
        'jsondata_pointer_operations.html',
        'jsondata_patch_operations.html',
        'jsondata_branch_operations.html',
        'jsondata_branch_serializer.html',
        'jsondata_m_tree.html',
        'jsondata_m_serializer.html',
        'jsondata_m_patch.html',
        'jsondata_m_pointer.html',
        'jsondata_m_selftest.html',
        'software_design.html',
    ]
    for px in patchlist:
        fn = dst0 + os.sep + px
        _sed(fn, pt, rp, re.MULTILINE)

    sys.argv.remove('build_doc')

# custom doc creation by epydoc
if 'build_epydoc' in sys.argv:
    try:
        os.makedirs('build' + os.sep + 'apidoc' + os.sep + 'epydoc')
    except:
        pass

    print("#---------------------------------------------------------")
    exit_code = os.system(
        'epydoc --config docsrc/epydoc-standalone.conf')  # create apidoc
    print("#---------------------------------------------------------")
    print(
        "Called/Finished epydoc --config docsrc/epydoc-standalone.conf => exit=" + str(
            exit_code))
    sys.argv.remove('build_epydoc')

# install local project doc
if 'project_doc' in sys.argv:
    print("# project_doc.sh...")

    dstroot = os.path.normpath("doc/en/html/man3/") + os.sep

    try:
        os.makedirs(dstroot)
    except:
        pass

    if os.path.exists(dst0):
        if os.path.exists(dstroot + str(_NAME)):
            shutil.rmtree(dstroot + str(_NAME))
        shutil.copytree(dst0, dstroot + str(_NAME))

    src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".sphinx"):
            shutil.rmtree(dstroot + str(_NAME) + ".sphinx")
        shutil.copytree(src0, dstroot + str(_NAME) + ".sphinx")

    src0 = os.path.normpath("build/apidoc/epydoc")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".epydoc"):
            shutil.rmtree(dstroot + str(_NAME) + ".epydoc")
        shutil.copytree(src0, dstroot + str(_NAME) + ".epydoc")

    print("#")
    idx = 0
    for i in sys.argv:
        if i == 'install_doc': break
        idx += 1

    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    sys.argv.remove('project_doc')

# install user doc
if 'install_doc' in sys.argv:
    print("# install_doc.sh...")

    # set platform
    if sys.platform in ('win32'):
        dstroot = os.path.expandvars("%APPDATA%/Python/doc/en/html/man3/")
    else:
        dstroot = os.path.expanduser("~/.local/doc/en/html/man3/")
    dstroot = os.path.normpath(dstroot) + os.sep

    try:
        os.makedirs(dstroot)
    except:
        pass

    if os.path.exists(dst0):
        if os.path.exists(dstroot + str(_NAME)):
            shutil.rmtree(dstroot + str(_NAME))
        shutil.copytree(dst0, dstroot + str(_NAME))

    src0 = os.path.normpath("build/apidoc/sphinx/_build/html")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".sphinx"):
            shutil.rmtree(dstroot + str(_NAME) + ".sphinx")
        shutil.copytree(src0, dstroot + str(_NAME) + ".sphinx")

    src0 = os.path.normpath("build/apidoc/epydoc")
    if os.path.exists(src0):
        if os.path.exists(dstroot + str(_NAME) + ".epydoc"):
            shutil.rmtree(dstroot + str(_NAME) + ".epydoc")
        shutil.copytree(src0, dstroot + str(_NAME) + ".epydoc")

    print("#")
    idx = 0
    for i in sys.argv:
        if i == 'install_doc': break
        idx += 1

    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    sys.argv.remove('install_doc')

# call of complete test suite by 'discover'
if 'tests' in sys.argv or 'test' in sys.argv:
    if os.path.dirname(__file__) + os.pathsep not in os.environ['PATH']:
        p0 = os.path.dirname(__file__)
        os.putenv('PATH', p0 + os.pathsep + os.getenv('PATH', ''))
        print("# putenv:PATH[0]=" + str(p0))
    print("#")
    print("# Test - call in: tests")
    if version in ('2.6',):  # pragma: no cover
        exit_code += os.system(
            'python -m discover -s tests -p CallCase.py')  # traverse tree
    elif version in ('2.7',):  # pragma: no cover
        exit_code += os.system(
            'python -m unittest discover -s tests -p CallCase.py')  # traverse tree
    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    try:
        sys.argv.remove('test')
    except:
        pass
    try:
        sys.argv.remove('tests')
    except:
        pass

# call of complete UseCases by 'discover'
if 'usecases' in sys.argv or 'usecase' in sys.argv:
    if os.path.dirname(__file__) + os.pathsep not in os.environ['PATH']:
        p0 = os.path.dirname(__file__)
        os.putenv('PATH', p0 + os.pathsep + os.getenv('PATH', ''))
        print("# putenv:PATH[0]=" + str(p0))
    print("#")
    print("# Check 'inspect' paths - call in: UseCases")
    if version in ('2.6',):  # pragma: no cover
        exit_code = os.system(
            'python -m discover -s UseCases -p CallCase.py')  # traverse tree
    elif version in ('2.7',):  # pragma: no cover
        exit_code = os.system(
            'python -m unittest discover -s UseCases -p CallCase.py')  # traverse tree
    print("#")
    print("Called/Finished PyUnit tests => exit=" + str(exit_code))
    print("exit setup.py now: exit=" + str(exit_code))
    try:
        sys.argv.remove('usecase')
    except:
        pass
    try:
        sys.argv.remove('usecases')
    except:
        pass

# Intentional HACK: ignore (online) dependencies, mainly foreseen for developement
__no_install_requires = False
if '--no-install-requires' in sys.argv:
    __no_install_requires = True
    sys.argv.remove('--no-install-requires')

# Intentional HACK: offline only, mainly foreseen for developement
__offline = False
if '--offline' in sys.argv:
    __offline = True
    __no_install_requires = True
    sys.argv.remove('--offline')

# Execution failed - Error.
if exit_code != 0:
    sys.exit(exit_code)

# Help on addons.
if '--help-jsondata' in sys.argv:
    usage()
    sys.exit(0)

# Exit here.
if '--exit' in sys.argv:
    sys.exit(0)

# if jsondata-specials only
if len(sys.argv) == 1:
    sys.exit(exit_code)

if __debug__:
    print("#---------------------------------------------------------")
    print("packages=" + str(_packages))
    print("#---------------------------------------------------------")
    print("package_data=" + str(_package_data))
    print("#---------------------------------------------------------")

# Intentional HACK: ignore (online) dependencies, mainly foreseen for developement
if __no_install_requires:
    print("#")
    print("# Changed to offline mode, ignore install dependencies completely.")
    print("# Requires appropriate PYTHONPATH.")
    print("# Ignored dependencies are:")
    print("#")
    for ir in _install_requires:
        print("#   " + str(ir))
    print("#")
    _install_requires = []


setup(name=_name,
      version=__version__,
      author=__author__,
      author_email=__author_email__,
      classifiers=_classifiers,
      description=_description,
      download_url=_download_url,
      install_requires=_install_requires,
      keywords=_keywords,
      license=__license__,
      long_description=_long_description,
      platforms=_platforms,
      url=_url,
      scripts=_scripts,
      packages=_packages,
      package_data=_package_data
      )

if '--help' in sys.argv:
    print()
    print("Help on usage extensions by " + str(_NAME))
    print("   --help-" + str(_NAME))
    print()
