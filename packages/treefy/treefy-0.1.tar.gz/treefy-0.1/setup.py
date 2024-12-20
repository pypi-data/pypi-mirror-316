# setup.py

from setuptools import setup, find_packages

setup(
    name='treefy',  # Name of your package
    version='0.1',  # Version number
    packages=find_packages(),  # Automatically finds packages in the treefy directory
    install_requires=[],  # Add any required dependencies here (e.g., numpy, requests, etc.)
    author='Deven Kapadia',  # Your name or organization
    author_email='devenkapadia1@gmail.com',  # Your email address
    description='A dynamic tree library for algorithmic problem solving',  # Short description
    long_description=open('README.md').read(),  # Read the content of your README file
    long_description_content_type='text/markdown',  # Format of your README
    url='https://github.com/devenkapadia/treefy.git',  # Your GitHub repository URL
    classifiers=[
        'Programming Language :: Python :: 3',  # Python 3 support
        'License :: OSI Approved :: MIT License',  # License type
        'Operating System :: OS Independent',  # OS compatibility
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
