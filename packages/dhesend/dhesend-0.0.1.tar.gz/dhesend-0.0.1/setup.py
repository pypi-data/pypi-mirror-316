from setuptools import setup, find_packages

setup(
    name="dhesend",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "requests>=2.32.3"
    ],
    description="Dhesend Official Python SDK.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Dhesend",
    author_email="",
    url="https://github.com/dhesend/dhesend-python",
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ],
)