# Creating an ibm_catalog.json File from Scratch - Complete Guide

## Step-by-Step Guide

1. **Create the Base Structure**
   - Start with the root JSON object containing a `products` array
   - This is the foundation for all catalog entries

2. **Define Product Metadata**
   - Add `name`: Unique identifier (lowercase, hyphens)
   - Add `label`: Display name for the catalog
   - Set `product_kind`: Use `"solution"` for deployable architectures
   - Add `provider_name`: Provider attribution (e.g., "IBM")
   - Add `tags`: Array of relevant tags (e.g., `["network", "watson"]`) that determine the DAs catalog category. See the command `ibmcloud catalog offering category-options`
   - Add `keywords`: Search terms for catalog discovery
   - Add `short_description`: Brief summary (1-2 sentences)
   - Add `long_description`: Detailed description with any disclaimers
   - Add `offering_docs_url`: Link to documentation
   - Add `offering_icon_url`: Base64-encoded SVG or image URL
   - Add `features`: Array of product-level feature highlights (optional but recommended)

3. **Add Product Features Array (Recommended)**
   
   Add a `features` array at the product level to highlight key capabilities:
   
   ```json
   {
     "products": [{
       "name": "my-solution",
       "features": [
         {
           "title": "Feature Name",
           "description": "Detailed description with [links](https://docs.example.com)"
         }
       ]
     }]
   }
   ```
   
   **Benefits:**
   - Provides marketing-friendly feature highlights
   - Supports rich text with Markdown links
   - Appears prominently in catalog UI
   - Helps users understand value proposition
   
   **Best Practices:**
   - Use 5-9 features for optimal display
   - Include documentation links in descriptions
   - Focus on business value, not technical details
   - Mention optional integrations with other services

4. **Create Product Icon**
   - Design or obtain an SVG icon
   - Convert to base64 format: `data:image/svg+xml;base64,<base64-string>`
   - Alternatively, provide a direct URL to the icon

5. **Define Flavors Array**
   - Add `name`: Flavor identifier (e.g., `"basic"`, `"standard"`, `"advanced"`)
   - Add `label`: Display name for the flavor
   - Add `index`: Display order (lower numbers appear first)
   - Add `short_description`: Brief flavor description
   - Set `install_type`: Typically `"fullstack"` for complete deployments
   - Set `working_directory`: Path to Terraform files within the repository (e.g., `"solutions/quickstart"` or `"./"`)
   - Add `release_notes_url`: Link to version-specific release notes
   - Add `terraform_version`: Specify Terraform version (e.g., "1.12.2")
   - Add `ignore_readme`: Set to `true` to hide README in catalog
   - Add `compliance`: Object for compliance metadata (can be empty `{}`)
   - Add `dependency_version_2`: Set to `true` if using dependencies

6. **Working with Multiple Flavors**
   - Each flavor represents a different deployment variation (e.g., QuickStart vs Fully Configurable)
   - Flavors can have different:
     - IAM permissions requirements
     - Configuration parameters
     - Architecture diagrams
     - Working directories
     - Dependencies
   - Use flavors to offer simplified vs advanced deployment options
   - Example: A "quickstart" flavor with minimal configuration and a "fully-configurable" flavor with all options
   - Each flavor is independently deployable and can target different use cases
   - Use `index` to control display order in the UI

