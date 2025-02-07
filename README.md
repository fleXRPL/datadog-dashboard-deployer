# DataDog Dashboard Deployer

A powerful framework for deploying DataDog dashboards as code using CI/CD pipelines. Define, version, and automate your DataDog dashboard deployments using YAML configurations.

#### versions

[![PyPI version](https://badge.fury.io/py/datadog-dashboard-deployer.svg)](https://badge.fury.io/py/datadog-dashboard-deployer))
[![PyPI version](https://img.shields.io/pypi/v/datadog-dashboard-deployer.svg)](https://pypi.org/project/datadog-dashboard-deployer/)
[![Python](https://img.shields.io/pypi/pyversions/datadog-dashboard-deployer.svg)](https://pypi.org/project/datadog-dashboard-deployer/)

#### health

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-dashboard-deployerb&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-dashboard-deployerb)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-dashboard-deployerb&metric=coverage)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-dashboard-deployerb)
[![Security Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-dashboard-deployerb&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-dashboard-deployerb)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-dashboard-deployerb&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-dashboard-deployerb)
[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=fleXRPL_datadog-dashboard-deployerb&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=fleXRPL_datadog-dashboard-deployerb)
[![Dependabot Status](https://img.shields.io/badge/Dependabot-enabled-success.svg)](https://github.com/fleXRPL/datadog-dashboard-deployer/blob/main/.github/dependabot.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

#### stats

[![Downloads](https://pepy.tech/badge/datadog-dashboard-deployer)](https://pepy.tech/project/datadog-dashboard-deployer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- 🚀 **Configuration as Code**: Define dashboards using YAML configuration files
- 🔄 **Automated Deployment**: Deploy dashboards automatically via GitHub Actions
- 📊 **Rich Widget Support**: Support for timeseries, query values, heatmaps, and more
- 🔐 **Secure Credentials**: Handle DataDog API credentials securely
- 🎨 **Templating Support**: Create dynamic dashboards using Jinja2 templating
- 🔌 **Extensible Architecture**: Easy to extend and customize

## Quick Start

### Installation

```bash
pip install datadog-dashboard-deployer
```

### Basic Usage

1. Set up your DataDog credentials:

```bash
export DATADOG_API_KEY='your-api-key'
export DATADOG_APP_KEY='your-application-key'
```

2. Create a dashboard configuration:

```yaml
# config/dashboard_config.yaml
version: "1.0"
dashboards:
  - name: "System Overview"
    description: "System performance metrics"
    widgets:
      - title: "CPU Usage"
        type: "timeseries"
        query: "avg:system.cpu.user{*}"
      - title: "Memory Usage"
        type: "timeseries"
        query: "avg:system.mem.used{*}"
```

3. Deploy your dashboard:

```bash
datadog-dashboard-deploy config/dashboard_config.yaml
```

## Project Structure

```bash
datadog-dashboard-deployer/
├── src/
│   └── datadog_dashboard_deployer/
│       ├── __init__.py
│       ├── core.py       # Core logic for dashboard creation
│       ├── config.py     # Configuration handling
│       └── utils.py      # Utility functions
├── config/
│   └── dashboard_config.yaml  # Main dashboard configuration
├── .github/
│   └── workflows/
│       └── deploy.yml      # GitHub Actions workflow
├── tests/                  # Test suite
├── docs/                   # Documentation
├── requirements.txt        # Project dependencies
├── setup.py               # Package configuration
└── README.md
```

## Documentation

- [Getting Started Guide](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Getting-Started)
- [Configuration Guide](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Configuration-Guide)
- [API Reference](https://datadog-dashboard-deployer.readthedocs.io/)
- [Examples](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Examples)

## GitHub Actions Integration

1. Add DataDog credentials as secrets:

   - Go to repository Settings > Secrets and Variables > Actions
   - Add `DATADOG_API_KEY` and `DATADOG_APP_KEY`

2. Create a workflow file:

```yaml
# .github/workflows/deploy.yml
name: Deploy Dashboards
on:
  push:
    branches: [main]
  workflow_dispatch:

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.x"
      - name: Deploy dashboards
        env:
          DATADOG_API_KEY: ${{ secrets.DATADOG_API_KEY }}
          DATADOG_APP_KEY: ${{ secrets.DATADOG_APP_KEY }}
        run: |
          pip install datadog-dashboard-deployer
          datadog-dashboard-deploy config/dashboard_config.yaml
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Contributing) for details.

### Development Setup

1. Clone the repository:

```bash
git clone https://github.com/fleXRPL/datadog-dashboard-deployer.git
cd datadog-dashboard-deployer
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

## Security

- API keys are stored securely as environment variables or GitHub secrets
- Regular security audits and dependency updates
- See our [Security Policy](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Security) for details

## Support

- [GitHub Issues](https://github.com/fleXRPL/datadog-dashboard-deployer/issues) for bug reports and feature requests
- [GitHub Discussions](https://github.com/fleXRPL/datadog-dashboard-deployer/discussions) for questions and community support
- [Stack Overflow](https://stackoverflow.com/questions/tagged/datadog-dashboard-deployer) using the `datadog-dashboard-deployer` tag

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [DataDog](https://www.datadoghq.com/) for their excellent monitoring platform
- [datadogpy](https://github.com/DataDog/datadogpy) for the official Python client
- All our [contributors](https://github.com/fleXRPL/datadog-dashboard-deployer/graphs/contributors)
