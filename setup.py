#! /usr/bin/env python3
"""
license: MIT, see LICENSE.txt
"""

from setuptools import setup

version = "0.2"


entry_points = {"console_scripts": []}
install_requirements = ["bottle"]


entry_points["console_scripts"].append(
    'mpv_simpleserver = mpv_simpleserver.__main__:main'
)

setup(
    name='mpv_simpleserver',
    version=version,
    # version_format='{tag}',
    description='Web server for mpv',
    author='Alexander K.',
    author_email='devkral@web.de',
    license='BSD-3',
    url='https://github.com/devkral/mpv_simpleserver',
    download_url='https://github.com/devkral/mpv_simpleserver/tarball/v%s' %
                 version,
    entry_points=entry_points,
    # zip_safe=True,
    platforms='Platform Independent',
    include_package_data=True,
    install_requires=install_requirements,
    packages=[
        "mpv_simpleserver", "mpv_simpleserver.mpv_simpleserver"
    ],

    classifiers=[
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX',
        'Environment :: Console',
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Education',
        'Intended Audience :: End Users/Desktop',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Sound/Audio :: Players'
    ],
    keywords=['mpv', 'helper', 'tool']
)
