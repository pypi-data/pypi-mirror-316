from setuptools import setup, find_packages

setup(
    name="QapitolApp",                    
    version="0.2.0",                     # Version of your app
    author="Abinash Sahoo",                  # Author name
    author_email="abinash.sahoo@qapitol.com",# Author email
    description="For internal use only", # Short description of your app
    packages=find_packages(where="FLASK"),  # Automatically finds your packages inside the FLASK directory
    include_package_data=True,             # Include extra files like static, templates, etc.
    install_requires=open('FLASK/requirements.txt').read().splitlines(),  # Dependencies
    classifiers=[                        # Optional: Classifiers for PyPi
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",               # Python version requirement
    entry_points={                         # Optional: if you want to create command-line tools
        "console_scripts": [
            "flask_app=FLASK.__init__:create_app",  # Command to run your app
        ],
    },
)
