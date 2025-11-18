# IBM Catalog Manifest Validation Checklist

This checklist represents the validation steps performed by the `validate_catalog_manifest.py` script for validating `ibm_catalog.json` files.

## Prerequisites

- [ ] Locate the `ibm_catalog.json` file to validate

## JSON File Validation

- [ ] Load and parse the JSON file
- [ ] Verify JSON syntax is valid
- [ ] Confirm file exists and is readable

## Top-Level Structure Validation

- [ ] Verify `products` field exists
- [ ] Confirm `products` is an array
- [ ] Ensure `products` array is not empty
- [ ] Count and report number of products found

## Product-Level Validation

For each product in the products array:

### Required Fields
- [ ] Verify `name` field exists and is not empty
- [ ] Verify `label` field exists and is not empty
- [ ] Verify `product_kind` field exists and is not empty
- [ ] Verify `short_description` field exists and is not empty
- [ ] Verify `long_description` field exists and is not empty
- [ ] Verify `offering_docs_url` field exists and is not empty
- [ ] Verify `provider_name` field exists and is not empty

### Product Kind Validation
- [ ] Confirm `product_kind` is either 'solution' or 'module'

### Tags Validation
- [ ] Check if `tags` array exists
- [ ] Count number of tags
- [ ] Validate tags against valid tags list.  The valid tags list is :
      ['app_dev', 'business_analytics', 'solution_docs', 'solution', 'target_terraform', 'terraform', 'reference_architecture', 'storage_classic', 'database', 'logging_monitoring', 'dev_ops', 'asset_management', 'network', 'content', 'migration_tools', 'mobile', 'storage_datamovement', 'clusters', 'ibm_created', 'blockchain', 'storage', 'analytics', 'ai', 'network_vpc', 'network_classic', 'converged_infra', 'storage_backup', 'network_edge', 'storage_object', 'business_automation', 'storage_file', 'data_analytics', 'enterprise_app', 'compute_baremetal', 'platform_engineering', 'integration', 'watson', 'Manufacturing', 'data_management', 'storage_vpc', 'network_interconnectivity', 'internet_of_things', 'registry', 'compute_classic', 'virtualservers', 'security', 'containers', 'storage_block', 'openwhisk', 'compute', 'platform_service', 'FinancialSector']
- [ ] Report any invalid tags found

### Keywords Validation
- [ ] Check if `keywords` array exists
- [ ] Count number of keywords

### Icon Validation
- [ ] Check if `offering_icon_url` is defined

## Flavor Validation

For each product:

### Flavor Structure
- [ ] Verify `flavors` array exists
- [ ] Confirm `flavors` is a non-empty array
- [ ] Count number of flavors

For each flavor:

### Required Flavor Fields
- [ ] Verify `label` field exists
- [ ] Verify `name` field exists
- [ ] Verify `install_type` field exists
- [ ] Verify `working_directory` field exists

### Install Type Validation
- [ ] Confirm `install_type` is either 'fullstack' or 'extension'
- [ ] Verify `install_type` appears only once within the flavor (singleton rule)

## IAM Permissions Validation

For each flavor:

### IAM Structure
- [ ] Check if `iam_permissions` array exists

For each IAM permission:
- [ ] Verify `service_name` field exists
- [ ] Verify `role_crns` array exists
- [ ] Validate each CRN matches pattern: `crn:v1:bluemix:public:iam::::(?:role|serviceRole):\w+`
- [ ] Report any invalid CRN formats

## Configuration Parameters Validation

For each flavor:

### Configuration Structure
- [ ] Check if `configuration` array exists
- [ ] Count total number of parameters
- [ ] Count number of required parameters

For each configuration parameter:
- [ ] Verify `key` field exists
- [ ] Verify `type` field exists
- [ ] Confirm `type` is one of `boolean`, `float`, `int`, `number`, `password`, `string`, `object` or it must be one of the following `Custom types` 
      array, textarea, vpc, vpc_region, power_iaas, power_iaas_zone, resource_group, schematics_workspace, code_editor, platform_resource, worker_node_flavors, secret_group, secret, kms_key, vpc_ssh_key
- [ ] Report any unusual types

## Architecture Validation

For each flavor:

### Architecture Structure
- [ ] Check if `architecture` section exists

### Architecture Components
- [ ] Check if `descriptions` field exists
- [ ] Check if `features` array exists and count features
- [ ] Verify `diagrams` array exists

For each diagram:
- [ ] Verify `diagram` object exists
- [ ] Verify `url` field exists in diagram
- [ ] Check if `type` field exists in diagram

## Results Reporting

- [ ] Collect all warnings
- [ ] Collect all errors
- [ ] Print warnings summary
- [ ] Print errors summary
- [ ] Report validation status (PASSED/FAILED)
- [ ] Exit with appropriate status code (0 for success, 1 for failure)

---