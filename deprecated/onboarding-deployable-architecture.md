# Guide: Onboarding Deployable Architecture to IBM Cloud Catalog

## Overview

This guide provides detailed instructions for onboarding a Deployable Architecture (DA) to IBM Cloud Private Catalog. Deployable Architectures are advanced Terraform-based solutions with enhanced IBM Cloud features, compliance profiles, and enterprise-grade capabilities.

## Prerequisites

- Terraform code with `ibm_catalog.json` containing `"product_kind": "solution"`
- Git repository with releases/tags
- IBM Cloud account with Catalog Management permissions
- Completed and tested DA configuration
- Architecture diagrams and documentation
- Compliance profiles configured (if applicable)

## When to Use Deployable Architecture

- Enterprise-grade deployments
- Complex multi-service architectures
- Compliance and governance requirements
- Advanced IBM Cloud features (Projects, compliance scanning)
- Standardized reference architectures
- Multi-environment deployments

## Deployable Architecture vs Standard Terraform

**Deployable Architecture includes:**
- Integration with IBM Cloud Projects service
- Compliance profile support
- Enhanced validation and testing
- Architecture diagrams and documentation
- Multi-stack deployments
- Dependency management between stacks

## Steps

### 1. Prepare DA Repository

#### Verify ibm_catalog.json

Ensure `ibm_catalog.json` exists with DA-specific metadata:

```json
{
  "products": [
    {
      "name": "deploy-arch-your-solution",
      "label": "Your Deployable Architecture",
      "product_kind": "solution",
      "tags": ["ibm_created", "target_terraform", "terraform", "solution"],
      "keywords": ["keyword1", "keyword2"],
      "short_description": "Brief description",
      "long_description": "Detailed description of the architecture",
      "offering_docs_url": "https://github.com/user/repo/blob/main/README.md",
      "offering_icon_url": "https://example.com/icon.svg",
      "provider_name": "IBM",
      "features": [
        {
          "title": "Feature 1",
          "description": "Description of feature 1"
        }
      ],
      "flavors": [
        {
          "label": "Standard",
          "name": "standard",
          "install_type": "fullstack",
          "working_directory": "solutions/standard",
          "compliance": {
            "authority": "scc-v3",
            "profiles": [
              {
                "profile_name": "IBM Cloud Framework for Financial Services",
                "profile_version": "1.5.0"
              }
            ]
          },
          "iam_permissions": [
            {
              "service_name": "service-name",
              "role_crns": ["crn:v1:bluemix:public:iam::::role:Administrator"]
            }
          ],
          "architecture": {
            "descriptions": "Architecture description",
            "features": [],
            "diagrams": [
              {
                "diagram": {
                  "caption": "Architecture Diagram",
                  "url": "https://example.com/diagram.svg",
                  "type": "image/svg+xml"
                }
              }
            ]
          }
        }
      ]
    }
  ]
}
```

#### Create Architecture Diagram

- Create SVG diagram showing architecture components
- Include all services and connections
- Store in repository (e.g., `reference-architecture/diagram.svg`)
- Reference in `ibm_catalog.json`

#### Document IAM Permissions

List all required IAM permissions in `ibm_catalog.json`:
- Service names
- Required roles (platform and service)
- Notes explaining why permissions are needed

### 2. Create Private Catalog

1. Navigate to **Catalog** → **Private catalogs**
2. Click **Create**
3. Provide catalog details:
   - **Name**: Descriptive catalog name
   - **Description**: Purpose and scope
   - **Resource group**: Target resource group
4. Click **Create**

### 3. Add Deployable Architecture

1. In your private catalog, click **Private products** → **Add**
2. Select **Deployable architecture** as product type
3. Configure DA:
   - **Repository type**: Select Git provider
   - **Repository URL**: Enter repository URL
   - **Personal access token**: Add for private repos
   - **Release/Tag**: Select version to onboard
   - **Terraform version**: Specify required version
4. Click **Add**

### 4. Configure DA Metadata

#### Overview Tab
- Edit product name and label
- Add comprehensive description
- Upload icon/logo (SVG recommended)
- Add keywords and tags
- Link to documentation

#### Architecture Tab
- Upload or link architecture diagram
- Add architecture description
- Document features and capabilities
- Describe deployment patterns

#### Configure Tab
- Review detected variables from Terraform
- Set default values
- Mark sensitive variables
- Add variable descriptions and constraints
- Configure validation values
- Group related variables

