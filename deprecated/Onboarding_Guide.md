# Onboarding a Deployable Architecture

## Overview
This guide provides step-by-step instructions for onboarding/creating a tile in a private catalog on the IBM Cloud.  It assumes you have already created your automation following the recommended practices and
that you have already created your catalog manifest file using the steps [found in this guide](https://github.com/IBM/da-bootstrap/blob/main/guides/How_to_create_a_DA.md).  Tiles in private catalogs 
maybe shared to additional IBM Cloud accounts and published to the IBM Cloud Catalog.

## Prerequisites

Before onboarding, ensure your DA github repository contains all required files:

### ✅ Required Files Checklist
- **ibm_catalog.json** - Catalog manifest defining your DA
- **Terraform Configuration Files** - This is your DA's automation.
   Your DA requires at least one Terraform file (`.tf` extension). The specific files and their organization can vary based on your implementation needs. 
- **Architecture Diagram** - An SVG file exists in the repository and is referenced by the `ibm_catalog.json` file
- **Documentation**:
  - `README.md` - Project overview and usage
- **Icon** - An icon file exists in the repository and is referenced by the `ibm_catalog.json` file
- **IBM Cloud Account** - With appropriate permissions to create a catalog if just starting or with edit permission to use an existing private catalog.

### 📖 Reference Guides
If you haven't created these files yet, refer to:
- [Creating ibm_catalog.json](https://github.com/IBM/da-bootstrap/blob/main/guides/How_to_create_a_DA.md) - Detailed catalog manifest guide

## Pre-Onboarding Validation

Before importing to IBM Cloud, optionally validate your DA locally:

- verify that all pending file changes have been committed to the git repository.

### 1. Optionally Validate Terraform Configuration
```bash
# Navigate to your Terraform directory
cd terraform/  # or wherever your .tf files are located

# Initialize Terraform
terraform init

# Validate syntax and configuration
terraform validate

# Review planned changes
terraform plan
```

### 2. Optionally Validate ibm_catalog.json if it exists
```bash
# Check JSON syntax
cat ibm_catalog.json | jq .

# Verify required fields are present
# - products[].name
# - products[].label
# - products[].product_kind (should be "solution")
# - products[].flavors[]
# - products[].flavors[].configuration[]
```

## Onboarding Steps

### Step 1: Create a Private Catalog if you do not already have one

Start with a private offering catalog for testing before publishing publicly.  Use either the IBM Console UI 
or the IBM Cloud CLI.

Use the IBM Console UI to create a catalog
1. Log into [IBM Cloud Console](https://cloud.ibm.com)
2. Navigate to **Manage > Catalogs**
3. Click **Create catalog**
4. Provide:
   - **Catalog type**: Select **Product** for the type of private catalog
   - **Name**: Descriptive name for your catalog
   - **Description**: Purpose of this catalog
   - **Resource group**: Select the name of an existing resource group
   - **Select template**: Choose between an empty catalog or a non-empty catalog 
5. Click **Create**

Use the IBM Cloud CLI to create a catalog
1. Log into the IBM Cloud using the ibmcloud cli
2. Set a target resource group:
```ibmcloud target -g <RESOURCE_GROUP>``` where RESOURCE_GROUP is an existing resource group name.
3. Create the catalog using the following command:
```bash
ibmcloud catalog create --name "My-DA-Catalog" --description "Private catalog for automation, solutions, and Deployable Architectures"
```
This command creates a new private catalog named "My-DA-Catalog" in the resource group you targeted in step 2. You can customize the catalog name and description as needed.

### Step 2: Push any updated files to Github

If any of the files have changed, they should be pushed to the Github repository.  This would include the manifest file, icons, diagrams and any terraform files that have changed.

### Step 3: Import Your DA from GitHub

Your DA may be imported into a private offering catalog with one of two methods.  Use either the IBM Console UI 
or the IBM Cloud CLI.  Before you begin, make sure that you update your github repository with any DA files that have changed.  Be sure that the catalog manifest, ibm_catalog.json, has been added to the repository and its up to date.  This assumes you are planning to import the DA from a git repository branch, typicaly `main`.

The Github url may either be a url to a github branch or it may be the url to a github release of the repository.  Onboarding local files is not supported.

Use the IBM Console UI to import your DA

1. Login to the IBM Cloud console and navigate to your private catalog.
2. In your catalog, click **Add product** if this is a new offering.
   - Select **Deployable architecture** as the Product type
   - Select **Terraform** as the Delivery method
   - Choose repository type:
      - **Public repository** - For public GitHub repos
      - **Private repository** - Requires GitHub personal access token
   - Enter your **GitHub web url** which should also include the current branch.  If current directory represents a github repository, determine the url from the github config.
      - Example: `https://github.com/your-org/your-da-repo/tree/your-branch-name` (typically `main`)
   - Select the name of your variation (flavor)
   - Select a semantic version string, for example `0.0.1` for the Software version
   - Select **Add product**
3. If it is an already existing offering, click the existing offering listed in the catalog.
   - Click **Versions**
   - Click **Add version**
   - Select **Terraform** as the Delivery method
   - Choose repository type:
      - **Public repository** - For public GitHub repos
      - **Private repository** - Requires GitHub personal access token
   - Enter your **GitHub web url** which should also include the current branch.  If current directory represents a github repository, determine the url from the github config.
      - Example: `https://github.com/your-org/your-da-repo/tree/your-branch-name` (typically `main`)
   - Select the name of your variation (flavor)
   - Select a semantic version string, for example `0.0.1` for the Software version
   - Select **Add version**

Use the IBM Cloud CLI to import your DA

1. Log into the IBM Cloud using the ibmcloud cli
2. If this is a new offering
   - create the offering and initial version by using the ibmcloud cli using the `catalog offering create` command and specifying
      - catalog id or catalog name of the private catalog
      - the **GitHub web url** which should also include the current branch
         - Example: `https://github.com/your-org/your-da-repo/tree/your-branch-name` (typically `main`)
      - the variation display name as the variation-label
      - the offering name as the `name`
      - the product-kind is `solution` for a DA
      - the semantic version string for example `0.0.1` for the initial version
      - `terraform` for the format-kind 
      - `fullstack` for the install-type
   Example: 
```
   ibmcloud catalog offering create --catalog "CATALOG_NAME" --zipurl GITHUB_REPO_URL --variation-label "VARIATION_NAME" --name "OFFERING_NAME" --product-kind solution --target-version SEMANTIC_VERSION --format-kind terraform --install-type fullstack
```

3. If this is an existing offering
   - import a version of the offering by using the ibmcloud cli using the `catalog offering import-version` command and specifying 
      - the **GitHub web url** which should also include the current branch
         - Example: `https://github.com/your-org/your-da-repo/tree/your-branch-name` (typically `main`)
      - the semantic version string for example `0.0.1` for the initial version
      - catalog id or catalog name of the private catalog
      - the offering id of the existing offering.  The offering id of the existing offering may be found using the ibmcloud cli command `catalog offering list` and finding the offering in the list and retrieving its ID value.
      - include defined configuation by specifying include-config
      - the variation display name as the variation-label
      - `terraform` for the format-kind 
      - `fullstack` for the install-type
   Example:
```
   ibmcloud catalog offering import-version --zipurl GITHUB_REPO_URL --target-version SEMANTIC_VERSION --catalog "CATALOG_NAME --offering CATALOG_OFFERING_ID --include-config --variation-label "VARIATION_NAME" --format-kind terraform --install-type fullstack
```         

### Step 4: Review and Validate the Imported Offering

After import, IBM Cloud displays your DA configuration:

#### Review Product Metadata
- ✅ Product name and label display correctly
- ✅ Description is clear and accurate
- ✅ Tags and keywords are appropriate
- ✅ Icon displays properly

#### Review Flavors
- ✅ All flavors are listed (e.g., "standard", "quickstart")
- ✅ Flavor descriptions are clear
- ✅ Working directory path is correct

#### Review Configuration Parameters
- ✅ All Terraform variables are mapped
- ✅ Parameter types are correct (string, password, number, boolean)
- ✅ Default values are appropriate
- ✅ Required parameters are marked correctly
- ✅ Custom UI widgets render properly (vpc_region, resource_group, etc.)

#### Review IAM Permissions
- ✅ All required IBM Cloud services are listed
- ✅ Role CRNs are correct
- ✅ Permissions match what your Terraform code requires

#### Review Architecture Diagrams
- ✅ Diagrams display correctly
- ✅ Captions and descriptions are accurate
- ✅ SHA-256 hashes are valid

**If validation errors occur:**
1. Fix issues in your GitHub repository
2. Commit and push changes
3. Return to IBM Cloud Catalog
4. Click **Update from repository** to re-import

### Step 5: Configure Version Details

1. Click on your imported offering
2. Navigate to **Version** tab
3. Add or update:
   - **Version number** (use semantic versioning: 1.0.0)
   - **Release notes** (changelog for this version)
   - **Terraform version** (minimum required version)
   - **Compliance** information (if applicable)
4. Save changes

### Step 6: Validate Deployment

Test your DA thoroughly before sharing or publishing:

#### Run Validation
1. Click **Validate** button in the catalog
2. Select a **flavor** to test
3. Choose a **target region**
4. Fill in **required parameters**:
   - Use test values
   - Ensure you have necessary IBM Cloud resources (VPC, resource group, etc.)
5. Click **Validate**

IBM Cloud will:
- Run `terraform init`
- Run `terraform plan`
- Display planned changes
- Show any errors or warnings

#### Deploy to Test Environment
1. After successful validation, click **Deploy**
2. Provide:
   - **Workspace name** (for tracking)
   - **Resource group** (where to deploy)
   - **Region** (deployment location)
3. Fill in all **required parameters**
4. Review the deployment plan
5. Click **Deploy**

#### Verify Deployment
- ✅ All resources created successfully
- ✅ No errors in deployment logs
- ✅ Outputs display correctly
- ✅ Resources function as expected
- ✅ Resources can be destroyed cleanly

### Step 7: Share with Team (Optional)

Before publishing publicly, share with your team for testing:

1. Using the ibmcloud cli, mark the version of the offering as `pre-release`:
```
ibmcloud catalog offering version pre-release --version-locator LOCATOR
```
Use the cli command
```
ibmcloud catalog offering list --catalog <NAME or ID>
``` 
to obtain the version locator.

2. Publish the offering to the account:
```
ibmcloud catalog offering publish account --catalog CATALOG --offering OFFERING
```

### Step 8: Publish to Public Catalog (Optional)

Once thoroughly tested, you can publish to the public IBM Cloud Catalog:

#### Prerequisites for Public Publishing
- ✅ Extensive testing in private catalog
- ✅ Complete and accurate documentation
- ✅ Clear support and maintenance plan
- ✅ Compliance with IBM Cloud policies
- ✅ IBM Cloud Partner agreement (if applicable)

#### Publishing Process
1. **Request Approval**
   - Contact IBM Cloud Catalog team
   - Provide DA details and use case
   - Submit for review

2. **Complete Onboarding**
   - Fill out IBM Cloud Partner forms
   - Provide support contact information
   - Define pricing (if applicable)
   - Agree to terms and conditions

3. **Submit for Review**
   - IBM team reviews your DA
   - Checks for quality, security, compliance
   - May request changes or improvements

4. **Address Feedback**
   - Make requested changes
   - Update documentation
   - Re-submit for review

5. **Publish**
   - Once approved, DA is published
   - Available in public IBM Cloud Catalog
   - Monitor for user feedback and issues

## Quick Command Reference

```bash
# Validate JSON syntax
cat ibm_catalog.json | jq .

# Generate diagram SHA-256 hash
shasum -a 256 diagrams/architecture.svg

# List available catalog categories
ibmcloud catalog offering category-options

# Terraform validation
terraform init
terraform validate
terraform plan

# Test Terraform locally
terraform apply -auto-approve
terraform destroy -auto-approve

# Check Terraform version
terraform version

# Format Terraform code
terraform fmt -recursive
```

## Additional Resources

### IBM DA Bootstrap Resources
- **[Creating ibm_catalog.json](https://github.com/IBM/da-bootstrap/blob/main/guides/Creating_ibm_catalog_json.md)** - Detailed catalog manifest guide
- **[IBM DA Bootstrap Repository](https://github.com/IBM/da-bootstrap)** - Templates and examples

### IBM Cloud Documentation
- [IBM Cloud Catalog Management](https://cloud.ibm.com/docs/account?topic=account-restrict-by-user)
- [Private Catalog Documentation](https://cloud.ibm.com/docs/account?topic=account-catalog-enterprise-filters)
- [Deployable Architecture Guide](https://cloud.ibm.com/docs/secure-enterprise)
- [IBM Cloud Catalog Management API](https://cloud.ibm.com/apidocs/resource-catalog/private-catalog)
- [Catalog manifest](https://github.com/ibm-cloud-docs/secure-enterprise/blob/master/catalog-manifest.md)

### Terraform Resources
- [Terraform IBM Cloud Provider](https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs)
- [Terraform Best Practices](https://www.terraform.io/docs/cloud/guides/recommended-practices/index.html)

---

## Summary

Onboarding a Deployable Architecture to IBM Cloud Catalog involves:

1. **Preparation** - Ensure all required files are in your repository
2. **Validation** - Test locally before importing
3. **Import** - Create private catalog and import from GitHub
4. **Review** - Validate all metadata, parameters, and configurations
5. **Test** - Deploy and verify in test environment
6. **Share** - Test with team members (optional)
7. **Publish** - Submit for review and publish to public catalog (optional)

**Remember**: The onboarding process is iterative. Be prepared to update your repository and re-import as you refine your offering based on testing and feedback. Always prioritize thorough testing in a private catalog before publishing publicly.