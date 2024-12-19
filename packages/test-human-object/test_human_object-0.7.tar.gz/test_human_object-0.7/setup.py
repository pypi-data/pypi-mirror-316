from setuptools import setup, find_packages

setup(
    name="test_human_object",  # Replace with your package name
    version="0.7",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],  # Any dependencies your package needs (e.g., ['numpy'])
    long_description_content_type="text/markdown",  # Use markdown for your README
    author="Your Name",
    author_email="your.email@example.com",
    description="A short description of your package",
    url="https://github.com/yourusername/my_package",  # Your project URL
    classifiers=[  # These help people discover your package
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Specify the license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
