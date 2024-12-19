from setuptools import setup, find_packages

setup(
    name="postmansub",
    version="0.1",
    description="A small package to sent post requests.",
    long_description=open("readme.md").read(),
    long_description_content_type="text/markdown",
    author="Benevant Mathew",
    license="MIT",
    packages=find_packages(include=["postmansub"]),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "postmansub = postmansub.main:create_gui",  # entry point
        ],
    },    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",        
    ],
    python_requires=">=3.7",
)
