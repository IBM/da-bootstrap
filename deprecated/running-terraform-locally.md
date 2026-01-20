# Guide: Running Terraform Locally

## Overview

This guide provides detailed instructions for running Terraform automation locally on your machine using the Terraform CLI.

## Prerequisites

- Terraform CLI installed (version matching your project's `version.tf`)
- Required provider credentials configured (e.g., IBM Cloud API key)
- Access to the Terraform project directory

## When to Use Local Execution

- Rapid iteration and testing
- Debugging and syntax validation
- Private development environment
- No need for shared state
- Frequent changes without committing to repository

## Steps

### 1. Navigate to Your Terraform Directory

```bash
cd /path/to/your/terraform/project
```

### 2. Initialize Terraform

```bash
terraform init
```

This downloads required providers and initializes the backend.

### 3. Create a Variables File (Optional)

Create `terraform.tfvars` or `terraform.tfvars.json` with your variable values:

```hcl
# terraform.tfvars example
variable_name = "value"
another_variable = 123
```

### 4. Validate Configuration

```bash
terraform validate
```

Checks syntax and configuration validity.

### 5. Generate Execution Plan

```bash
terraform plan
# Or with variables file:
terraform plan -var-file="terraform.tfvars"
```

Review the plan to understand what resources will be created, modified, or destroyed.

### 6. Apply Configuration

```bash
terraform apply
# Or with variables file:
terraform apply -var-file="terraform.tfvars"
```

Type `yes` when prompted to confirm the changes.

### 7. Review Outputs

```bash
terraform output
```

View the output values defined in your Terraform configuration.

## State Management

- State file (`terraform.tfstate`) is stored locally in the project directory
- Keep state file secure and backed up
- Do not commit state file to version control

## Cleanup

To destroy resources when done:

```bash
terraform destroy
```

## Troubleshooting

### Common Issues

- **Provider authentication errors**: Ensure credentials are properly configured
- **Version conflicts**: Check that Terraform and provider versions match requirements
- **State lock errors**: Remove `.terraform.tfstate.lock.info` if process was interrupted

## Next Steps

- Consider moving to cloud execution for team collaboration
- Explore remote state backends for shared state management
- Review [Guide: Running Terraform with IBM Cloud Schematics](./running-terraform-with-schematics.md)