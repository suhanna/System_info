import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="system_info",
    version="2.0.1",
    author="Suhanna CH",
    author_email="suhanna52@gmail.com",
    description="Package for finding system hardware specifications",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/suhanna/System_info",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['py-cpuinfo>=6.0.0', 'psutil'],
)
