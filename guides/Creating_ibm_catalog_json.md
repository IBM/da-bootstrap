# Creating an ibm_catalog.json File from Scratch

## Step-by-Step Guide

1. **Create the Base Structure**
   - Start with the root JSON object containing a `products` array
   - This is the foundation for all catalog entries

2. **Define Product Metadata**
   - Add `name`: Unique identifier (lowercase, hyphens)
   - Add `label`: Display name for the catalog
   - Set `product_kind`: Use `"solution"` for deployable architectures
   - Add `tags`: Array of relevant tags (e.g., `["network", "watson"]`) that determine the DAs catalog category. See the command `ibmcloud catalog offering category-options`
   - Add `keywords`: Search terms for catalog discovery
   - Add `short_description`: Brief summary (1-2 sentences)
   - Add `long_description`: Detailed description with any disclaimers
   - Add `offering_docs_url`: Link to documentation
   - Add `offering_icon_url`: Base64-encoded SVG or image URL

3. **Create Product Icon**
   - Design or obtain an SVG icon
   - Convert to base64 format: `data:image/svg+xml;base64,<base64-string>`
   - Alternatively, provide a direct URL to the icon

4. **Define Flavors Array**
   - Add `name`: Flavor identifier (e.g., `"basic"`, `"standard"`, `"advanced"`)
   - Add `label`: Display name for the flavor
   - Set `install_type`: Typically `"fullstack"` for complete deployments
   - Set `working_directory`: Path to Terraform files within the repository (e.g., `"solutions/quickstart"` or `"./"`)
   - Add `compliance`: Object for compliance metadata (can be empty `{}`)

5. **Working with Multiple Flavors**
   - Each flavor represents a different deployment variation (e.g., QuickStart vs Fully Configurable)
   - Flavors can have different:
     - IAM permissions requirements
     - Configuration parameters
     - Architecture diagrams
     - Working directories
   - Use flavors to offer simplified vs advanced deployment options
   - Example: A "quickstart" flavor with minimal configuration and a "fully-configurable" flavor with all options
   - Each flavor is independently deployable and can target different use cases

6. **Specify IAM Permissions**
   - Define required IBM Cloud permissions in `iam_permissions` array
   - Add `service_name`: The IBM Cloud service identifier
   - Add `role_crns`: Array of required role CRNs (e.g., Manager, Administrator)
   - Example: `"crn:v1:bluemix:public:iam::::serviceRole:Manager"`
   
   **Common IBM Cloud Services and Their Permissions:**
   - **containers-kubernetes**: For OpenShift/Kubernetes clusters
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
     - `crn:v1:bluemix:public:iam::::role:Administrator` (platform role)
   - **is** (VPC Infrastructure Services): For VPC resources
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
     - `crn:v1:bluemix:public:iam::::role:Administrator` (platform role)
   - **cloud-object-storage**: For COS instances
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
     - `crn:v1:bluemix:public:iam::::role:Editor` (platform role)
   - **kms**: For Key Protect/HPCS encryption
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
   
   **Note**: Different flavors may require different permission sets based on their features.

7. **Add Architecture Diagrams**
   - Create `architecture` object with `diagrams` array
   - For each diagram, add:
     - `url_proxy.url`: Path to diagram file (SVG recommended)
     - `url_proxy.sha`: SHA-256 hash of the diagram file
     - `caption`: Diagram title
     - `type`: MIME type (e.g., `"image/svg+xml"`)
     - `description`: Detailed diagram description
   - Generate SHA hash using: `shasum -a 256 diagram.svg`

8. **Configure Input Parameters**
   - Create `configuration` array for each Terraform variable
   - For each parameter, define:
     - `key`: Variable name (must match Terraform variable)
     - `type`: Data type (`string`, `password`, `number`, `boolean`, `float`, `int`, `object`)
     - `default_value`: Default value (use `""` for empty, `"__NOT_SET__"` for required)
     - `description`: Parameter description
     - `display_name`: UI-friendly display name
     - `required`: Boolean indicating if parameter is required

