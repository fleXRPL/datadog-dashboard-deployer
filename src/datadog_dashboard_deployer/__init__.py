"""
DataDog Dashboard Deployer - A framework for deploying DataDog dashboards as code.
"""

__version__ = "0.1.0"
__author__ = "fleXRPL"
__license__ = "MIT"

from .config import ConfigParser
from .core import DashboardDeployer
from .utils import setup_logging

__all__ = ["DashboardDeployer", "ConfigParser", "setup_logging"]
