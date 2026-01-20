# Local Terraform Management (Scenario 1)

## Skill Overview
This skill covers managing Terraform locally on a developer's machine for quick testing and single-user scenarios. The state file is stored on your local machine.

## When to Use
- Quick testing of Terraform templates
- Rapid iteration and development
- Short-term resource creation
- Single-user management
- Learning and experimentation

## Key Concepts

### State File Management
When Terraform executes, it creates, deletes, and modifies resources as instructed by the template's Terraform code. Upon completion, it maintains a record of the infrastructure in a **state file** - a critical map to actual resources that enables proper handling of future updates.

### Advantages
- **Easy Setup**: Minimal configuration required
- **Fast Iteration**: Quick changes and testing cycles
- **Simple Workflow**: Direct execution without additional services
- **Immediate Feedback**: Instant results from terraform commands

### Disadvantages
- **Single User Limitation**: Only the person with the state file can manage resources
- **State File Risk**: Vulnerable to local machine failures, accidental deletion, or corruption
- **No Collaboration**: Team members cannot safely manage the same resources
- **Not Production-Ready**: Unsuitable for long-term resource management

## Best Practices

### 1. State File Protection
- Keep regular backups of the state file
- Store in a secure location on your machine
- Never commit state files to version control (add to .gitignore)
- Document the state file location

### 2. Resource Lifecycle
- Use for short-term resources only
- Clean up resources promptly after testing
- Document resource ownership and purpose
- Plan migration to cloud-based management for long-term resources

### 3. Development Workflow
```bash
# Initialize Terraform
terraform init

# Preview changes
terraform plan

# Apply changes
terraform apply

# Destroy resources when done
terraform destroy
```

### 4. Testing Strategy
- Test template changes incrementally
- Verify resource creation before expanding
- Use terraform plan to preview changes
- Keep test environments isolated

## Migration Path
When you need to:
- Collaborate with team members
- Manage resources long-term
- Reduce state file risk
- Enable multiple users to manage resources

**Consider migrating to**: Cloud-based Terraform with IBM Schematics (see `cloud-schematics-terraform.md`)

## Common Commands
```bash
# Initialize working directory
terraform init

# Validate configuration
terraform validate

# Format code
terraform fmt

# Plan changes
terraform plan -out=tfplan

# Apply changes
terraform apply tfplan

# Show current state
terraform show

# List resources in state
terraform state list

# Destroy all resources
terraform destroy
```

## Troubleshooting

### State File Issues
- **Lost State File**: Resources become unmanaged; manual cleanup may be required
- **Corrupted State**: Use state file backups or terraform state commands to recover
- **State Drift**: Run `terraform refresh` to sync state with actual resources

### Common Errors
- **Lock Errors**: Ensure no other terraform processes are running
- **Provider Issues**: Run `terraform init` to download required providers
- **Resource Conflicts**: Check for existing resources with same names

## Security Considerations
- State files may contain sensitive data (passwords, keys)
- Encrypt state file storage location
- Limit access to the machine with state files
- Rotate credentials if state file is compromised

## When to Avoid
- Production environments
- Long-term resource management
- Multi-user scenarios
- Critical infrastructure
- Compliance-required environments