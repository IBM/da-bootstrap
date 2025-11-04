# Steps to Create a Deployable Architecture for IBM Cloud

## Overview
This guide outlines the steps needed to create a Deployable Architecture (DA) suitable for onboarding to the IBM Cloud Catalog.

## 1. Project Structure Setup
- Create a GitHub repository for your DA
- Set up directory structure:
  - `/` or `/terraform/` - Terraform configuration files
  - `/diagrams/` - Architecture diagrams (SVG recommended)
  - Documentation files (README.md, etc.)

## 2. Terraform Configuration
Create the following Terraform files:

### Required Files:
- **main.tf** - Core infrastructure resources and module calls
- **variables.tf** - Input variables with descriptions and validation
- **outputs.tf** - Output values to expose after deployment
- **version.tf** - Provider version constraints and required Terraform version
- **terraform.tfvars.template** - Example variable values for users

### Best Practices:
- Use meaningful variable names
- Add detailed descriptions to all variables
- Include validation rules where appropriate
- Define sensible default values
- Document all outputs

## 3. Architecture Diagram
- Create an SVG diagram showing your architecture components
- Include all IBM Cloud services and their relationships
- Generate SHA-256 hash: `shasum -a 256 diagrams/architecture.svg`
- Place diagram in `/diagrams/` directory
- Keep diagram updated with infrastructure changes

## 4. Create ibm_catalog.json

The `ibm_catalog.json` file is the key configuration file for IBM Cloud Catalog onboarding. It defines how your DA appears and behaves in the IBM Cloud Catalog. It is sometimes referred to as the `catalog manifest` or just `manifest`.

**📖 For detailed step-by-step instructions on creating this file, see:**
[Creating an ibm_catalog.json File from Scratch](https://github.com/IBM/da-bootstrap/blob/main/topics/Creating_ibm_catalog_json.md)

### Key Components:
- Product metadata (name, description, tags, keywords)
- Flavors configuration (deployment variations)
- IAM permissions required
- Architecture diagram references
- Terraform variable mappings to UI inputs
- Custom UI widgets for enhanced user experience

## 5. Documentation

### README.md
- Project overview and purpose
- Prerequisites and requirements
- Quick start guide
- Usage examples
- Architecture overview
- Contributing guidelines

### DEPLOYMENT_GUIDE.md
- Detailed step-by-step deployment instructions
- Configuration options
- Post-deployment steps
- Troubleshooting guide
- FAQ section

### CONTRIBUTING.md (Optional)
- How to contribute
- Code standards
- Pull request process
- Testing requirements

## 6. Icon/Branding
- Create or obtain an SVG icon (recommended size: 32x32 or 64x64)
- Convert to base64: `base64 -i icon.svg`
- Format: `data:image/svg+xml;base64,<base64-string>`
- Alternatively, host publicly and provide URL
- Add to ibm_catalog.json `offering_icon_url` field

## 7. Testing

### Local Testing:
```bash
# Initialize Terraform
terraform init

# Validate configuration
terraform validate

# Plan deployment
terraform plan

# Apply (in test environment)
terraform apply
```

### Validation Checklist:
- ✅ JSON syntax is valid
- ✅ All required fields are present
- ✅ CRNs and service names are correct
- ✅ SHA hashes match diagram files
- ✅ Parameter keys match Terraform variable names
- ✅ Terraform code runs successfully
- ✅ Documentation is complete and accurate

## 8. Onboarding to IBM Cloud

### Steps:
1. **Create Private Catalog**
   - Log into IBM Cloud Console
   - Navigate to Manage > Catalogs
   - Create a new private catalog

2. **Import from GitHub**
   - Select "Import offering"
   - Provide GitHub repository URL
   - Select branch (usually `main`)
   - Specify path to ibm_catalog.json

3. **Validate Offering**
   - Review imported metadata
   - Verify UI rendering
   - Check parameter mappings
   - Validate IAM permissions

4. **Test Deployment**
   - Deploy through catalog UI
   - Test with various parameter combinations
   - Verify all resources are created correctly
   - Check outputs are displayed properly

5. **Publish (Optional)**
   - Request approval for public catalog
   - Complete IBM Cloud onboarding process
   - Publish to public catalog

## Key Files Checklist

- ✅ **ibm_catalog.json** - Catalog metadata and configuration
- ✅ **main.tf** - Terraform infrastructure code
- ✅ **variables.tf** - Input variable definitions
- ✅ **outputs.tf** - Output value definitions
- ✅ **version.tf** - Provider version constraints
- ✅ **terraform.tfvars.template** - Example variable values
- ✅ **diagrams/architecture.svg** - Architecture diagram
- ✅ **README.md** - Project documentation
- ✅ **DEPLOYMENT_GUIDE.md** - Deployment instructions
- ✅ **icon.svg** - Product icon
- ✅ **.gitignore** - Git ignore rules

## Additional Resources

- [Creating ibm_catalog.json - Step-by-Step Guide](https://github.com/IBM/da-bootstrap/blob/main/topics/Creating_ibm_catalog_json.md)
- [IBM Cloud Catalog Management API](https://cloud.ibm.com/apidocs/resource-catalog/private-catalog)
- [Deployable Architecture Documentation](https://cloud.ibm.com/docs/secure-enterprise)
- [Terraform IBM Cloud Provider](https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs)
- [IBM DA Bootstrap Repository](https://github.com/IBM/da-bootstrap)

## Next Steps

After creating these files:
1. Commit all files to your GitHub repository
2. Test locally with Terraform
3. Create a private catalog in IBM Cloud
4. Import and validate your offering
5. Test deployment through the catalog
6. Iterate based on feedback
7. Consider publishing to public catalog

---

**Note**: Always test thoroughly in a private catalog before publishing publicly. Ensure all documentation is complete and accurate.