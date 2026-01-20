# Terraform Product Offerings in Cloud Catalogs (Scenario 3)

## Skill Overview
This skill covers creating versioned product offerings in cloud catalogs for formal release management and distribution of Terraform templates. This approach is useful whether you work alone or collaborate with others.

## When to Use
- Need formal version releases of Terraform templates
- Want to track versions (development, testing, production)
- Each deployment should create NEW resource instances (not manage same resources)
- Tested and accepted infrastructure patterns
- Version tracking and rollback capabilities
- Development vs. production version separation
- Reusable infrastructure components
- Working alone or with team, but need version control

## Key Concepts

### Product Offerings
As part of the normal lifecycle, templates maintained in Git repositories can be formally released. Product offerings are collections of versioned Terraform templates kept in a cloud catalog, providing:
- **Version Management**: Track releases and development versions
- **Quality Gates**: Designate tested and accepted versions
- **Distribution**: Share with authorized teams
- **Instance Creation**: Each deployment creates new resource instances

### Cloud Catalogs
Catalogs are containers for product offerings that:
- Store multiple versions of templates
- Control access to offerings
- Enable sharing across teams
- Provide centralized template management

### Key Difference from Schematics Workspaces
- **Workspace Approach**: Single workspace manages one set of resources (shared state)
- **Offering Approach**: Each Schematics execution creates a NEW workspace and NEW instances of resources

## Prerequisites

### 1. Git Repository with Releases
- Terraform template in Git repository
- Git tags or releases created
- Semantic versioning (e.g., v1.0.0, v1.1.0)
- Release notes and documentation

### 2. IBM Cloud Catalog Access
- Permissions to create catalogs
- Permissions to create offerings
- Access to target resource groups

### 3. Tested Template
- Template validated and tested
- Acceptance criteria met
- Documentation complete
- Variables clearly defined

## Implementation Steps

### Step 1: Create Git Releases
```bash
# Tag a release in Git
git tag -a v1.0.0 -m "Initial release"
git push origin v1.0.0

# Create release on GitHub/GitLab
# Include release notes and changelog
```

### Step 2: Create or Access Catalog
1. Navigate to IBM Cloud Catalog Management
2. Create new catalog or select existing:
   - **Name**: Descriptive catalog name
   - **Description**: Purpose and contents
   - **Resource Group**: Target resource group
3. Configure catalog settings:
   - **Visibility**: Private or shared
   - **Access Control**: Define who can view/use

### Step 3: Create Product Offering
1. In catalog, click "Create offering"
2. Configure offering details:
   - **Name**: Template name
   - **Category**: Infrastructure, Networking, etc.
   - **Description**: What the template does
   - **Provider**: Your organization
3. Set offering metadata:
   - **Documentation URL**: Link to docs
   - **Support URL**: Support contact
   - **Tags**: Searchable keywords

### Step 4: Import Version from Git
1. Click "Import version" in offering
2. Configure version import:
   - **Repository URL**: Git repository URL
   - **Release/Tag**: Select Git tag (e.g., v1.0.0)
   - **Folder**: Path to Terraform files
   - **Version**: Semantic version number
3. Configure version settings:
   - **Terraform Version**: Required Terraform version
   - **Variables**: Define input variables
   - **Outputs**: Define output values
4. Validate and import version

### Step 5: Configure Version Details
1. Add version documentation
2. Define required variables with:
   - **Name**: Variable name
   - **Type**: string, number, bool, list, map
   - **Description**: What it controls
   - **Default**: Default value (if any)
   - **Required**: Whether mandatory
3. Set version status:
   - **Draft**: Under development
   - **Ready**: Tested and approved
   - **Deprecated**: No longer recommended

### Step 6: Share Catalog
1. Navigate to catalog settings
2. Configure sharing:
   - **Account**: Share within account
   - **Enterprise**: Share across enterprise
   - **Specific Users**: Grant individual access
3. Set permissions:
   - **Viewer**: Can view and deploy
   - **Editor**: Can modify offerings
   - **Administrator**: Full control

## Usage Patterns

### Deploying from Offering
1. User accesses shared catalog
2. Selects product offering
3. Chooses version to deploy
4. Configures variables
5. Schematics creates NEW workspace
6. Resources are provisioned
7. User manages their own instance

### Version Lifecycle
```
Development → Testing → Ready → Production → Deprecated
     ↓           ↓         ↓          ↓           ↓
   Draft      Draft     Ready      Ready     Deprecated
```

