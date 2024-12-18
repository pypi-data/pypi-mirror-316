from setuptools import setup, find_packages

setup(
    name="priority-manager",
    version="0.1.0",
    description="A CLI tool for managing tasks with priorities and statuses.",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "click",
        "PyYAML"
    ],
    entry_points={
        "console_scripts": [
            "priority-manager=priority_manager.main:cli"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
