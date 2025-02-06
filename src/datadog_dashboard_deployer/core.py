"""
Core module for DataDog dashboard deployment functionality.
"""

import logging
from typing import Dict, Optional

import datadog

from .config import ConfigParser
from .utils import setup_logging

logger = logging.getLogger(__name__)


class DashboardDeployer:
    """Main class for handling dashboard deployment operations."""

    def __init__(self, api_key: str, app_key: str, site: Optional[str] = None):
        """
        Initialize the dashboard deployer.

        Args:
            api_key: DataDog API key
            app_key: DataDog Application key
            site: Optional DataDog site (e.g., 'datadoghq.com', 'datadoghq.eu')
        """
        self.api_key = api_key
        self.app_key = app_key
        self.site = site or "datadoghq.com"
        self._initialize_client()
        setup_logging()

    def _initialize_client(self) -> None:
        """Initialize the DataDog API client."""
        try:
            datadog.initialize(
                api_key=self.api_key,
                app_key=self.app_key,
                api_host=f"https://api.{self.site}",
            )
            logger.info("Successfully initialized DataDog client")
        except Exception as e:
            logger.error(f"Failed to initialize DataDog client: {e}")
            raise

    def deploy(self, config_path: str, dry_run: bool = False) -> Dict:
        """
        Deploy dashboards based on configuration.

        Args:
            config_path: Path to the dashboard configuration YAML file
            dry_run: If True, validate but don't deploy

        Returns:
            Dict containing deployment results
        """
        try:
            # Parse configuration
            config = ConfigParser(config_path).parse()

            if dry_run:
                logger.info("Dry run - validating configuration only")
                return {"status": "validated", "dashboards": config["dashboards"]}

            results = []
            for dashboard in config["dashboards"]:
                result = self._deploy_dashboard(dashboard)
                results.append(result)

            return {"status": "success", "results": results}

        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            raise

    def _deploy_dashboard(self, dashboard_config: Dict) -> Dict:
        """
        Deploy a single dashboard.

        Args:
            dashboard_config: Dashboard configuration dictionary

        Returns:
            Dict containing deployment result
        """
        try:
            # Check if dashboard exists
            existing = self._get_dashboard_by_name(dashboard_config["name"])

            if existing:
                result = self._update_dashboard(existing["id"], dashboard_config)
                logger.info(f"Updated dashboard: {dashboard_config['name']}")
            else:
                result = self._create_dashboard(dashboard_config)
                logger.info(f"Created dashboard: {dashboard_config['name']}")

            return {
                "status": "success",
                "dashboard_id": result["id"],
                "name": dashboard_config["name"],
                "action": "update" if existing else "create",
            }

        except Exception as e:
            logger.error(f"Failed to deploy dashboard {dashboard_config['name']}: {e}")
            raise

    def _get_dashboard_by_name(self, name: str) -> Optional[Dict]:
        """
        Get dashboard by name.

        Args:
            name: Dashboard name

        Returns:
            Dashboard dict if found, None otherwise
        """
        try:
            dashboards = datadog.api.Dashboard.get_all()
            for dashboard in dashboards["dashboards"]:
                if dashboard["title"] == name:
                    return dashboard
            return None
        except Exception as e:
            logger.error(f"Failed to get dashboard {name}: {e}")
            raise

    def _create_dashboard(self, config: Dict) -> Dict:
        """
        Create a new dashboard.

        Args:
            config: Dashboard configuration

        Returns:
            Created dashboard response
        """
        try:
            return datadog.api.Dashboard.create(
                title=config["name"],
                description=config.get("description", ""),
                widgets=config["widgets"],
                layout_type=config.get("layout_type", "ordered"),
                template_variables=config.get("template_variables", []),
            )
        except Exception as e:
            logger.error(f"Failed to create dashboard: {e}")
            raise

    def _update_dashboard(self, dashboard_id: str, config: Dict) -> Dict:
        """
        Update an existing dashboard.

        Args:
            dashboard_id: ID of the dashboard to update
            config: New dashboard configuration

        Returns:
            Updated dashboard response
        """
        try:
            return datadog.api.Dashboard.update(
                dashboard_id,
                title=config["name"],
                description=config.get("description", ""),
                widgets=config["widgets"],
                layout_type=config.get("layout_type", "ordered"),
                template_variables=config.get("template_variables", []),
            )
        except Exception as e:
            logger.error(f"Failed to update dashboard: {e}")
            raise