### Multiple Instances
Each deployment creates:
- New Schematics workspace
- New state file
- New set of resources
- Independent lifecycle

## Advantages

### Version Control Benefits
- **Release Tracking**: Clear version history
- **Rollback Capability**: Deploy previous versions
- **Change Documentation**: Release notes per version
- **Quality Assurance**: Formal testing before release

### Distribution Benefits
- **Centralized Management**: Single source for templates
- **Controlled Access**: Manage who can use templates
- **Consistent Deployment**: Same template for all users
- **Reduced Duplication**: Reuse instead of recreate

### Operational Benefits
- **Instance Isolation**: Each deployment independent
- **Parallel Environments**: Multiple instances simultaneously
- **Team Autonomy**: Teams manage their own instances
- **Resource Separation**: Clear ownership boundaries

## Best Practices

### 1. Version Management
- Use semantic versioning (MAJOR.MINOR.PATCH)
- Create releases for tested versions only
- Maintain changelog for each version
- Document breaking changes clearly

### 2. Offering Organization
- One offering per logical infrastructure component
- Clear naming conventions
- Comprehensive descriptions
- Appropriate categorization

### 3. Variable Design
- Provide sensible defaults where possible
- Validate variable inputs
- Document variable purposes
- Group related variables

### 4. Documentation
- Include README in repository
- Provide usage examples
- Document prerequisites
- Explain outputs and their uses

### 5. Testing Strategy
- Test in draft status first
- Validate in non-production
- Get user feedback
- Mark as ready only after approval

### 6. Catalog Management
- Regular catalog reviews
- Deprecate old versions
- Archive unused offerings
- Monitor usage patterns

## Version Import Process

### Automatic Import
When Git releases are created, import them to offerings:
```
Git Tag → Import to Offering → Validate → Set Status → Share
```

### Manual Import
For development versions or branches:
1. Specify branch instead of tag
2. Import for testing purposes
3. Keep in draft status
4. Promote to release when ready

## Comparison: Workspace vs. Offering

### Single Workspace (Scenario 2)
- One workspace = One set of resources
- Team collaborates on same infrastructure
- Shared state file
- Collective management
- Updates affect all users

### Product Offering (Scenario 3)
- Each deployment = New workspace + New resources
- Each team has own infrastructure instance
- Separate state files
- Independent management
- Updates don't affect other instances

## Migration Path

### From Schematics Workspace
When you need to:
- Distribute template to multiple teams
- Create multiple independent instances
- Implement formal version control
- Enable self-service deployment

**Action**: Convert workspace template to product offering

### From Local Terraform
1. Move to Git repository
2. Create releases
3. Import to catalog offering
4. Share with teams

## Troubleshooting

### Import Failures
- **Repository Access**: Verify Git URL and credentials
- **Path Issues**: Check folder path to Terraform files
- **Validation Errors**: Review Terraform syntax
- **Version Conflicts**: Ensure unique version numbers

### Deployment Issues
- **Variable Errors**: Verify all required variables provided
- **Permission Errors**: Check IAM permissions for resources
- **Quota Errors**: Verify resource quotas available
- **Network Errors**: Check connectivity and endpoints

### Version Management
- **Cannot Update**: Versions are immutable; create new version
- **Wrong Version**: Deploy correct version from catalog
- **Deprecated Version**: Update to newer version

## Advanced Features

### Version Dependencies
- Specify required provider versions
- Define Terraform version constraints
- Document external dependencies

### Custom Validation
- Add validation rules for variables
- Implement pre-deployment checks
- Validate resource configurations

### Integration
- **CI/CD**: Automate version imports
- **Monitoring**: Track deployment success
- **Notifications**: Alert on new versions
- **APIs**: Programmatic catalog management

## Security Considerations

### Access Control
- Restrict catalog access appropriately
- Use IAM policies for fine-grained control
- Audit catalog access regularly
- Separate dev and prod catalogs

### Version Security
- Scan templates for security issues
- Review code before marking ready
- Document security requirements
- Update for security patches

### Credential Management
- Never include credentials in templates
- Use variable injection for secrets
- Integrate with Secrets Manager
- Rotate credentials regularly

## Cost Considerations
- Catalog management is free
- Each deployment creates billable resources
- Monitor resource costs per instance
- Implement cost controls and budgets

## When to Upgrade
Consider global sharing (see `global-terraform-sharing.md`) when:
- Template is general-purpose
- Useful across entire organization
- Ready for company-wide adoption
- Mature and well-documented