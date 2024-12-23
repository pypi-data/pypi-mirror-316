from setuptools import setup, find_packages

setup(
    name='tea-oss-todo',
    version='0.1.0',
    description='A simple To-Do list API using Flask for Tea OSS.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Clafa',
    author_email='rafaisyadwiadrianto@gmail.com',
    url='https://github.com/clafa30/tea-oss-todo',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'Flask>=2.0.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
