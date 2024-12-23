from setuptools import setup, find_packages

setup(
    name='fast_trans_obj',
    version='0.0.6',
    packages=find_packages(),
    install_requires=['asyncio'],
    author='cg_now',
    author_email='1939296965@qq.com',
    description='A simple tools to trans obj to rpc',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.1',
)
