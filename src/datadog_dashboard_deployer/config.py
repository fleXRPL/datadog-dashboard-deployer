"""
Configuration parsing and validation module.
"""

import logging
import os
from typing import Any, Dict

import yaml
from jsonschema import ValidationError, validate

logger = logging.getLogger(__name__)

# Schema for dashboard configuration validation
DASHBOARD_SCHEMA = {
    "type": "object",
    "required": ["version", "dashboards"],
    "properties": {
        "version": {"type": "string"},
        "defaults": {
            "type": "object",
            "properties": {
                "layout_type": {"type": "string", "enum": ["ordered", "free"]},
                "refresh_interval": {"type": "integer", "minimum": 0},
                "tags": {"type": "array", "items": {"type": "string"}},
            },
        },
        "dashboards": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name", "widgets"],
                "properties": {
                    "name": {"type": "string"},
                    "description": {"type": "string"},
                    "layout_type": {"type": "string", "enum": ["ordered", "free"]},
                    "tags": {"type": "array", "items": {"type": "string"}},
                    "widgets": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["title", "type"],
                            "properties": {
                                "title": {"type": "string"},
                                "type": {"type": "string"},
                                "query": {"type": "string"},
                                "size": {"type": "string"},
                                "visualization": {"type": "object"},
                                "conditional_formats": {
                                    "type": "array",
                                    "items": {"type": "object"},
                                },
                                "custom_links": {
                                    "type": "array",
                                    "items": {"type": "object"},
                                },
                            },
                        },
                    },
                    "template_variables": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "required": ["name"],
                            "properties": {
                                "name": {"type": "string"},
                                "prefix": {"type": "string"},
                                "default": {"type": "string"},
                            },
                        },
                    },
                },
            },
        },
    },
}


class ConfigParser:
    """Parser for dashboard configuration files."""

    def __init__(self, config_path: str):
        """
        Initialize the configuration parser.

        Args:
            config_path: Path to the YAML configuration file
        """
        self.config_path = config_path
        self._validate_path()

    def _validate_path(self) -> None:
        """Validate that the configuration file exists and is readable."""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        if not os.path.isfile(self.config_path):
            raise ValueError(f"Configuration path is not a file: {self.config_path}")
        if not os.access(self.config_path, os.R_OK):
            raise PermissionError(f"Cannot read configuration file: {self.config_path}")

    def parse(self) -> Dict[str, Any]:
        """
        Parse and validate the configuration file.

        Returns:
            Dict containing the parsed configuration
        """
        try:
            with open(self.config_path, "r") as f:
                config = yaml.safe_load(f)

            # Validate against schema
            self._validate_config(config)

            # Apply defaults
            self._apply_defaults(config)

            logger.info(f"Successfully parsed configuration from {self.config_path}")
            return config

        except yaml.YAMLError as e:
            logger.error(f"Failed to parse YAML configuration: {e}")
            raise
        except Exception as e:
            logger.error(f"Error processing configuration: {e}")
            raise

    def _validate_config(self, config: Dict) -> None:
        """
        Validate configuration against schema.

        Args:
            config: Configuration dictionary to validate
        """
        try:
            validate(instance=config, schema=DASHBOARD_SCHEMA)
        except ValidationError as e:
            logger.error(f"Configuration validation failed: {e.message}")
            raise

    def _apply_defaults(self, config: Dict) -> None:
        """
        Apply default values to dashboard configurations.

        Args:
            config: Configuration dictionary to update
        """
        defaults = config.get("defaults", {})
        for dashboard in config["dashboards"]:
            # Apply layout type
            if "layout_type" not in dashboard and "layout_type" in defaults:
                dashboard["layout_type"] = defaults["layout_type"]

            # Apply tags
            if "tags" in defaults:
                dashboard_tags = set(dashboard.get("tags", []))
                dashboard_tags.update(defaults["tags"])
                dashboard["tags"] = list(dashboard_tags)

            # Apply refresh interval
            if "refresh_interval" in defaults:
                dashboard["refresh_interval"] = defaults["refresh_interval"]
