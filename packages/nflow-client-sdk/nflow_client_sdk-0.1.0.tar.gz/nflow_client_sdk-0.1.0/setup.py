from setuptools import setup, find_packages

setup(
    name="nflow-client-sdk",            # Package name
    version="0.1.0",                    # Initial version
    packages=find_packages(),           # Automatically find package modules
    include_package_data=True,          # Include non-code files specified in MANIFEST.in
    description="A private SDK for nFlow client pipelines.",
    long_description=open("README.md").read(),  # Optional long description
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="youremail@example.com",
    url="https://example.com",          # Replace with your project homepage
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
