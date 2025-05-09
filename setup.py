from setuptools import setup, find_packages

setup(
    name='dir2json',
    version='0.1.0',
    description='A Python package to encode and decode directories to/from JSON.',
    author='Sam Parmar',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        # Add external dependencies here, e.g., 'requests', 'numpy'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'dir2json=dir2json.cli:main',
        ],
    },
)