9. **Understanding Parameter Types**
   
   **Object Type Parameters:**
   The `object` type is used for complex data structures:
   - Arrays: Use `"default_value": []` for empty arrays
   - Maps/Objects: Use `"default_value": {}` for empty objects
   - Can represent lists of tags, worker pool configurations, subnet metadata, etc.
   - Examples from real deployments:
     - `access_tags`: Array of access management tags
     - `vpc_subnets`: Object containing subnet metadata
     - `worker_pools`: Array of worker pool configurations
     - `addons`: Map of add-on versions
   
   **Special Default Value Patterns:**
   - `""` (empty string): Optional parameter with no default
   - `"__NOT_SET__"`: Required parameter that must be provided by user
   - `null`: Explicitly null value (different from empty)
   - `[]`: Empty array for list-type parameters
   - `{}`: Empty object for map-type parameters
   
   **Example**: VPC ID is required but has no sensible default:
   ```json
   {
       "key": "vpc_id",
       "type": "string",
       "default_value": "__NOT_SET__",
       "required": true
   }
   ```

10. **Add Custom UI Widgets (Optional)**
    - **Note**: Custom UI widgets are **optional** for basic input types (`boolean`, `float`, `int`, `number`, `password`, `string`, `object`)
    - Basic types will render with standard UI controls:
      - `string`: Text input field
      - `password`: Password input field (masked)
      - `number`, `int`, `float`: Numeric input field
      - `boolean`: Checkbox or toggle
      - `object`: JSON editor or structured input
    - For enhanced UI controls, add `custom_config` to parameters
    - Set `type`: Widget type (e.g., `"vpc_region"`, `"resource_group"`, `"ssh_key"`)
    - Set `grouping`: UI section grouping (e.g., `"deployment"`)
    - Add `config_constraints`: Widget-specific constraints
    - Common widget types:
      - `vpc_region`: Region selector with generation filter
      - `resource_group`: Resource group dropdown
      - `ssh_key`: SSH key selector
      - `subnet`: Subnet selector
      - `vpc`: VPC selector
      - `security_group`: Security group selector
    - **When to use custom widgets**:
      - When you need dynamic dropdowns populated from IBM Cloud resources
      - When you want to enforce specific constraints or validation
      - When you need dependent field behavior (e.g., subnets filtered by VPC)
      - When you want to improve user experience with guided selection

11. **Provider Configuration Parameters**
    Some deployable architectures need provider-specific settings:
    - `provider_visibility`: Controls IBM provider endpoint visibility ("public", "private", "public-and-private")
    - Used when deploying to private network environments
    - Typically set to "private" for secure deployments
    - Example:
    ```json
    {
        "key": "provider_visibility",
        "type": "string",
        "description": "Set the visibility value for the IBM terraform provider.",
        "display_name": "Provider Visibility",
        "default_value": "private",
        "required": true
    }
    ```

12. **Validate the JSON**
    - Verify JSON syntax is valid (use a JSON validator)
    - Ensure all required fields are present
    - Check that CRNs and service names are correct
    - Validate SHA hashes match diagram files
    - Confirm parameter keys match Terraform variable names
    
    **Enhanced Validation Checklist:**
    - [ ] All required IAM permissions are listed for each flavor
    - [ ] Architecture diagram SHA hashes are current
    - [ ] Parameter keys exactly match Terraform variable names
    - [ ] Default values match Terraform variable defaults
    - [ ] Boolean parameters use `true`/`false`, not strings
    - [ ] Object types use `[]` or `{}` for empty defaults
    - [ ] Required parameters use `"__NOT_SET__"` when no default exists
    - [ ] Password-type parameters are used for sensitive data
    - [ ] Each flavor has appropriate working_directory path

13. **Test the Configuration**
    - Onboard to IBM Cloud Catalog (private or public)
    - Verify UI renders correctly with all widgets
    - Test deployment with sample values
    - Confirm IAM permission checks work as expected
    - Validate that all parameters are properly captured

## Key Considerations

- **Naming conventions**: Use lowercase with hyphens for IDs
- **Security**: Mark sensitive inputs as `type: "password"`
- **Defaults**: Provide sensible defaults where possible
- **Documentation**: Link to comprehensive docs in `offering_docs_url`
- **Versioning**: Update SHA hashes when diagrams change
- **Testing**: Always test in a private catalog before going public
- **Widget usage**: Only add custom widgets when they provide value over standard inputs
- **Multiple Flavors**: Design flavors for different user personas (beginners vs advanced users)

