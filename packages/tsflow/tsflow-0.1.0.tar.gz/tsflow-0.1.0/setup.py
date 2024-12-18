from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()
    
setup(
    name='tsflow',
    version='0.1.0',
    description='Python package for searching transition states and generating reaction complexes',
    long_description=long_description,
    url='https://github.com/kyunghoonlee777/pyMCD2.git',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'mcd=tsflow.run:main',
        ],
    },
    install_requires=[
        'numpy',
        'scipy>=1.11.0',
        'cclib>=1.8.1',
        'rdkit',
        'matplotlib',
    ],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)