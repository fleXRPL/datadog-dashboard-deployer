# Configuration Examples

This directory contains example configurations for the DataDog Dashboard Deployer. These examples demonstrate various features and use cases of the tool.

## Available Examples

### 1. Basic Configuration (`examples/basic.yaml`)
A simple configuration demonstrating:
- Basic dashboard structure
- Essential system metrics
- Common widget types

### 2. Advanced Configuration (`examples/advanced.yaml`)
Demonstrates advanced features including:
- Global defaults
- Template variables
- Widget templates
- Multiple dashboards
- Conditional formatting

### 3. Application Monitoring (`examples/application.yaml`)
Shows how to configure:
- Web application metrics
- Performance monitoring
- Error tracking
- User analytics

## Usage

1. Copy an example configuration:
   ```bash
   cp examples/basic.yaml my-dashboard.yaml
   ```

2. Modify the configuration for your needs:
   ```yaml
   dashboards:
     - name: "My Dashboard"
       description: "My custom dashboard"
       # ... rest of configuration
   ```

3. Deploy the dashboard:
   ```bash
   datadog-dashboard-deploy my-dashboard.yaml
   ```

## Best Practices

1. **Organization**
   - Use meaningful dashboard and widget names
   - Group related metrics together
   - Include clear descriptions

2. **Templates**
   - Use templates for common widget patterns
   - Define global defaults where appropriate
   - Leverage template variables for flexibility

3. **Performance**
   - Keep queries efficient
   - Use appropriate time aggregations
   - Consider dashboard load time

## Additional Resources

- [Configuration Guide](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Configuration-Guide)
- [Dashboard Examples](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Dashboard-Examples)
- [Best Practices](https://github.com/fleXRPL/datadog-dashboard-deployer/wiki/Best-Practices) 