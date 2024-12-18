from setuptools import setup, find_packages

setup(
    name="license_bb",
    version="0.1.0",
    author="Ambadas Dannak",
    author_email="ambadas@mollatech.com",
    description="A description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/my_package",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests', 'python-dateutil', 'schedule==1.2.2', 'cryptography==42.0.8', 'tzlocal==5.2'
    ],
    python_requires='>=3.8',
)