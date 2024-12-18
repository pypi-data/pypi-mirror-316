from setuptools import setup, find_packages

setup(
    name='modelAfroz',  # The name of the package
    version='0.1',
    packages=find_packages(),  # Find all packages inside the directory
    install_requires=[
        'requests',  # Dependency for downloading files from URLs
    ],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
