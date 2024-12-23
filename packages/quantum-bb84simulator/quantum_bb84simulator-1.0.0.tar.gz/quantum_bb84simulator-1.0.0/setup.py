from setuptools import setup, find_packages

setup(
    name='quantum_bb84simulator',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'qiskit>=0.37.0',  # Specify minimum version for compatibility
        'matplotlib>=3.5.0',
        'numpy>=1.21.0'
    ],
    extras_require={
        'dev': ['pytest', 'pytest-cov', 'sphinx'],  # Development tools
    },
    description='A comprehensive Python library for simulating the BB84 quantum key distribution protocol.',
    long_description=open('README.md', 'r', encoding='utf-8').read(),  # Read long description from README
    long_description_content_type='text/markdown',  # Specify the format of the README
    author='Syon Balakrishnan',
    author_email='balakrishnansyon@gmail.com',
    url='',  # Replace with your GitHub repo
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Physics',
        'Topic :: Scientific/Engineering :: Information Analysis',
    ],
    python_requires='>=3.8',  # Specify the minimum Python version
    entry_points={
        'console_scripts': [
            'run-bb84=examples.run_bb84:main',  # Example CLI entry point
        ],
    },
)
