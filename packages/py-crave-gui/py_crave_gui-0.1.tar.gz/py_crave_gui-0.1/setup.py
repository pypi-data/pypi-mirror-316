from setuptools import setup, find_packages

setup(
    name="py-crave-gui",         # Name of your library
    version="0.1",               # Version of your library
    packages=find_packages(),    # Automatically find and include all packages
    install_requires=[],         # List dependencies (none for this case)
    long_description=open('README.md').read(),  # Read the content from README.md
    long_description_content_type='text/markdown',  # Format of README.md
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version
)
