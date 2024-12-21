from setuptools import setup, find_packages

setup(
    name='scraply',
    version='1.0.2',
    packages=find_packages(),
    description='A Python package to scrape and clone websites.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Fidal',
    author_email='mrfidal@proton.me',
    url='https://github.com/ByteBreach/scraply',
    install_requires=[
        'requests',
        'beautifulsoup4'
    ],
    entry_points={
        'console_scripts': [
            'scraply = scraply.cli:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
