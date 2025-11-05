# Creating an ibm_catalog.json File from Scratch

## Step-by-Step Guide

1. **Create the Base Structure**
   - Start with the root JSON object containing a `products` array
   - This is the foundation for all catalog entries

2. **Define Product Metadata**
   - Add `name`: Unique identifier (lowercase, hyphens)
   - Add `label`: Display name for the catalog
   - Set `product_kind`: Use `"solution"` for deployable architectures
   - Add `tags`: Array of relevant tags (e.g., `["network", "watson"]`) that determine the DAs catalog category.  See the command `ibmcloud catalog offering category-options`
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
   - Set `working_directory`: Path to Terraform files within the repository (usually `"./"`)
   - Add `compliance`: Object for compliance metadata (can be empty `{}`)

5. **Specify IAM Permissions**
   - Define required IBM Cloud permissions in `iam_permissions` array
   - Add `service_name`: The IBM Cloud service identifier
   - Add `role_crns`: Array of required role CRNs (e.g., Manager, Administrator)
   - Example: `"crn:v1:bluemix:public:iam::::serviceRole:Manager"`

6. **Add Architecture Diagrams**
   - Create `architecture` object with `diagrams` array
   - For each diagram, add:
     - `url_proxy.url`: Path to diagram file (SVG recommended)
     - `url_proxy.sha`: SHA-256 hash of the diagram file
     - `caption`: Diagram title
     - `type`: MIME type (e.g., `"image/svg+xml"`)
     - `description`: Detailed diagram description
   - Generate SHA hash using: `shasum -a 256 diagram.svg`

7. **Configure Input Parameters**
   - Create `configuration` array for each Terraform variable
   - For each parameter, define:
     - `key`: Variable name (must match Terraform variable)
     - `type`: Data type (`string`, `password`, `number`, `boolean`, `float`, `int`, `object`)
     - `default_value`: Default value (use `""` for empty, `"__NOT_SET__"` for required)
     - `description`: Parameter description
     - `display_name`: UI-friendly display name
     - `required`: Boolean indicating if parameter is required

8. **Add Custom UI Widgets (Optional)**
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

9. **Validate the JSON**
   - Verify JSON syntax is valid (use a JSON validator)
   - Ensure all required fields are present
   - Check that CRNs and service names are correct
   - Validate SHA hashes match diagram files
   - Confirm parameter keys match Terraform variable names

10. **Test the Configuration**
    - Onboard to IBM Cloud Catalog (private or public)
    - Verify UI renders correctly with all widgets
    - Test deployment with sample values
    - Confirm IAM permission checks work as expected
    - Validate that all parameters are properly captured

## Key Considerations

- **Naming conventions**: Use lowercase with hyphens for IDs
- **Security**: Mark sensitive inputs as `type: "password"`
- **Defaults**: Provide sensible defaults where possible
- **Grouping**: Use `custom_config.grouping` to organize UI sections (optional but recommended)
- **Documentation**: Link to comprehensive docs in `offering_docs_url`
- **Versioning**: Update SHA hashes when diagrams change
- **Testing**: Always test in a private catalog before going public
- **Widget usage**: Only add custom widgets when they provide value over standard inputs

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

## Best Practices

1. **Start Simple**: Begin with standard input types and add custom widgets only where needed
2. **User Experience**: Use custom widgets for complex selections (regions, resource groups, VPCs)
3. **Validation**: Leverage custom widgets for built-in validation and constraints
4. **Documentation**: Provide clear descriptions for all parameters, regardless of widget type
5. **Testing**: Test both with and without custom widgets to ensure fallback behavior works
6. **Grouping**: Use `grouping` in `custom_config` to organize related parameters, even for standard inputs

## Additional Resources

- [IBM Cloud Catalog Management API](https://cloud.ibm.com/apidocs/resource-catalog/private-catalog)
- [Deployable Architecture Documentation](https://cloud.ibm.com/docs/secure-enterprise)
- [Terraform IBM Cloud Provider](https://registry.terraform.io/providers/IBM-Cloud/ibm/latest/docs)