## Required Files

Along with `ibm_catalog.json`, you need:

1. Terraform configuration files (`.tf`)
2. Architecture diagrams (`.svg` or `.png`)
3. README documentation
4. Optional: `version.tf` for provider versions
5. Optional: `outputs.tf` for output values

## Example Minimal Structure (Without Custom Widgets)

```json
{
    "products": [
        {
            "name": "my-solution",
            "label": "My Solution",
            "product_kind": "solution",
            "tags": ["category"],
            "keywords": ["keyword"],
            "short_description": "Brief description",
            "long_description": "Detailed description",
            "offering_docs_url": "https://docs.example.com",
            "offering_icon_url": "data:image/svg+xml;base64,...",
            "flavors": [
                {
                    "name": "basic",
                    "label": "Basic",
                    "install_type": "fullstack",
                    "working_directory": "./",
                    "compliance": {},
                    "iam_permissions": [
                        {
                            "service_name": "service.name",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::role:Administrator"
                            ]
                        }
                    ],
                    "architecture": {
                        "diagrams": [
                            {
                                "diagram": {
                                    "url_proxy": {
                                        "url": "https://path/to/diagram.svg",
                                        "sha": "sha256hash"
                                    },
                                    "caption": "Architecture",
                                    "type": "image/svg+xml"
                                },
                                "description": "Architecture description"
                            }
                        ]
                    },
                    "configuration": [
                        {
                            "key": "api_key",
                            "type": "password",
                            "description": "API key for authentication",
                            "display_name": "API Key",
                            "required": true
                        },
                        {
                            "key": "cluster_name",
                            "type": "string",
                            "description": "Name of the cluster",
                            "display_name": "Cluster Name",
                            "default_value": "my-cluster",
                            "required": true
                        },
                        {
                            "key": "worker_count",
                            "type": "number",
                            "description": "Number of worker nodes",
                            "display_name": "Worker Count",
                            "default_value": 3,
                            "required": true
                        },
                        {
                            "key": "enable_monitoring",
                            "type": "boolean",
                            "description": "Enable monitoring for the cluster",
                            "display_name": "Enable Monitoring",
                            "default_value": false,
                            "required": false
                        }
                    ]
                }
            ]
        }
    ]
}
```

## Example with Optional Custom Widgets

```json
{
    "products": [
        {
            "name": "my-solution",
            "label": "My Solution",
            "product_kind": "solution",
            "tags": ["category"],
            "keywords": ["keyword"],
            "short_description": "Brief description",
            "long_description": "Detailed description",
            "offering_docs_url": "https://docs.example.com",
            "offering_icon_url": "data:image/svg+xml;base64,...",
            "flavors": [
                {
                    "name": "basic",
                    "label": "Basic",
                    "install_type": "fullstack",
                    "working_directory": "./",
                    "compliance": {},
                    "iam_permissions": [
                        {
                            "service_name": "service.name",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::role:Administrator"
                            ]
                        }
                    ],
                    "architecture": {
                        "diagrams": [
                            {
                                "diagram": {
                                    "url_proxy": {
                                        "url": "https://path/to/diagram.svg",
                                        "sha": "sha256hash"
                                    },
                                    "caption": "Architecture",
                                    "type": "image/svg+xml"
                                },
                                "description": "Architecture description"
                            }
                        ]
                    },
                    "configuration": [
                        {
                            "key": "api_key",
                            "type": "password",
                            "description": "API key for authentication",
                            "display_name": "API Key",
                            "required": true
                        },
                        {
                            "key": "cluster_name",
                            "type": "string",
                            "description": "Name of the cluster",
                            "display_name": "Cluster Name",
                            "default_value": "my-cluster",
                            "required": true
                        },
                        {
                            "key": "region",
                            "type": "string",
                            "description": "IBM Cloud region",
                            "display_name": "Region",
                            "required": true,
                            "custom_config": {
                                "type": "vpc_region",
                                "grouping": "deployment",
                                "config_constraints": {
                                    "generationFilter": "2"
                                }
                            }
                        },
                        {
                            "key": "resource_group_id",
                            "type": "string",
                            "description": "Resource group ID",
                            "display_name": "Resource Group",
                            "required": true,
                            "custom_config": {
                                "type": "resource_group",
                                "grouping": "deployment"
                            }
                        }
                    ]
                }
            ]
        }
    ]
}
```

