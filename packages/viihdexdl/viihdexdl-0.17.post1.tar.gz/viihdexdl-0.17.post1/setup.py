from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name = 'viihdexdl',
    description = 'Command line tool for downloading HLS streams with FFmpeg',
    long_description = long_description,
    long_description_content_type='text/markdown',
    url = 'https://github.com/Qotscha/viihdexdl',
    author = 'Qotscha',
    version = '0.17.post1',
    packages = ['viihdexdl'],
    package_dir = {'viihdexdl': 'src'},
    install_requires = [
        'requests',
        'langcodes',
        ],
    entry_points = {
        'console_scripts': [
            'viihdexdl = viihdexdl.__main__:main'
            ]
        },
    classifiers = [
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Win32 (MS Windows)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3'
        ]
    )
