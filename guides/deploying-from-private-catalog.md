# Guide: Deploying from IBM Cloud Private Catalog

## Overview

This guide provides detailed instructions for deploying Terraform offerings that have been onboarded to IBM Cloud Private Catalog. This method provides a streamlined deployment experience with versioned, validated configurations.

## Prerequisites

- Terraform offering published in IBM Cloud Private Catalog
- IBM Cloud account with appropriate IAM permissions
- Access to the private catalog containing the offering
- Required resource permissions for target infrastructure

## When to Deploy from Catalog

- Using standardized, pre-validated configurations
- Deploying versioned offerings
- Following organizational governance policies
- Leveraging catalog-based discovery
- Ensuring consistent deployments across teams

## Steps

### 1. Access IBM Cloud Catalog

1. Log in to [IBM Cloud Console](https://cloud.ibm.com)
2. Navigate to **Catalog**
3. Filter by **Private** to see your organization's offerings
4. Or navigate directly to **Catalog** → **Private catalogs** → Select your catalog

### 2. Find Your Offering

1. Browse or search for your Terraform offering
2. Use filters to narrow results:
   - **Provider**: Filter by provider name
   - **Category**: Filter by category/tags
   - **Type**: Select "Terraform"
3. Click on the offering to view details

### 3. Review Offering Details

Before deploying, review:
- **Overview**: Description, features, and documentation
- **Architecture**: Diagrams and architecture details
- **About**: Version information and release notes
- **Required permissions**: IAM permissions needed

### 4. Create Deployment

1. Click **Create** or **Install** button
2. Configure deployment settings:
   - **Name**: Provide a name for this deployment
   - **Resource group**: Select target resource group
   - **Location**: Select geographic location
   - **Version**: Select offering version to deploy

### 5. Configure Variables

1. Fill in required variables:
   - Review variable descriptions
   - Provide values for all required fields
   - Optionally override default values
   - Mark sensitive values appropriately

2. Variable types:
   - **String**: Text values
   - **Number**: Numeric values
   - **Boolean**: true/false values
   - **List**: Array of values
   - **Map**: Key-value pairs
   - **Object**: Complex structured data

### 6. Review Configuration

1. Review the **Summary** section
2. Verify all settings and variable values
3. Review estimated costs (if available)
4. Check compliance requirements (if applicable)

### 7. Deploy

1. Accept terms and conditions (if required)
2. Click **Install** or **Create**
3. Deployment creates a Schematics workspace automatically
4. Monitor deployment progress:
   - View real-time logs
   - Track resource creation
   - Check for errors

### 8. Monitor Deployment

1. Deployment redirects to Schematics workspace
2. Monitor the **Activity** tab for progress
3. View detailed logs in the **Jobs** section
4. Wait for status to show **Active**

### 9. Review Outputs

After successful deployment:
1. Go to **Outputs** tab in Schematics workspace
2. Review all output values
3. Copy values for downstream use
4. Document important outputs

## Managing Deployments

### View Existing Deployments

1. Navigate to **Schematics** → **Workspaces**
2. Find workspace created by catalog deployment
3. Workspace name typically includes offering name

### Update Deployment

To update an existing deployment:

1. Go to the Schematics workspace
2. Click **Settings** tab
3. Update variable values as needed
4. Click **Generate plan**
5. Review changes
6. Click **Apply plan**

### Upgrade to New Version

To upgrade to a newer version:

1. Note current configuration and variables
2. Create new deployment with new version
3. Migrate resources if needed
4. Destroy old deployment when ready

### Destroy Deployment

To remove deployed resources:

1. Go to Schematics workspace
2. Click **Actions** → **Destroy resources**
3. Confirm destruction
4. Monitor destruction logs
5. Optionally delete workspace after resources are destroyed

## State Management

- State is automatically managed by Schematics
- State is stored securely in IBM Cloud
- State is accessible to authorized users
- No manual state file management required

## Troubleshooting

### Common Issues

**Deployment Failures**
- Check IAM permissions for target resources
- Verify all required variables are provided
- Review error logs in Schematics workspace
- Ensure resource quotas are not exceeded

**Variable Errors**
- Verify variable types match expected format
- Check for required variables without values
- Validate complex object structures
- Review sensitive variable handling

**Permission Errors**
- Confirm IAM roles for target services
- Check resource group permissions
- Verify API key has required access
- Review service-to-service authorizations

**Version Issues**
- Ensure selected version is published
- Check for deprecated versions
- Review version release notes
- Verify compatibility with dependencies

## Best Practices

### Before Deployment
- Review offering documentation thoroughly
- Understand resource costs and quotas
- Plan resource naming conventions
- Document deployment parameters

### During Deployment
- Use descriptive deployment names
- Tag resources appropriately
- Monitor logs for warnings
- Save output values

### After Deployment
- Document deployed resources
- Set up monitoring and alerts
- Plan for updates and maintenance
- Review security configurations

## Next Steps

- Set up monitoring for deployed resources
- Configure backup and disaster recovery
- Plan for scaling and updates
- Review [Guide: Running Terraform with IBM Cloud Schematics](./running-terraform-with-schematics.md) for workspace management

## Additional Resources

- [IBM Cloud Catalog Documentation](https://cloud.ibm.com/docs/account?topic=account-filter-account)
- [IBM Cloud Schematics Documentation](https://cloud.ibm.com/docs/schematics)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)