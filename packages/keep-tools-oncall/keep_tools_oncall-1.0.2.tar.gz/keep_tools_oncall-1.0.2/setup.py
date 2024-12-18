from setuptools import setup

setup(
    name='keep_tools_oncall',
    version='1.0.2',
    description='keep tools',
    author='dolmo',
    readme = "README.md",
    author_email='chengtianran@kuaishou.com',
    py_modules=['onCall'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        oc=onCall:oc
    ''',
)