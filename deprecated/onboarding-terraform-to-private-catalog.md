# Guide: Onboarding Terraform to IBM Cloud Private Catalog

## Overview

This guide provides detailed instructions for onboarding your Terraform automation as a versioned offering in IBM Cloud Private Catalog. This enables formal versioning, governance, and sharing across your organization.

## Prerequisites

- Terraform code stored in a Git repository with releases/tags
- IBM Cloud account with Catalog Management permissions
- `ibm_catalog.json` file in repository root (optional but recommended)
- Completed and tested Terraform configuration
- Documentation (README.md) in repository

## When to Use Private Catalog

- Formal versioning and release management
- Sharing across organization or teams
- Governance and compliance requirements
- Standardized deployment patterns
- Catalog-based discovery and deployment

## Steps

### 1. Prepare Your Repository

#### Create Git Releases/Tags

```bash
# Tag your release
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0
```

#### Add ibm_catalog.json (Optional)

Create `ibm_catalog.json` in repository root with metadata:

```json
{
  "products": [
    {
      "name": "your-terraform-offering",
      "label": "Your Terraform Offering",
      "product_kind": "terraform",
      "tags": ["terraform", "infrastructure"],
      "keywords": ["keyword1", "keyword2"],
      "short_description": "Brief description",
      "long_description": "Detailed description",
      "offering_docs_url": "https://github.com/user/repo/blob/main/README.md",
      "offering_icon_url": "https://example.com/icon.svg",
      "provider_name": "Your Organization"
    }
  ]
}
```

### 2. Create Private Catalog

1. Navigate to **Catalog** → **Private catalogs** in IBM Cloud Console
2. Click **Create**
3. Provide:
   - **Catalog name**: Descriptive name for your catalog
   - **Description**: Purpose and contents of catalog
   - **Resource group**: Select appropriate resource group
4. Click **Create**

### 3. Add Terraform Offering

1. In your private catalog, click **Private products** → **Add**
2. Select **Terraform** as the product type
3. Configure offering:
   - **Repository type**: Select Git provider (GitHub, GitLab, etc.)
   - **Repository URL**: Enter your repository URL
   - **Personal access token**: Add token for private repositories
   - **Release/Tag**: Select the version to onboard
   - **Terraform version**: Specify required Terraform version
4. Click **Add**

### 4. Configure Offering Details

1. **Overview tab**:
   - Edit product name and description
   - Add keywords and tags
   - Upload icon/logo
   - Add documentation links

2. **Configure tab**:
   - Review detected variables
   - Set default values
   - Mark sensitive variables
   - Add variable descriptions
   - Configure validation values

3. **Outputs tab**:
   - Review detected outputs
   - Add output descriptions

### 5. Validate Offering

1. Click **Validate** button
2. Select validation target:
   - **Schematics workspace**: Creates temporary workspace
   - **Existing workspace**: Use existing workspace
3. Provide required variable values
4. Click **Validate**
5. Monitor validation logs
6. Review validation results
7. Fix any issues and re-validate

### 6. Publish to Catalog

1. After successful validation, click **Publish**
2. Configure visibility:
   - **Private**: Only your account
   - **IBM Cloud account**: Specific accounts
   - **Public**: All IBM Cloud users (requires approval)
3. Set access controls and permissions
4. Click **Publish**

### 7. Manage Versions

To add new versions:

1. Create new Git tag/release
2. In catalog offering, click **Add version**
3. Select new tag/release
4. Validate new version
5. Publish when ready

## Catalog Metadata Best Practices

### ibm_catalog.json Structure

- Use clear, descriptive names and labels
- Include comprehensive keywords for searchability
- Provide both short and long descriptions
- Add architecture diagrams when available
- Document all configuration parameters
- Include IAM permission requirements

### Version Management

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Document breaking changes in release notes
- Maintain backward compatibility when possible
- Test thoroughly before publishing

## State Management

- Deployments from catalog use Schematics for state management
- State is stored in IBM Cloud Schematics service
- Each deployment creates a separate Schematics workspace

## Troubleshooting

### Common Issues

- **Validation failures**: Check variable values and provider credentials
- **Repository access errors**: Verify personal access token permissions
- **Version conflicts**: Ensure Terraform version compatibility
- **Missing metadata**: Add or update `ibm_catalog.json`

## Next Steps

- Deploy your offering from the catalog
- Review [Guide: Deploying from IBM Cloud Private Catalog](./deploying-from-private-catalog.md)
- Set up automated validation pipelines
- Configure compliance scanning

## Additional Resources

- [IBM Cloud Catalog Management Documentation](https://cloud.ibm.com/docs/account?topic=account-restrict-by-user)
- [Terraform Registry Documentation](https://www.terraform.io/docs/registry/index.html)