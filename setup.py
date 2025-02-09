"""
Setup configuration for the DataDog Dashboard Deployer package.
"""

from setuptools import find_packages, setup

# Read version from package
with open("src/datadog_dashboard_deployer/__init__.py", "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"')
            break

# Read README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="datadog-dashboard-deployer",
    version=version,
    description="A framework for deploying DataDog dashboards as code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="fleXRPL",
    author_email="support@flexrpl.com",
    url="https://github.com/fleXRPL/datadog-dashboard-deployer",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "datadog>=0.44.0",
        "PyYAML>=6.0",
        "click>=8.0.0",
        "jsonschema>=4.0.0",
    ],
    entry_points={
        "console_scripts": [
            "datadog-dashboard-deploy=datadog_dashboard_deployer.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: System :: Monitoring",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.9",
    keywords="datadog dashboard monitoring devops automation",
    project_urls={
        "Documentation": "https://github.com/fleXRPL/datadog-dashboard-deployer/wiki",
        "Source": "https://github.com/fleXRPL/datadog-dashboard-deployer",
        "Issues": "https://github.com/fleXRPL/datadog-dashboard-deployer/issues",
    },
)
