from distutils.core import setup
import py2exe

NAME = 'cmdr'
VERSION = '0.1.0'

setup(
    name=NAME,
    version=VERSION,
    author='Wisen Tanasa',
    url='https://github.com/ceilfors/command-reservoir',
    license='BSD',
    packages=['cmdr'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ],
    console=[{
        'script': 'main.py',
        'dest_base': NAME
    }],
    options={
        'py2exe': {
            'bundle_files': 1
        }
    },
    zipfile=None
)