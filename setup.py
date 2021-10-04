from setuptools import setup, find_packages

# README read-in
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()
# END README read-in

setup(
    name='timetrackerctl',
    version='0.1.0',
    packages=find_packages(),
    description='Opinionated Tempo time-tracking toolset',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/Parakoopa/timetrackerctl',
    author='Parakoopa',
    license='MIT',
    install_requires=[
        'jira>=2.0.0',
        'tempo-api-python-client>=0.4.1',
        'todoist-python>=8.1.1',
        'google-api-python-client>=2.21.0',
        'google-auth-httplib2>=0.1.0',
        'google-auth-oauthlib>=0.4.6',
        'PyGithub>=1.54.1'
        'appdirs>=1.4',
        'python-dateutil>=2.8',
        'Click>=8.0',
        'PyInquirer>=1.0.3',
        'pyyaml>=5.4.1',
        'PrettyTable>=2.2.0',
        'zenipy>=0.1.5',
        'pygobject>=3.26.0',
        'python-rofi @ git+https://github.com/Parakoopa/python-rofi.git@master#egg=python-rofi'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    entry_points='''
            [console_scripts]
            timetrackerctl=timetrackerctl.console.main:cli
            tt=timetrackerctl.console.main:cli
        ''',
)