## Example with Multiple Flavors

```json
{
    "products": [
        {
            "name": "deploy-arch-ibm-ocp-vpc",
            "label": "Red Hat OpenShift Container Platform on VPC",
            "product_kind": "solution",
            "tags": ["ibm_created", "target_terraform", "terraform", "solution", "containers"],
            "keywords": ["openshift", "ocp", "vpc", "kubernetes"],
            "short_description": "Deploy Red Hat OpenShift on IBM Cloud VPC",
            "long_description": "Comprehensive solution for deploying OpenShift clusters",
            "offering_docs_url": "https://github.com/example/docs",
            "offering_icon_url": "data:image/svg+xml;base64,...",
            "flavors": [
                {
                    "name": "quickstart",
                    "label": "QuickStart",
                    "install_type": "fullstack",
                    "working_directory": "solutions/quickstart",
                    "compliance": {},
                    "iam_permissions": [
                        {
                            "service_name": "containers-kubernetes",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                                "crn:v1:bluemix:public:iam::::role:Administrator"
                            ]
                        },
                        {
                            "service_name": "is",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                                "crn:v1:bluemix:public:iam::::role:Administrator"
                            ]
                        }
                    ],
                    "architecture": {
                        "diagrams": [
                            {
                                "diagram": {
                                    "url_proxy": {
                                        "url": "https://path/to/quickstart-diagram.svg",
                                        "sha": "sha256hash"
                                    },
                                    "caption": "QuickStart Architecture",
                                    "type": "image/svg+xml"
                                },
                                "description": "Simplified deployment for development"
                            }
                        ]
                    },
                    "configuration": [
                        {
                            "key": "ibmcloud_api_key",
                            "type": "password",
                            "description": "IBM Cloud API key",
                            "display_name": "API Key",
                            "required": true
                        },
                        {
                            "key": "region",
                            "type": "string",
                            "description": "Region for deployment",
                            "display_name": "Region",
                            "default_value": "us-south",
                            "required": true
                        },
                        {
                            "key": "size",
                            "type": "string",
                            "description": "Cluster size preset",
                            "display_name": "Cluster Size",
                            "default_value": "mini",
                            "required": true
                        }
                    ]
                },
                {
                    "name": "fully-configurable",
                    "label": "Fully Configurable",
                    "install_type": "fullstack",
                    "working_directory": "solutions/fully-configurable",
                    "compliance": {},
                    "iam_permissions": [
                        {
                            "service_name": "containers-kubernetes",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                                "crn:v1:bluemix:public:iam::::role:Administrator"
                            ]
                        },
                        {
                            "service_name": "is",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                                "crn:v1:bluemix:public:iam::::role:Administrator"
                            ]
                        },
                        {
                            "service_name": "kms",
                            "role_crns": [
                                "crn:v1:bluemix:public:iam::::serviceRole:Manager"
                            ]
                        }
                    ],
                    "architecture": {
                        "diagrams": [
                            {
                                "diagram": {
                                    "url_proxy": {
                                        "url": "https://path/to/full-diagram.svg",
                                        "sha": "sha256hash"
                                    },
                                    "caption": "Fully Configurable Architecture",
                                    "type": "image/svg+xml"
                                },
                                "description": "Production-ready with all features"
                            }
                        ]
                    },
                    "configuration": [
                        {
                            "key": "ibmcloud_api_key",
                            "type": "password",
                            "description": "IBM Cloud API key",
                            "display_name": "API Key",
                            "required": true
                        },
                        {
                            "key": "vpc_id",
                            "type": "string",
                            "description": "Existing VPC ID",
                            "display_name": "VPC ID",
                            "default_value": "__NOT_SET__",
                            "required": true
                        },
                        {
                            "key": "worker_pools",
                            "type": "object",
                            "description": "Worker pool configurations",
                            "display_name": "Worker Pools",
                            "default_value": "__NOT_SET__",
                            "required": true
                        },
                        {
                            "key": "kms_config",
                            "type": "object",
                            "description": "KMS configuration",
                            "display_name": "KMS Config",
                            "default_value": null,
                            "required": false
                        },
                        {
                            "key": "enable_secrets_manager_integration",
                            "type": "boolean",
                            "description": "Enable Secrets Manager",
                            "display_name": "Enable Secrets Manager",
                            "default_value": false,
                            "required": false
                        }
                    ]
                }
            ]
        }
    ]
}
```

