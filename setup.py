from setuptools import setup

setup(
    name="py-check-imports",
    version="1.1.0",
    py_modules=["py_check_imports"],
    install_requires=[],
    entry_points={
        "console_scripts": [
            "py-check-imports=py_check_imports:main"
        ]
    },
    author="Sacha Wheeler",
    description="Scan Python scripts or directories for unused and duplicate imports.",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
