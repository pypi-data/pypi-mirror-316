from setuptools import setup, find_packages

setup(
    name="pganalytics",
    version="0.5.0",
    author="pgcass",
    author_email="cansin@pronetgaming.com",
    description="A Python library for analyzing PG data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(include=["pganalytics", "pganalytics.*"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pandas>=2.1.2,<2.2",
        "google-cloud-bigquery>=3.4.0,<3.21.0",
        "xgboost>=1.5.0",
        "scikit-learn>=1.0.0",
        "pyyaml>=5.4.0",
        "google-generativeai>=0.1.0",
        "db-dtypes>=1.0.0",
        "xlsxwriter>=1.3.0",
        "apache-airflow>=2.5.0,<2.6.0"
    ],
)