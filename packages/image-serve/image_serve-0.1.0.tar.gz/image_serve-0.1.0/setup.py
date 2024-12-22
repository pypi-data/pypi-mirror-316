from setuptools import setup

setup(
    name="image-serve",
    version="0.1.0",
    packages=["image_serve"],  # Correct package name
    install_requires=["requests"],
    description="Python SDK for uploading images using the Image Uploader API.",
    long_description="A simple SDK for uploading images with API key authentication.",
    author="IP Softech - Pratham Pansuriya",
    author_email="ipsoftechsolutions@gmail.com",
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
    ],
)

