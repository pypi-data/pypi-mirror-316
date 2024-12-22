from setuptools import setup, find_packages

setup(
    name='telugu_phenome_gen',
    version='0.1.0',
    author='RAVINDRA CHOWDARY JONNAGADLA',
    description='A package for converting Telugu text to phonetic representations in English.',
    long_description_content_type='text/markdown',
    url='https://github.com/RAVINDRA8008/TELUGU-PHENOME-TO-ENGLISH',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        # Add any package dependencies here
    ],
)