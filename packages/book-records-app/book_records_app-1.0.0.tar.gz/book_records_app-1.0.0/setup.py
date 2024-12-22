from setuptools import setup, find_packages

setup(
    name="book-records-app",
    version="1.0.0",
    author="Charlito C. Casalta",
    author_email="charlito320@gmail.com",
    description="A simple GUI application to manage book records using SQLite.",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "book-records=book_records.main:main",  # CLI command to launch app
        ],
    },
)