## Comparison: Standard vs Custom Widgets

### Standard Input (No Custom Widget)
```json
{
    "key": "cluster_name",
    "type": "string",
    "description": "Name of the cluster",
    "display_name": "Cluster Name",
    "default_value": "my-cluster",
    "required": true
}
```
**Result**: Simple text input field where users type the cluster name

### Custom Widget Input
```json
{
    "key": "region",
    "type": "string",
    "description": "IBM Cloud region",
    "display_name": "Region",
    "required": true,
    "custom_config": {
        "type": "vpc_region",
        "grouping": "deployment",
        "config_constraints": {
            "generationFilter": "2"
        }
    }
}
```
**Result**: Dropdown populated with available VPC regions, filtered by generation

## Troubleshooting Common Issues

### Parameter Not Appearing in UI
- Verify `key` matches Terraform variable name exactly
- Check that parameter is in correct flavor's configuration array
- Ensure JSON syntax is valid
- Confirm the parameter is not hidden by conditional logic

### Default Value Not Working
- Use `""` for optional strings, not `null`
- Use `[]` for empty arrays, not `null`
- Use `"__NOT_SET__"` for required parameters without defaults
- Verify the default value type matches the parameter type

### IAM Permission Errors
- Verify service_name matches IBM Cloud service identifier
- Check role CRNs are complete and correctly formatted
- Ensure all required services are listed for the flavor
- Test with a user account that has the specified permissions

### Diagram Not Displaying
- Verify SHA hash matches current file (regenerate with `shasum -a 256`)
- Check URL is accessible and returns the correct content
- Ensure MIME type matches file format
- Verify the diagram file is committed to the repository

### Configuration Not Saving
- Check for JSON syntax errors
- Verify all required fields have values
- Ensure object types have proper structure
- Test with minimal configuration first

### Flavor Not Deploying
- Verify working_directory path is correct
- Check that all Terraform files exist in the specified directory
- Ensure IAM permissions are sufficient
- Review Terraform logs for specific errors

## Best Practices

1. **Start Simple**: Begin with standard input types and add custom widgets only where needed
2. **User Experience**: Use custom widgets for complex selections (regions, resource groups, VPCs)
3. **Validation**: Leverage custom widgets for built-in validation and constraints
4. **Documentation**: Provide clear descriptions for all parameters, regardless of widget type
5. **Testing**: Test both with and without custom widgets to ensure fallback behavior works
6. **Grouping**: Use `grouping` in `custom_config` to organize related parameters, even for standard inputs
7. **Multiple Flavors**: Design flavors for different user personas and use cases
8. **Security First**: Always use `password` type for sensitive data
9. **Defaults Matter**: Provide sensible defaults to improve user experience
10. **Keep It Updated**: Regularly update SHA hashes and version numbers

## Complete Real-World Example

See the [terraform-ibm-base-ocp-vpc](https://github.com/terraform-ibm-modules/terraform-ibm-base-ocp-vpc/blob/main/ibm_catalog.json) repository for a production example featuring:
- Two flavors (QuickStart and Fully Configurable)
- 15+ configuration parameters per flavor
- Multiple IAM permission sets
- Architecture diagrams with descriptions
- Security group management
- KMS integration
- Secrets Manager integration
- Worker pool configuration
- Network customization options
- Comprehensive tagging support
- Advanced cluster features

## Additional Resources

- [IBM Cloud Catalog Management API](https://cloud.ibm.com/apidocs/resource-catalog/private-catalog)
- [Deployable Architecture Documentation](https://cloud.ibm.com/docs/secure-enterprise)
- [Terraform IBM Cloud Provider](https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs)
- [IBM Cloud CLI Catalog Commands](https://cloud.ibm.com/docs/cli?topic=cli-manage-catalogs-plugin)
- [Context-Based Restrictions](https://cloud.ibm.com/docs/account?topic=account-context-restrictions-whatis)