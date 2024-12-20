from setuptools import setup, find_packages


with open("README.md" ,"r") as f:
    description_long = f.read()

setup(
    name="smuls",
    version="0.1.0",
    author="Sam_x",
    description="A brief description of your package",
    long_description=description_long,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],  # Add dependencies here
        entry_points={
        "console_scripts":[
            "smul = smul:hello",
        ],
    },
)
