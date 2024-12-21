from setuptools import setup, find_packages

setup(
    name='web-scraper-tool',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'requests',
        'beautifulsoup4',
        'selenium',
        'webdriver-manager',
    ],
    entry_points={
        'console_scripts': [
            'web-scraper-tool=web_scraper_tool.scraper:main',
        ],
    },
    author='hdd5ps',
    author_email='hdd5ps@virginia.edu',
    description='A web scraper tool to extract data from e-commerce websites',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hdd5ps/web-scraper-tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)