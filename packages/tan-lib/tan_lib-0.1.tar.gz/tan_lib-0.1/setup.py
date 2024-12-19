# setup.py
from setuptools import setup, find_packages

setup(
    name='tan_lib',  # Name of your library
    version='0.1',  # Version of your library
    packages=find_packages(),
    install_requires=[],  # Any other libraries you may need
    test_suite='tests',  # Where your tests are
    author='Tanmay Dumbre',  # Your name
    author_email='tanmaymdumbrek@gmail.com',  # Your email
    description='A simple math library',  # Short description
    long_description=open('README.md').read(),  # Will write this next
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/tan_lib',  # URL (if you use GitHub)
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
