from setuptools import setup, find_packages

setup(
    name="datalib_btayari",  # Nom de votre package
    version="0.1.0",  # Version initiale
    author="Votre Nom",
    author_email="votre.email@example.com",
    description="A Python library for data manipulation and analysis",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/votre_nom_utilisateur/DataLib",  # URL du dépôt GitHub
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "matplotlib>=3.4.0",
        "scikit-learn>=0.24.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
