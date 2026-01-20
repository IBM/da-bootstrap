# Guide: Deploying Deployable Architecture via IBM Cloud Projects

## Overview

This guide provides detailed instructions for deploying Deployable Architectures using IBM Cloud Projects service. Projects provide enterprise-grade deployment capabilities with compliance scanning, multi-stack management, and lifecycle governance.

## Prerequisites

- Deployable Architecture published in IBM Cloud Private Catalog
- IBM Cloud account with Projects service access
- Required IAM permissions for target resources
- Understanding of compliance requirements (if applicable)
- Access to the catalog containing the DA

## When to Use Projects

- Enterprise deployments with governance
- Compliance and security requirements
- Multi-stack architectures
- Environment management (dev, staging, prod)
- Automated compliance scanning
- Team collaboration with approval workflows

## Projects vs Schematics

**IBM Cloud Projects provides:**
- Compliance scanning and validation
- Multi-configuration deployments
- Approval workflows
- Environment management
- Enhanced security controls
- Integrated compliance reporting

**Schematics provides:**
- Simple Terraform execution
- Basic state management
- Single workspace deployments

## Steps

### 1. Access IBM Cloud Projects

1. Log in to [IBM Cloud Console](https://cloud.ibm.com)
2. Navigate to **Menu** → **Projects**
3. Or search for "Projects" in the top search bar

### 2. Create or Select Project

#### Create New Project

1. Click **Create project**
2. Provide project details:
   - **Project name**: Descriptive name
   - **Description**: Purpose and scope
   - **Resource group**: Target resource group
   - **Location**: Geographic location
3. Configure project settings:
   - **Compliance profiles**: Select applicable profiles
   - **Approval workflow**: Enable if required
   - **Notifications**: Configure alerts
4. Click **Create**

#### Use Existing Project

1. Select existing project from list
2. Verify project settings match requirements
3. Check compliance configuration

### 3. Add Deployable Architecture to Project

1. In your project, click **Create** or **Add**
2. Select **From catalog**
3. Find your Deployable Architecture:
   - Browse private catalog
   - Search by name or keywords
   - Filter by tags or provider
4. Click on the DA to view details

### 4. Review DA Details

Before configuring:
- **Overview**: Features and description
- **Architecture**: Diagram and components
- **Compliance**: Required profiles and controls
- **IAM permissions**: Required roles
- **Versions**: Available versions

### 5. Configure Deployment

#### Basic Configuration

1. **Configuration name**: Provide descriptive name
2. **Version**: Select DA version to deploy
3. **Flavor**: Choose deployment flavor (if multiple available)
4. **Location**: Select target region

#### Input Variables

1. Review all required variables
2. Provide values for each variable:
   - **String**: Text values
   - **Number**: Numeric values
   - **Boolean**: true/false
   - **List**: Array of values
   - **Map**: Key-value pairs
   - **Object**: Complex structures
3. Mark sensitive values appropriately
4. Use variable sets for reusable values

#### Advanced Settings

1. **Working directory**: Verify correct path
2. **Terraform version**: Confirm version
3. **Dependencies**: Configure if multi-stack
4. **Approval required**: Enable manual approval
5. **Auto-deploy**: Configure automatic deployment

### 6. Configure Compliance (If Applicable)

1. **Select profiles**: Choose compliance frameworks
   - IBM Cloud Framework for Financial Services
   - CIS IBM Cloud Foundations Benchmark
   - NIST
   - Custom profiles
2. **Scan settings**: Configure scan frequency
3. **Thresholds**: Set pass/fail criteria
4. **Remediation**: Configure auto-remediation

### 7. Validate Configuration

1. Click **Validate** button
2. Projects performs:
   - Terraform plan generation
   - Syntax validation
   - Compliance pre-scan
   - Dependency checks
3. Review validation results:
   - Plan output
   - Resource changes
   - Compliance findings
   - Warnings and errors
4. Fix any issues and re-validate

### 8. Deploy Configuration

#### Manual Deployment

1. Click **Deploy** button
2. Review deployment summary
3. Confirm deployment
4. Monitor deployment progress:
   - Real-time logs
   - Resource creation status
   - Compliance scanning
   - Error messages

#### Approval Workflow (If Enabled)

1. Submit deployment for approval
2. Approvers receive notification
3. Approvers review:
   - Configuration details
   - Compliance results
   - Resource changes
4. Approve or reject deployment
5. Deployment proceeds after approval

#### Automated Deployment

If auto-deploy is configured:
1. Deployment starts automatically after validation
2. Monitor progress in project dashboard
3. Review completion status

### 9. Monitor Deployment

1. **Activity tab**: View deployment progress
2. **Logs**: Review detailed execution logs
3. **Resources**: Track created resources
4. **Compliance**: Monitor compliance scanning
5. **Status**: Check overall deployment status

### 10. Review Deployment Results

After successful deployment:

1. **Outputs tab**: Review output values
2. **Resources tab**: View created resources
3. **Compliance tab**: Check compliance results
4. **Costs tab**: Review estimated costs
5. **Activity tab**: View deployment history

## Managing Deployments

### View Configurations

1. Navigate to project
2. View all configurations in project
3. Check status of each configuration
4. Review compliance posture

### Update Configuration

To update an existing configuration:

1. Select configuration in project
2. Click **Edit**
3. Update variable values
4. Click **Validate**
5. Review changes
6. Click **Deploy**

### Upgrade to New Version

To upgrade to a newer DA version:

1. Select configuration
2. Click **Edit**
3. Change version selection
4. Review breaking changes
5. Update variables if needed
6. Validate and deploy

### Manage Multiple Environments

For dev/staging/prod environments:

1. Create separate configurations in same project
2. Use different variable values per environment
3. Configure dependencies between environments
4. Use approval workflows for production
5. Promote configurations across environments

### Destroy Resources

To remove deployed resources:

1. Select configuration
2. Click **Actions** → **Destroy**
3. Review resources to be destroyed
4. Confirm destruction
5. Monitor destruction logs
6. Optionally remove configuration from project

## Compliance Management

### View Compliance Results

1. Navigate to **Compliance** tab
2. Review scan results:
   - Overall compliance score
   - Failed controls
   - Passed controls
   - Exemptions
3. Drill down into specific findings
4. Review remediation recommendations

### Remediate Findings

1. Review failed controls
2. Update configuration to address issues
3. Re-validate and re-deploy
4. Verify compliance improvement

### Configure Exemptions

For accepted risks:

1. Select failed control
2. Click **Create exemption**
3. Provide justification
4. Set expiration date
5. Submit for approval (if required)

## State Management

- State managed by IBM Cloud Projects service
- Separate state per configuration
- State encrypted at rest
- State accessible to authorized users
- Automatic state locking
- State versioning and history

## Troubleshooting

### Common Issues

**Deployment Failures**
- Check IAM permissions for all services
- Verify variable values and types
- Review error logs in activity tab
- Check resource quotas and limits
- Validate network connectivity

**Compliance Failures**
- Review failed controls
- Check resource configurations
- Verify security settings
- Update compliance profiles
- Request exemptions if needed

**Validation Errors**
- Check Terraform syntax
- Verify provider versions
- Validate variable constraints
- Review dependency configurations
- Check working directory path

**Approval Workflow Issues**
- Verify approvers are configured
- Check notification settings
- Review approval permissions
- Confirm workflow is enabled

**Version Conflicts**
- Check Terraform version compatibility
- Verify provider version requirements
- Review module version constraints
- Update version specifications

## Best Practices

### Project Organization
- Use separate projects for different applications
- Group related configurations in same project
- Use consistent naming conventions
- Tag projects and configurations
- Document project purpose

### Configuration Management
- Use descriptive configuration names
- Document variable purposes
- Use variable sets for common values
- Version control configuration changes
- Test in non-production first

### Compliance
- Enable compliance scanning early
- Address findings promptly
- Document exemptions clearly
- Review compliance regularly
- Keep profiles up to date

### Security
- Use least privilege IAM permissions
- Protect sensitive variables
- Enable approval workflows for production
- Audit deployment activities
- Rotate credentials regularly

### Lifecycle Management
- Plan for updates and upgrades
- Test changes in lower environments
- Use blue-green deployments
- Maintain rollback procedures
- Document deployment processes

## Multi-Stack Deployments

For complex architectures with dependencies:

### Configure Dependencies

1. Deploy foundation stack first
2. Configure dependent stacks to reference outputs
3. Set up dependency relationships
4. Deploy in correct order
5. Validate dependencies

### Manage Stack Lifecycle

1. Update foundation stacks carefully
2. Propagate changes to dependent stacks
3. Coordinate updates across stacks
4. Test dependencies thoroughly
5. Plan for stack removal

## Next Steps

- Set up monitoring and alerting
- Configure backup and disaster recovery
- Implement CI/CD pipelines
- Review [Guide: Running Terraform with IBM Cloud Schematics](./running-terraform-with-schematics.md) for workspace details
- Explore Projects API for automation

## Additional Resources

- [IBM Cloud Projects Documentation](https://cloud.ibm.com/docs/secure-enterprise?topic=secure-enterprise-understanding-projects)
- [Deployable Architectures Documentation](https://cloud.ibm.com/docs/secure-enterprise?topic=secure-enterprise-understand-module-da)
- [Security and Compliance Center](https://cloud.ibm.com/docs/security-compliance)
- [IBM Cloud IAM Documentation](https://cloud.ibm.com/docs/account?topic=account-iamoverview)