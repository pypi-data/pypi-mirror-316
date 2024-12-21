from setuptools import setup, find_packages

setup(
    name="AB_library",
    version="0.1.0",
    packages=find_packages(),
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    description="AB Testing library",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'seaborn',
        'statsmodels',
        'tqdm'
    ],
)