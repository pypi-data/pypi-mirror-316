from setuptools import setup

setup(
    name="image-serve-python",
    version="1.0.0",
    packages=["image-serve-python"],  # Correct package name
    install_requires=["requests"],
    description="A Python package for effortless image uploads and management via the ImageServe API, ensuring seamless integration for your applications.",
    long_description="A simple package for uploading images with API key authentication.",
    author="IP Softech - Pratham Pansuriya",
    author_email="ipsoftechsolutions@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)

