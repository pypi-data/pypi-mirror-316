from setuptools import setup

setup(
    name='tgcodes',
    version='0.1.2',
    description='API Client for https://gateway.telegram.org/.',
    author='nesquikcode',
    author_email='nesquik@nishine.ru',
    url='https://github.com/nesquikcode/TGCodes',
    packages=['tgcodes'],
    install_requires=[
        'requests',
    ],
    license='MIT'
)