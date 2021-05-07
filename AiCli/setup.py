from setuptools import setup

setup(
    name='myaws',
    version='0.8',
    py_modules=['myaws'],
    install_requires=[
        'Click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        myaws=myaws:cli
    ''',
)