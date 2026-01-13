# Guide: Running Terraform with IBM Cloud Schematics

## Overview

This guide provides detailed instructions for running Terraform automation using IBM Cloud Schematics, which allows you to execute Terraform in the cloud with shared state management.

## Prerequisites

- IBM Cloud account with appropriate permissions
- Terraform code stored in a Git repository (GitHub, GitLab, Bitbucket, etc.)
- Personal access token for private repositories (if applicable)
- Required IAM permissions for target resources

## When to Use Schematics

- Team collaboration with shared state
- Production deployments
- Centralized state management
- Audit trail and logging requirements
- No local Terraform installation needed

## Steps

### 1. Prepare Your Repository

Ensure your Terraform code is committed and pushed to a Git repository:

```bash
git remote -v  # Verify repository URL
git push       # Ensure latest code is pushed
```

### 2. Access IBM Cloud Schematics

1. Log in to [IBM Cloud Console](https://cloud.ibm.com)
2. Navigate to **Menu** → **Schematics** → **Workspaces**

### 3. Create Schematics Workspace

1. Click **Create workspace**
2. Fill in workspace details:
   - **Repository URL**: Your Git repository URL (e.g., `https://github.com/user/repo.git`)
   - **Personal access token**: Required for private repositories
   - **Terraform version**: Select version matching your `version.tf` file
   - **Workspace name**: Descriptive name for your workspace
   - **Resource group**: Select target resource group
   - **Location**: Select geographic location for workspace
3. Click **Create**

### 4. Configure Variables

1. Go to the **Settings** tab in your workspace
2. Scroll to the **Variables** section
3. Add all required variables:
   - Click **Add variable**
   - Enter variable name and value
   - Mark as **Sensitive** for passwords/API keys
   - Set **Type** (string, number, bool, list, map)
4. Click **Save changes**

### 5. Generate Plan

1. Click **Generate plan** button
2. Monitor the plan generation in the logs
3. Review the plan output:
   - Resources to be created
   - Resources to be modified
   - Resources to be destroyed
4. Verify expected changes

### 6. Apply Configuration

1. Click **Apply plan** button
2. Confirm the action when prompted
3. Monitor the apply logs in real-time
4. Wait for completion (status will show "Active" when done)

### 7. Review Outputs

1. Go to the **Outputs** tab
2. Review all output values from your Terraform configuration
3. Copy values as needed for downstream processes

## State Management

- State is automatically stored in IBM Cloud Schematics service
- State is encrypted at rest
- State is accessible to authorized users in your account
- No local state file management required

## Updating Your Workspace

To apply changes after updating your repository:

1. Ensure changes are pushed to Git
2. In Schematics workspace, click **Pull latest** to sync repository
3. Generate new plan
4. Apply changes

## Cleanup

To destroy resources:

1. Go to **Actions** menu
2. Select **Destroy resources**
3. Confirm the action
4. Monitor destruction logs

To delete the workspace:

1. Go to **Actions** menu
2. Select **Delete workspace**
3. Confirm deletion

## Troubleshooting

### Common Issues

- **Authentication errors**: Verify IBM Cloud API key and permissions
- **Repository access errors**: Check personal access token and repository URL
- **Version mismatch**: Ensure Terraform version matches your code requirements
- **Variable errors**: Verify all required variables are set with correct types

## Best Practices

- Use descriptive workspace names
- Tag workspaces for organization
- Store sensitive values as sensitive variables
- Regularly review and clean up unused workspaces
- Use resource groups to organize deployments

## Next Steps

- Consider onboarding to Private Catalog for versioned offerings
- Review [Guide: Onboarding Terraform to IBM Cloud Private Catalog](./onboarding-terraform-to-private-catalog.md)
- Explore automation with Schematics API