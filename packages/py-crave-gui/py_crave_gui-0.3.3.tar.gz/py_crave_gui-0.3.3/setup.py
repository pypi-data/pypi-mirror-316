from setuptools import setup, find_packages

setup(
    name="py-crave-gui",  # Name of the package
    version="0.3.3",  # Update the version to 0.3
    packages=find_packages(),
    install_requires=[
        'py-crave-sync',  # Add the new dependency
    ],
    author="Julox Games",
    description="A GUI library with customizable components for Python.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
