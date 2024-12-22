from setuptools import setup, find_packages

setup(
    name="nflow",                    # Change this to "nflow"
    version="0.1.0",
    packages=find_packages(),        # Automatically find package modules
    include_package_data=True,
    description="A Python SDK for nFlow client pipelines.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://example.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "tqdm>=4.0",  # Example dependency
    ],
)
