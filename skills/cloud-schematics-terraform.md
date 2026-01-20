# Cloud-Based Terraform with IBM Schematics (Scenario 2)

## Skill Overview
This skill covers deploying and managing Terraform using IBM Cloud Schematics for team collaboration and production-grade infrastructure management. In this scenario, a single workspace with a shared state file is used, and multiple team members collectively manage the SAME set of resources.

## When to Use
- Team collaboration on infrastructure
- Long-term resource management
- Production environments
- Reduced state file risk
- **Multiple users managing the SAME resources together**
- Centralized infrastructure operations
- Team members building off each other's efforts

## Key Concepts

### IBM Schematics Workspaces
Running Terraform on the cloud means the state file is stored securely on the cloud. Terraform operations are represented by a **workspace** created by the IBM Schematics cloud service. This workspace becomes the central point for managing your infrastructure.

### State File Storage
Unlike local Terraform, the state file is stored on IBM Cloud, providing:
- **Durability**: Protected against local machine failures
- **Accessibility**: Available to authorized team members
- **Security**: Encrypted and backed up automatically
- **Consistency**: Single source of truth for infrastructure state

### Team Collaboration
Cloud users with appropriate permissions can:
- Execute Terraform through Schematics
- Update a single shared state file
- Build upon each other's work
- Maintain collective infrastructure

## Prerequisites

### 1. Git Repository
Store your Terraform template in a Git repository (GitHub, GitLab, Bitbucket, etc.). When a Schematics workspace is created, it reads from this repository to retrieve the Terraform template.

### 2. IBM Cloud Account
- Active IBM Cloud account
- Appropriate IAM permissions for Schematics
- Access to target resource groups

### 3. Terraform Template
- Valid Terraform configuration files
- Provider configurations
- Variable definitions
- Output definitions

## Implementation Steps

### Step 1: Prepare Git Repository
```bash
# Initialize git repository
git init

# Add terraform files
git add *.tf

# Commit changes
git commit -m "Initial terraform template"

# Push to remote repository
git push origin main
```

### Step 2: Create Schematics Workspace
1. Navigate to IBM Cloud Schematics service
2. Click "Create workspace"
3. Provide workspace details:
   - **Name**: Descriptive workspace name
   - **Resource Group**: Target resource group
   - **Location**: Geographic region for workspace
4. Configure repository settings:
   - **Repository URL**: Git repository URL
   - **Branch**: Branch to use (e.g., main)
   - **Folder**: Path to Terraform files (if not root)
5. Review and create workspace

### Step 3: Configure Variables
Set Terraform variables in the workspace:
- Navigate to workspace settings
- Add variables (terraform.tfvars equivalent)
- Mark sensitive variables as secure
- Save configuration

### Step 4: Generate Plan
```
1. Click "Generate plan" in workspace
2. Review planned changes
3. Verify resources to be created/modified/destroyed
```

### Step 5: Apply Changes
```
1. Click "Apply plan" to execute Terraform
2. Monitor execution logs
3. Verify successful completion
4. Review created resources
```

## Advantages

### Collaboration Benefits
- **Shared State**: Single state file accessible to team
- **Concurrent Access**: Multiple users can work safely
- **Change Tracking**: Audit trail of all operations
- **Role-Based Access**: Control who can view/modify

### Operational Benefits
- **Reliability**: Cloud-backed state file storage
- **Scalability**: Handle large infrastructure deployments
- **Integration**: Works with IBM Cloud services
- **Automation**: API-driven operations possible

### Risk Reduction
- **No Local Dependencies**: Not tied to individual machines
- **Backup & Recovery**: Automatic state file backups
- **Disaster Recovery**: State file survives local failures
- **Version Control**: Template changes tracked in Git

## Best Practices

### 1. Repository Management
- Use meaningful commit messages
- Tag releases for important versions
- Implement branch protection rules
- Review changes before merging

### 2. Workspace Organization
- One workspace per environment (dev, staging, prod)
- Clear naming conventions
- Consistent resource group usage
- Document workspace purpose

### 3. Variable Management
- Use workspace variables for environment-specific values
- Mark sensitive data as secure
- Document required variables
- Validate variable values

### 4. Access Control
- Grant minimum necessary permissions
- Use IAM policies for fine-grained control
- Regular access reviews
- Separate dev and prod permissions

### 5. Change Management
- Always generate plan before applying
- Review plans carefully
- Test in non-production first
- Coordinate with team on changes

## Workspace Operations

### View Workspace State
```
1. Navigate to workspace
2. Click "Resources" tab
3. View managed resources
4. Check resource details
```

### Update Terraform Template
```
1. Update files in Git repository
2. Commit and push changes
3. In workspace, click "Pull latest"
4. Generate new plan
5. Apply changes
```

### Destroy Resources
```
1. Navigate to workspace
2. Click "Actions" > "Destroy resources"
3. Confirm destruction
4. Monitor completion
```

### Delete Workspace
```
1. Destroy all resources first
2. Navigate to workspace settings
3. Click "Delete workspace"
4. Confirm deletion
```

## Migration from Local Terraform

### Option 1: Import Existing State
```bash
# Export local state
terraform state pull > terraform.tfstate

# Import to Schematics workspace via API or CLI
```

### Option 2: Fresh Start
1. Document existing resources
2. Create Schematics workspace
3. Import existing resources using terraform import
4. Verify state matches actual resources

### Option 3: Parallel Management
1. Create new resources in Schematics
2. Gradually migrate workloads
3. Decommission local resources
4. Complete transition

## Troubleshooting

### Common Issues

**Workspace Creation Fails**
- Verify Git repository accessibility
- Check IAM permissions
- Validate repository URL and branch

**Plan Generation Errors**
- Review Terraform syntax
- Check provider configurations
- Verify variable values

**Apply Failures**
- Check resource quotas
- Verify IAM permissions for resources
- Review error logs in workspace

**State Lock Issues**
- Wait for current operation to complete
- Check for stuck operations
- Contact support if lock persists

## Security Considerations

### State File Security
- State files stored encrypted
- Access controlled via IAM
- Audit logs track all access
- Sensitive data marked appropriately

### Credential Management
- Use IBM Cloud API keys
- Rotate credentials regularly
- Store secrets in Secrets Manager
- Never commit credentials to Git

### Network Security
- Use private endpoints where possible
- Implement network policies
- Control outbound access
- Monitor network traffic

## Cost Considerations
- Schematics workspace usage is free
- Pay only for created cloud resources
- Monitor resource costs regularly
- Use cost estimation features

## Integration Opportunities
- **CI/CD Pipelines**: Automate workspace operations
- **Monitoring**: Track infrastructure changes
- **Notifications**: Alert on workspace events
- **APIs**: Programmatic workspace management

## When to Upgrade
Consider moving to product offerings (see `terraform-product-offerings.md`) when:
- Need formal version releases
- Want to distribute to multiple teams
- Require version tracking and rollback
- Creating reusable infrastructure patterns