7. **Specify IAM Permissions with Notes**
   - Define required IBM Cloud permissions in `iam_permissions` array
   - Add `service_name`: The IBM Cloud service identifier
   - Add `role_crns`: Array of required role CRNs (e.g., Manager, Administrator)
   - Add `notes`: Explanatory text for why the permission is needed
   - Example: `"crn:v1:bluemix:public:iam::::serviceRole:Manager"`
   
   **Enhanced IAM Permission Format:**
   ```json
   {
     "iam_permissions": [
       {
         "service_name": "Resource group only",
         "role_crns": [
           "crn:v1:bluemix:public:iam::::role:Viewer"
         ],
         "notes": "Viewer access is required in the resource group you want to provision in."
       },
       {
         "service_name": "kms",
         "role_crns": [
           "crn:v1:bluemix:public:iam::::serviceRole:Manager",
           "crn:v1:bluemix:public:iam::::role:Editor"
         ],
         "notes": "[Optional] Required if Key Protect is used for encryption."
       }
     ]
   }
   ```
   
   **Common IBM Cloud Services and Their Permissions:**
   - **containers-kubernetes**: For OpenShift/Kubernetes clusters
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
     - `crn:v1:bluemix:public:iam::::role:Administrator` (platform role)
   - **is** or **is.vpc** (VPC Infrastructure Services): For VPC resources
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
     - `crn:v1:bluemix:public:iam::::role:Administrator` or `Editor` (platform role)
   - **cloud-object-storage**: For COS instances
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
     - `crn:v1:bluemix:public:iam::::role:Editor` (platform role)
   - **kms**: For Key Protect/HPCS encryption
     - `crn:v1:bluemix:public:iam::::serviceRole:Manager` (serviceRole)
   - **iam-identity**: For API key creation
     - `crn:v1:bluemix:public:iam::::role:Operator` (platform role)
     - `crn:v1:bluemix:public:iam-identity::::serviceRole:UserApiKeyCreator` (serviceRole)
   
   **Best Practices:**
   - Use `[Optional]` prefix for conditional permissions
   - Explain why each permission is needed
   - Mention which features require which permissions
   - Include special cases (e.g., "Resource group only")
   - Different flavors may require different permission sets based on their features

8. **Add Architecture Diagrams and Features**
   - Create `architecture` object with `diagrams` array
   - Optionally add `features` array for flavor-specific features
   - For each diagram, add:
     - `url` or `url_proxy.url`: Path to diagram file (SVG recommended)
     - `url_proxy.sha`: SHA-256 hash of the diagram file (for url_proxy)
     - `caption`: Diagram title
     - `type`: MIME type (e.g., `"image/svg+xml"`)
     - `description`: Detailed diagram description
   - Generate SHA hash using: `shasum -a 256 diagram.svg`
   
   **Direct URL** (simpler):
   ```json
   {
     "diagram": {
       "url": "https://raw.githubusercontent.com/org/repo/main/diagram.svg",
       "caption": "Architecture Diagram",
       "type": "image/svg+xml"
     }
   }
   ```
   
   **URL Proxy** (with SHA verification):
   ```json
   {
     "diagram": {
       "url_proxy": {
         "url": "https://raw.githubusercontent.com/org/repo/main/diagram.svg",
         "sha": "df289f85574f97c36f3f94ab9dd761654e8dd19ccaeee5bc15fe0c8038054cef"
       },
       "caption": "Architecture Diagram",
       "type": "image/svg+xml"
     }
   }
   ```
   
   Use `url_proxy` with SHA for integrity verification.
   
   **Architecture Features:**
   ```json
   {
     "architecture": {
       "features": [
         {
           "title": "Feature specific to this flavor",
           "description": "Detailed explanation"
         }
       ],
       "diagrams": []
     }
   }
   ```

9. **Configure Input Parameters**
   - Create `configuration` array for each Terraform variable
   - For each parameter, define:
     - `key`: Variable name (must match Terraform variable)
     - `type`: Data type (`string`, `password`, `number`, `boolean`, `float`, `int`, `object`, `array`)
     - `default_value`: Default value (use `""` for empty, `"__NOT_SET__"` for required)
     - `description`: Parameter description
     - `display_name`: UI-friendly display name
     - `required`: Boolean indicating if parameter is required
     - `hidden`: Set to `true` to hide from UI (optional)
     - `virtual`: Set to `true` for parameters that don't map to Terraform (optional)
     - `value_constraints`: Array of validation rules (optional)
     - `random_string`: Auto-generate random suffixes (optional)
     - `options`: Array of dropdown options with descriptions (optional)
     - `custom_config`: Enhanced UI widgets (optional)

10. **Understanding Parameter Types**
    
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

