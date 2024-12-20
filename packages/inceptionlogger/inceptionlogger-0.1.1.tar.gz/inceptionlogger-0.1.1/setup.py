from setuptools import setup, find_packages

setup(
    name="inceptionlogger",
    version="0.1.1",   # Package version
    author="KhaduaBloom",
    author_email="khaduabloom@gmail.com",
    description="inceptionlogger is a package that allows you to log your application to graylog",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/KhaduaBloom/inceptionforcepackages/tree/main/PythonPackage/inceptionlogger",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.13.0",
    install_requires=[
        "graypy==2.1.0",
        "psutil==6.1.0",
        "fastapi",
        "uvicorn",
        "pydantic-settings",
    ],
)
