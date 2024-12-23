# filepath: /c:/Users/Qapitol QA/Desktop/QapitolApp/setup.py
from setuptools import setup, find_packages

setup(
    name="QapitolApp",
    version="0.4.0",
    author="Abinash Sahoo",
    author_email="abinash.sahoo@qapitol.com",
    description="For internal use only",
    packages=find_packages(),  # Automatically finds your packages
    include_package_data=True,
    install_requires=open('FLASK/requirements.txt').read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "flask_app=FLASK.__init__:create_app",
        ],
    },
)