11. **Advanced Parameter Features**
    
    ### Hidden Parameters
    
    Use `"hidden": true` to hide parameters from the UI while still allowing them to be set programmatically or through dependencies:
    
    ```json
    {
      "key": "advanced_setting",
      "type": "string",
      "hidden": true,
      "default_value": "auto"
    }
    ```
    
    **Use Cases:**
    - Advanced settings not needed by typical users
    - Parameters controlled by dependencies
    - Internal configuration values
    - Feature flags for future capabilities
    
    ### Virtual Parameters
    
    Use `"virtual": true` for parameters that don't directly map to Terraform variables but control dependency behavior:
    
    ```json
    {
      "key": "enable_platform_metrics",
      "type": "boolean",
      "virtual": true,
      "required": true,
      "description": "Controls whether monitoring instance collects platform metrics"
    }
    ```
    
    ### Value Constraints
    
    Add validation rules using `value_constraints`:
    
    ```json
    {
      "key": "prefix",
      "type": "string",
      "value_constraints": [
        {
          "type": "regex",
          "description": "Prefix must begin with lowercase letter, contain only lowercase letters, digits, and hyphens",
          "value": "^[a-z](?!.*--)(?:[a-z0-9-]{0,14}[a-z0-9])?$"
        }
      ]
    }
    ```
    
    **Common Constraint Types:**
    - **regex**: Pattern matching for strings
    - **length**: Min/max length validation
    - **range**: Min/max value for numbers
    
    **CRN Validation Example:**
    ```json
    {
      "key": "existing_kms_instance_crn",
      "value_constraints": [
        {
          "type": "regex",
          "description": "The value provided for 'existing_kms_instance_crn' is not valid.",
          "value": "^__NULL__$|^crn:(.*:){3}(kms|hs-crypto):(.*:){2}[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}::$"
        }
      ]
    }
    ```
    
    ### Random String Generation
    
    Auto-generate random suffixes for resource names:
    
    ```json
    {
      "key": "prefix",
      "required": true,
      "default_value": "dev",
      "random_string": {
        "length": 4
      }
    }
    ```
    
    This generates values like `dev-a3f9` automatically.
    
    ### Options with Detailed Descriptions
    
    Provide rich option descriptions for dropdown selections:
    
    ```json
    {
      "key": "size",
      "type": "string",
      "options": [
        {
          "description": "bx2.4x16 with 4 vCPU and 16 GB memory, 2 nodes across 2 zones.",
          "displayname": "Mini",
          "value": "mini"
        },
        {
          "description": "bx2.8x32 with 8 vCPU and 32 GB memory, 3 nodes across 3 zones.",
          "displayname": "Small",
          "value": "small"
        }
      ]
    }
    ```

12. **Add Custom UI Widgets (Optional)**
    - **Note**: Custom UI widgets are **optional** for basic input types (`boolean`, `float`, `int`, `number`, `password`, `string`, `object`)
    - Basic types will render with standard UI controls:
      - `string`: Text input field
      - `password`: Password input field (masked)
      - `number`, `int`, `float`: Numeric input field
      - `boolean`: Checkbox or toggle
      - `object`: JSON editor or structured input
    - For enhanced UI controls, add `custom_config` to parameters
    - Set `type`: Widget type (e.g., `"vpc_region"`, `"resource_group"`, `"ssh_key"`, `"code_editor"`)
    - Set `grouping`: UI section grouping (e.g., `"deployment"`)
    - Set `original_grouping`: Original grouping value
    - Add `config_constraints`: Widget-specific constraints
    - Common widget types:
      - `vpc_region`: Region selector with generation filter
      - `resource_group`: Resource group dropdown
      - `ssh_key`: SSH key selector
      - `subnet`: Subnet selector
      - `vpc`: VPC selector
      - `security_group`: Security group selector
      - `code_editor`: For complex JSON/HCL configurations
      - `array`: For array inputs with type constraints
    - **When to use custom widgets**:
      - When you need dynamic dropdowns populated from IBM Cloud resources
      - When you want to enforce specific constraints or validation
      - When you need dependent field behavior (e.g., subnets filtered by VPC)
      - When you want to improve user experience with guided selection
      - For complex configurations that benefit from code editor
    
    **Code Editor Widget Example:**
    ```json
    {
      "key": "worker_pools",
      "type": "array",
      "custom_config": {
        "type": "code_editor",
        "grouping": "deployment",
        "original_grouping": "deployment"
      }
    }
    ```
    
    **Array Type Configuration:**
    ```json
    {
      "key": "access_tags",
      "type": "array",
      "custom_config": {
        "type": "array",
        "grouping": "deployment",
        "original_grouping": "deployment",
        "config_constraints": {
          "type": "string"
        }
      }
    }
    ```
    
    **Display Name Override:**
    ```json
    {
      "key": "existing_resource_group_name",
      "display_name": "resource_group",
      "custom_config": {
        "type": "resource_group",
        "grouping": "deployment",
        "config_constraints": {
          "identifier": "rg_name"
        }
      }
    }
    ```