#### Compliance Tab (if applicable)
- Select compliance profiles
- Configure Security and Compliance Center integration
- Set up automated compliance scanning
- Document compliance requirements

#### IAM Permissions Tab
- Review required permissions
- Add service-specific roles
- Document permission requirements
- Include notes for users

### 5. Configure Flavors

If your DA has multiple flavors (deployment variations):

1. Each flavor represents a different configuration
2. Configure working directory for each flavor
3. Set flavor-specific variables
4. Add flavor descriptions
5. Configure compliance per flavor

### 6. Validate Deployable Architecture

1. Click **Validate** button
2. Select validation method:
   - **New project**: Creates temporary project
   - **Existing project**: Use existing project
3. Provide required inputs:
   - All required variables
   - API keys and credentials
   - Target resource group and region
4. Click **Validate**
5. Monitor validation process:
   - Terraform plan generation
   - Resource provisioning
   - Compliance scanning (if configured)
   - Automated tests
6. Review validation results:
   - Deployment success/failure
   - Compliance scan results
   - Resource inventory
   - Output values
7. Fix any issues and re-validate

### 7. Configure Compliance Scanning (Optional)

For compliance-enabled DAs:

1. Select compliance profiles (e.g., IBM Cloud Framework for Financial Services)
2. Configure Security and Compliance Center integration
3. Set up automated scanning
4. Define compliance thresholds
5. Configure remediation workflows

### 8. Publish Deployable Architecture

1. After successful validation, click **Publish**
2. Configure visibility:
   - **Account**: Private to your account
   - **Enterprise**: Share across enterprise
   - **Public**: Submit for IBM Cloud catalog (requires approval)
3. Set access controls
4. Add release notes
5. Click **Publish**

### 9. Manage Versions

To add new versions:

1. Create new Git tag/release
2. In catalog offering, click **Add version**
3. Select new tag/release
4. Validate new version
5. Add version-specific release notes
6. Publish when ready

## State Management

- Deployments use IBM Cloud Projects service
- State stored in Projects service (not Schematics)
- Enhanced state management with project lifecycle
- Support for multi-stack deployments

## Best Practices

### Repository Structure
```
/
├── ibm_catalog.json          # DA metadata
├── README.md                 # Documentation
├── main.tf                   # Root module (optional)
├── variables.tf
├── outputs.tf
├── version.tf
├── reference-architecture/
│   └── diagram.svg          # Architecture diagram
├── solutions/
│   ├── standard/            # Standard flavor
│   │   ├── main.tf
│   │   ├── variables.tf
│   │   └── outputs.tf
│   └── advanced/            # Advanced flavor
└── modules/                 # Reusable modules
```

### Metadata Guidelines
- Use clear, descriptive names
- Include comprehensive documentation
- Add detailed architecture diagrams
- Document all IAM permissions
- Provide example values
- Include troubleshooting guides

### Compliance Configuration
- Select appropriate compliance profiles
- Document compliance requirements
- Test compliance scanning
- Provide remediation guidance
- Keep profiles up to date

### Version Management
- Use semantic versioning
- Document breaking changes
- Maintain backward compatibility
- Test upgrades thoroughly
- Provide migration guides

## Troubleshooting

### Common Issues

**Validation Failures**
- Check all required variables
- Verify IAM permissions
- Review compliance scan results
- Check resource quotas
- Validate architecture diagram URLs

**Compliance Scan Failures**
- Review failed controls
- Check resource configurations
- Verify security settings
- Update compliance profiles
- Document exceptions

**Metadata Errors**
- Validate `ibm_catalog.json` syntax
- Check required fields
- Verify URL accessibility
- Validate flavor configurations
- Review IAM permission format

## Next Steps

- Deploy your DA via Projects service
- Review [Guide: Deploying Deployable Architecture via IBM Cloud Projects](./deploying-deployable-architecture-via-projects.md)
- Set up CI/CD pipelines
- Configure automated testing
- Monitor compliance posture

## Additional Resources

- [IBM Cloud Deployable Architectures Documentation](https://cloud.ibm.com/docs/secure-enterprise?topic=secure-enterprise-understand-module-da)
- [IBM Cloud Projects Documentation](https://cloud.ibm.com/docs/secure-enterprise?topic=secure-enterprise-understanding-projects)
- [Security and Compliance Center](https://cloud.ibm.com/docs/security-compliance)