13. **Provider Configuration Parameters**
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
        "required": true,
        "options": [
          {
            "displayname": "private",
            "value": "private"
          },
          {
            "displayname": "public",
            "value": "public"
          },
          {
            "displayname": "public-and-private",
            "value": "public-and-private"
          }
        ]
    }
    ```

14. **Configure Dependencies (Advanced)**
    
    Dependencies allow your deployable architecture to compose with other DAs, creating a layered architecture approach.
    
    ### Key Dependency Attributes:
    
    ```json
    {
      "dependencies": [
        {
          "name": "deploy-arch-ibm-vpc",
          "description": "User-friendly description of what this dependency provides",
          "id": "uuid-global",
          "version": "v1.2.3",
          "flavors": ["flavor-name"],
          "catalog_id": "catalog-uuid",
          "optional": false,
          "on_by_default": true,
          "input_mapping": []
        }
      ],
      "dependency_version_2": true
    }
    ```
    
    ### Dependency Fields Explained:
    
    - **name**: Unique identifier for the dependency DA
    - **description**: User-facing explanation of why this dependency is needed
    - **id**: Global ID of the dependency DA in the catalog
    - **version**: Specific version to use (enables version pinning)
    - **flavors**: Array of flavor names from the dependency DA to use
    - **catalog_id**: Catalog where the dependency resides
    - **optional**: `true` = user can opt-out, `false` = required
    - **on_by_default**: `true` = pre-selected in UI, `false` = user must opt-in
    - **input_mapping**: Array defining how inputs/outputs flow between DAs
    - **dependency_version_2**: Set to `true` at flavor level to enable v2 features
    
    ### Input Mapping Patterns:
    
    **1. Reference Version Input (Pass-through)**
    ```json
    {
      "dependency_input": "prefix",
      "version_input": "prefix",
      "reference_version": true
    }
    ```
    Passes the parent DA's input directly to the dependency.
    
    **2. Dependency Output to Version Input**
    ```json
    {
      "dependency_output": "vpc_crn",
      "version_input": "existing_vpc_crn"
    }
    ```
    Takes an output from the dependency and uses it as input in the parent DA.
    
    **3. Static Value Assignment**
    ```json
    {
      "version_input": "enable_feature",
      "value": true
    }
    ```
    Sets a specific value in the parent DA when the dependency is selected.
    
    ### Real-World Dependency Example:
    
    ```json
    {
      "dependencies": [
        {
          "name": "deploy-arch-ibm-slz-vpc",
          "description": "Configure the VPC and subnets required to deploy your OpenShift cluster.",
          "id": "9fc0fa64-27af-4fed-9dce-47b3640ba739-global",
          "version": "v8.8.3",
          "flavors": ["fully-configurable"],
          "catalog_id": "1082e7d2-5e2f-0a11-a3bc-f88a8e1931fc",
          "optional": false,
          "on_by_default": true,
          "input_mapping": [
            {
              "dependency_input": "prefix",
              "version_input": "prefix",
              "reference_version": true
            },
            {
              "dependency_input": "region",
              "version_input": "region",
              "reference_version": true
            },
            {
              "dependency_output": "vpc_crn",
              "version_input": "existing_vpc_crn"
            }
          ]
        },
        {
          "name": "deploy-arch-ibm-kms",
          "description": "Integrate IBM Key Protect to manage encryption keys. If unselected, encryption is still applied using IBM-managed keys.",
          "id": "2cad4789-fa90-4886-9c9e-857081c273ee-global",
          "version": "v5.4.8",
          "flavors": ["fully-configurable"],
          "catalog_id": "7a4d68b4-cf8b-40cd-a3d1-f49aff526eb3",
          "optional": true,
          "on_by_default": true,
          "input_mapping": [
            {
              "version_input": "kms_encryption_enabled",
              "value": true
            },
            {
              "dependency_output": "kms_instance_crn",
              "version_input": "existing_kms_instance_crn"
            }
          ]
        }
      ]
    }
    ```
    
    ### Dependency Design Patterns:
    
    **Required Foundation Dependencies:**
    - VPC/Network infrastructure
    - Object Storage for registries
    - Set `"optional": false` and `"on_by_default": true`
    
    **Optional Enhancement Dependencies:**
    - Encryption (KMS)
    - Observability (Logs, Monitoring, Activity Tracker)
    - Security (Secrets Manager, Workload Protection)
    - Set `"optional": true` and `"on_by_default": true` (or `false`)
    
    **Layered Dependencies:**
    Dependencies can depend on each other (e.g., Cloud Logs depends on COS and KMS). Use `reference_version: true` to pass shared parameters through the chain.

15. **Validate the JSON**
    - Verify JSON syntax is valid (use a JSON validator)
    - Ensure all required fields are present
    - Check that CRNs and service names are correct
    - Validate SHA hashes match diagram files
    - Confirm parameter keys match Terraform variable names
    
    **Complete Validation Checklist:**
    - [ ] All required IAM permissions are listed for each flavor
    - [ ] IAM permissions include explanatory notes
    - [ ] Architecture diagram SHA hashes are current
    - [ ] Parameter keys exactly match Terraform variable names
    - [ ] Default values match Terraform variable defaults
    - [ ] Boolean parameters use `true`/`false`, not strings
    - [ ] Object types use `[]` or `{}` for empty defaults
    - [ ] Required parameters use `"__NOT_SET__"` when no default exists
    - [ ] Password-type parameters are used for sensitive data
    - [ ] Each flavor has appropriate working_directory path
    - [ ] Multiple flavors have distinct configurations
    - [ ] Optional feature flags have corresponding configuration parameters
    - [ ] `dependency_version_2` is set to `true` if using dependencies
    - [ ] All dependency IDs and catalog IDs are correct
    - [ ] Dependency versions are pinned to specific releases
    - [ ] Input mappings correctly reference dependency outputs
    - [ ] Optional dependencies have clear descriptions explaining their value
    - [ ] Hidden parameters have appropriate defaults
    - [ ] Virtual parameters are documented
    - [ ] Value constraints include user-friendly error messages
    - [ ] Features array highlights key capabilities
    - [ ] Provider name is set at product level
    - [ ] Flavor index controls display order appropriately
    - [ ] Release notes URL is current
    - [ ] Terraform version matches your code

16. **Test the Configuration**
    - Onboard to IBM Cloud Catalog (private or public)
    - Verify UI renders correctly with all widgets
    - Test deployment with sample values
    - Confirm IAM permission checks work as expected
    - Validate that all parameters are properly captured
    - Test dependency selection and input mapping
    - Verify hidden and virtual parameters work correctly

## Key Considerations

- **Naming conventions**: Use lowercase with hyphens for IDs
- **Security**: Mark sensitive inputs as `type: "password"`
- **Defaults**: Provide sensible defaults where possible
- **Grouping**: Use `grouping` in `custom_config` to organize related parameters
- **Documentation**: Link to comprehensive docs in `offering_docs_url`
- **Versioning**: Update SHA hashes when diagrams change
- **Testing**: Always test in a private catalog before going public
- **Widget usage**: Only add custom widgets when they provide value over standard inputs
- **Multiple Flavors**: Design flavors for different user personas (beginners vs advanced users)
- **Dependencies**: Use for composability and reusability
- **Features**: Highlight value proposition at product and flavor levels
- **IAM Notes**: Always explain why permissions are needed
- **Validation**: Use constraints to prevent user errors

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
            "provider_name": "IBM",
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
                    "index": 1,
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
                    "index": 2,
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

## Complete Production Example with Dependencies

```json
{
  "products": [
    {
      "name": "deploy-arch-ibm-ocp-vpc",
      "label": "OpenShift on VPC Landing Zone",
      "product_kind": "solution",
      "provider_name": "IBM",
      "tags": ["ibm_created", "target_terraform", "solution", "compute"],
      "keywords": ["openshift", "vpc", "kubernetes", "containers"],
      "short_description": "Deploy OpenShift with integrated security and observability",
      "long_description": "Comprehensive solution for deploying production-ready OpenShift clusters with optional integrations for encryption, monitoring, logging, and compliance.",
      "offering_docs_url": "https://cloud.ibm.com/docs/solution",
      "offering_icon_url": "https://example.com/icon.svg",
      "features": [
        {
          "title": "Multi-zone High Availability",
          "description": "Deploys clusters across multiple availability zones for resilience"
        },
        {
          "title": "Integrated Security",
          "description": "Optional [Key Protect](https://cloud.ibm.com/docs/key-protect) encryption and [Secrets Manager](https://cloud.ibm.com/docs/secrets-manager) integration"
        },
        {
          "title": "Comprehensive Observability",
          "description": "Optional integration with [Cloud Logs](https://cloud.ibm.com/docs/cloud-logs), [Monitoring](https://cloud.ibm.com/docs/monitoring), and [Activity Tracker](https://cloud.ibm.com/docs/activity-tracker)"
        }
      ],
      "flavors": [
        {
          "name": "quickstart",
          "label": "QuickStart",
          "index": 1,
          "short_description": "Simplified setup for development and testing",
          "install_type": "fullstack",
          "working_directory": "solutions/quickstart",
          "release_notes_url": "https://cloud.ibm.com/docs/solution?topic=solution-relnotes",
          "terraform_version": "1.12.2",
          "ignore_readme": true,
          "compliance": {},
          "iam_permissions": [
            {
              "service_name": "Resource group only",
              "role_crns": ["crn:v1:bluemix:public:iam::::role:Viewer"],
              "notes": "Viewer access required in the target resource group."
            },
            {
              "service_name": "containers-kubernetes",
              "role_crns": [
                "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                "crn:v1:bluemix:public:iam::::role:Administrator"
              ],
              "notes": "Required to create and manage the OpenShift cluster."
            },
            {
              "service_name": "is.vpc",
              "role_crns": ["crn:v1:bluemix:public:iam::::role:Editor"],
              "notes": "Required to create VPC infrastructure."
            }
          ],
          "architecture": {
            "features": [
              {
                "title": "Simplified Configuration",
                "description": "Pre-configured settings for rapid deployment"
              }
            ],
            "diagrams": [
              {
                "diagram": {
                  "url": "https://example.com/quickstart-diagram.svg",
                  "caption": "QuickStart Architecture",
                  "type": "image/svg+xml"
                },
                "description": "Lightweight OpenShift deployment for development"
              }
            ]
          },
          "configuration": [
            {
              "key": "ibmcloud_api_key",
              "type": "password",
              "required": true
            },
            {
              "key": "prefix",
              "type": "string",
              "required": true,
              "default_value": "dev",
              "random_string": {
                "length": 4
              },
              "value_constraints": [
                {
                  "type": "regex",
                  "description": "Must start with lowercase letter, contain only lowercase letters, digits, and hyphens",
                  "value": "^[a-z](?!.*--)(?:[a-z0-9-]{0,14}[a-z0-9])?$"
                }
              ]
            },
            {
              "key": "region",
              "type": "string",
              "required": true,
              "custom_config": {
                "type": "vpc_region",
                "grouping": "deployment",
                "config_constraints": {
                  "generationType": "2"
                }
              }
            },
            {
              "key": "size",
              "type": "string",
              "required": true,
              "default_value": "mini",
              "options": [
                {
                  "displayname": "Mini",
                  "description": "2 nodes, 4 vCPU, 16 GB RAM each",
                  "value": "mini"
                },
                {
                  "displayname": "Small",
                  "description": "3 nodes, 8 vCPU, 32 GB RAM each",
                  "value": "small"
                }
              ]
            }
          ]
        },
        {
          "name": "standard",
          "label": "Standard",
          "index": 2,
          "short_description": "Production-ready with optional integrations",
          "install_type": "fullstack",
          "working_directory": "solutions/standard",
          "release_notes_url": "https://cloud.ibm.com/docs/solution?topic=solution-relnotes",
          "terraform_version": "1.12.2",
          "ignore_readme": true,
          "compliance": {},
          "dependency_version_2": true,
          "iam_permissions": [
            {
              "service_name": "Resource group only",
              "role_crns": ["crn:v1:bluemix:public:iam::::role:Viewer"],
              "notes": "Viewer access required in the target resource group."
            },
            {
              "service_name": "containers-kubernetes",
              "role_crns": [
                "crn:v1:bluemix:public:iam::::serviceRole:Manager",
                "crn:v1:bluemix:public:iam::::role:Administrator"
              ],
              "notes": "Required to create and manage the OpenShift cluster."
            },
            {
              "service_name": "kms",
              "role_crns": [
                "crn:v1:bluemix:public:iam::::serviceRole:Manager"
              ],
              "notes": "[Optional] Required if Key Protect encryption is enabled."
            }
          ],
          "architecture": {
            "diagrams": [
              {
                "diagram": {
                  "url_proxy": {
                    "url": "https://example.com/standard-diagram.svg",
                    "sha": "abc123..."
                  },
                  "caption": "Standard Architecture",
                  "type": "image/svg+xml"
                },
                "description": "Production-ready OpenShift with optional security and observability"
              }
            ]
          },
          "configuration": [
            {
              "key": "ibmcloud_api_key",
              "type": "password",
              "required": true
            },
            {
              "key": "prefix",
              "type": "string",
              "required": true
            },
            {
              "key": "existing_vpc_crn",
              "type": "string",
              "hidden": true,
              "value_constraints": [
                {
                  "type": "regex",
                  "description": "Must be a valid VPC CRN",
                  "value": "^crn:(.*:){3}is:(.*:){2}:vpc:.*$"
                }
              ]
            },
            {
              "key": "enable_encryption",
              "type": "boolean",
              "virtual": true,
              "default_value": false,
              "description": "Enable KMS encryption for cluster"
            }
          ],
          "dependencies": [
            {
              "name": "deploy-arch-ibm-vpc",
              "description": "Configure VPC and subnets for the cluster",
              "id": "vpc-da-id-global",
              "version": "v1.0.0",
              "flavors": ["standard"],
              "catalog_id": "catalog-id",
              "optional": false,
              "on_by_default": true,
              "input_mapping": [
                {
                  "dependency_input": "prefix",
                  "version_input": "prefix",
                  "reference_version": true
                },
                {
                  "dependency_output": "vpc_crn",
                  "version_input": "existing_vpc_crn"
                }
              ]
            },
            {
              "name": "deploy-arch-ibm-kms",
              "description": "Integrate Key Protect for encryption",
              "id": "kms-da-id-global",
              "version": "v1.0.0",
              "flavors": ["standard"],
              "catalog_id": "catalog-id",
              "optional": true,
              "on_by_default": true,
              "input_mapping": [
                {
                  "version_input": "enable_encryption",
                  "value": true
                }
              ]
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

### Dependency Issues
- Verify dependency IDs and catalog IDs are correct
- Check that dependency versions exist
- Ensure input mappings reference correct parameter names
- Test dependencies individually before combining

## Best Practices

1. **Start Simple**: Begin with standard input types and add custom widgets only where needed
2. **User Experience**: Use custom widgets for complex selections (regions, resource groups, VPCs)
3. **Validation**: Leverage custom widgets and constraints for built-in validation
4. **Documentation**: Provide clear descriptions for all parameters, regardless of widget type
5. **Testing**: Test both with and without custom widgets to ensure fallback behavior works
6. **Grouping**: Use `grouping` in `custom_config` to organize related parameters
7. **Multiple Flavors**: Design flavors for different user personas and use cases
8. **Security First**: Always use `password` type for sensitive data
9. **Defaults Matter**: Provide sensible defaults to improve user experience
10. **Keep It Updated**: Regularly update SHA hashes and version numbers
11. **Dependencies**: Use for composability and reusability
12. **Features**: Highlight value proposition at product and flavor levels
13. **IAM Notes**: Always explain why permissions are needed
14. **Hidden Parameters**: Use for advanced settings controlled by dependencies
15. **Virtual Parameters**: Use for UI-only controls that affect dependencies

## Complete Real-World Example

See the [terraform-ibm-base-ocp-vpc](https://github.com/terraform-ibm-modules/terraform-ibm-base-ocp-vpc/blob/main/ibm_catalog.json) repository for a production example featuring:
- Two flavors (QuickStart and Fully Configurable)
- Product-level features array
- 15+ configuration parameters per flavor
- Multiple IAM permission sets with notes
- Architecture diagrams with descriptions
- 8 optional dependencies (VPC, KMS, COS, Cloud Logs, Monitoring, Activity Tracker, Secrets Manager, Workload Protection)
- Hidden and virtual parameters
- Value constraints and validation
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
- [IBM Cloud IAM Roles](https://cloud.ibm.com/docs/account?topic=account-userroles)