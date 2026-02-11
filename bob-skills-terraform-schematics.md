# Bob's Skills: Terraform & IBM Cloud Schematics

This document contains my learned skills for working with Terraform and IBM Cloud Schematics.

## Skill Categories

### 1. Terraform Detection
**Status**: ✅ Learned
**Description**: Ability to detect Terraform files in the workspace
**Key Capabilities**:
- Detect `.tf` files in workspace recursively
- Identify Terraform root modules
- Handle multiple root modules

**Detection Criteria**:
- Search for `*.tf` files recursively throughout the workspace
- Identify root modules: any directory containing `.tf` files (including subdirectories)
- Do NOT exclude directories like `modules/` or `examples/` - treat all directories with `.tf` files as potential root modules

**Behavior**:
- **Trigger**: Detect when user mentions "terraform" OR when `.tf` files are visible in workspace
- **Single root module**: Automatically proceed with that directory
- **Multiple root modules**: Ask user which directory to use
- **Report**: List all root module locations found

**Implementation**:
```bash
# Search for all .tf files recursively
find . -name "*.tf" -type f

# Group by directory to identify root modules
find . -name "*.tf" -type f | sed 's|/[^/]*$||' | sort -u
```

**Example Scenarios**:

Scenario 1 - Single root:
```
/main.tf
/variables.tf
```
→ Action: Automatically use `/` as root module

Scenario 2 - Multiple roots:
```
/main.tf
/modules/vpc/main.tf
/examples/simple/main.tf
```
→ Action: Ask user to choose from: `/`, `/modules/vpc`, `/examples/simple`

Scenario 3 - Nested structure:
```
/project-a/main.tf
/project-b/main.tf
```
→ Action: Ask user to choose from: `/project-a`, `/project-b`

### 2. Git Repository Detection
**Status**: ✅ Learned
**Description**: Ability to check if Terraform is in a git repository
**Key Capabilities**:
- Check for `.git` directory at workspace root
- Verify git repository is valid
- Check if remote is configured
- Get remote URL information

**Detection Criteria**:
- Always check workspace root directory for `.git` (not subdirectories)
- Verify it's a valid git repository (can run `git status`)
- Check if at least one remote is configured
- Get the remote URL (typically `origin`)

**Checks to Perform**:
1. Check if `.git` directory exists at workspace root
2. Verify git repository is valid: `git status` runs without error
3. Check for remote: `git remote -v`
4. Get remote URL: `git remote get-url origin` (or first available remote)
5. Get current branch: `git branch --show-current`
6. Check git status: `git status --porcelain` (for uncommitted changes)

**Reporting** (Simple format):
- **Scenario A** - Git with remote: "Git repository found with remote: https://github.com/user/repo.git"
- **Scenario B** - Git without remote: "Git repository found but no remote configured"
- **Scenario C** - No git: "No git repository found"

**Implementation**:
```bash
# Check if .git exists at workspace root
test -d .git && echo "Git repo exists" || echo "No git repo"

# Verify valid git repo
git status &>/dev/null && echo "Valid git repo" || echo "Invalid git repo"

# Check for remote
git remote -v | grep -q . && echo "Remote configured" || echo "No remote"

# Get remote URL (origin or first available)
git remote get-url origin 2>/dev/null || git remote -v | head -n1 | awk '{print $2}'

# Get current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain
```

**Status Classification**:
- **Ready for Schematics**: Git repo exists with remote configured
- **Needs Setup**: Git repo exists but no remote (requires Skill 3 to add remote)
- **Not in Git**: No git repository (requires Skill 3 to initialize)

### 3. Git Repository Creation
**Status**: To be learned
**Description**: Ability to create a git repository for Terraform code
**Key Capabilities**:
- Initialize git repository
- Add Terraform files to git
- Configure git remote
- Push to remote repository

### 4. IBM Cloud Schematics Workspace Detection
**Status**: ✅ Learned
**Description**: Ability to list and identify Schematics workspaces
**Key Capabilities**:
- List all Schematics workspaces in the account
- Get detailed information about specific workspaces
- Filter workspaces by region
- Parse workspace metadata (name, ID, status, git repo, etc.)

**Detection Criteria**:
- Check if user is logged into IBM Cloud CLI
- List all workspaces using JSON output for parsing
- Extract key workspace information: ID, name, status, git repository URL, branch, folder path
- Support filtering by region if needed

**Checks to Perform**:
1. Verify IBM Cloud CLI authentication: `ibmcloud target` (check if logged in)
2. List all workspaces: `ibmcloud schematics workspace list --output JSON --limit 200`
3. Get specific workspace details: `ibmcloud schematics workspace get --id WORKSPACE_ID --output JSON`
4. Parse JSON output to extract workspace metadata

**Key Workspace Fields**:
- `id`: Workspace unique identifier
- `name`: Workspace name
- `status`: Workspace status (ACTIVE, INACTIVE, etc.)
- `template_repo`: Git repository URL
- `template_data[].folder`: Terraform folder path in repo
- `template_data[].type`: Terraform version
- `location`: Region where workspace is deployed
- `resource_group`: Resource group name

**Reporting** (Simple format):
- **Scenario A** - Workspaces found: "Found X Schematics workspace(s): [list names with IDs]"
- **Scenario B** - No workspaces: "No Schematics workspaces found in this account"
- **Scenario C** - Not authenticated: "Not logged into IBM Cloud. Run `ibmcloud login` first"

**Implementation**:
```bash
# Check if logged in
ibmcloud target &>/dev/null && echo "Logged in" || echo "Not logged in"

# List all workspaces with JSON output
ibmcloud schematics workspace list --output JSON --limit 200

# Get specific workspace details
ibmcloud schematics workspace get --id WORKSPACE_ID --output JSON

# List workspaces in specific region
ibmcloud schematics workspace list --region us-south --output JSON

# Parse workspace list to extract names and IDs (using jq if available)
ibmcloud schematics workspace list --output JSON | jq -r '.workspaces[] | "\(.name) (\(.id))"'
```

**Status Classification**:
- **Authenticated & Has Workspaces**: Ready to check workspace-to-code connections
- **Authenticated & No Workspaces**: Ready to create new workspace (Skill 6)
- **Not Authenticated**: User needs to run `ibmcloud login`

**Error Handling**:
- If not logged in: Inform user to authenticate with `ibmcloud login`
- If API errors occur: Report the error and suggest checking IBM Cloud status
- If no workspaces found: This is valid - user may not have created any yet

### 5. Schematics-Terraform Connection Check
**Status**: ✅ Learned
**Description**: Ability to verify if a Schematics workspace is connected to local Terraform
**Key Capabilities**:
- Compare workspace git repository URL with local git remote URL
- Match workspace branch with local git branch
- Verify workspace folder path matches local Terraform root module
- Identify connected vs. unconnected workspaces
- Support multiple workspace scenarios

**Connection Criteria**:
A workspace is considered "connected" to local Terraform when ALL of the following match:
1. Workspace `template_repo.url` matches local git remote URL
2. Workspace `template_repo.branch` matches local git branch (or user confirms branch alignment)
3. Workspace `template_data[0].folder` matches the Terraform root module path relative to repo root

**Checks to Perform**:
1. Get local git remote URL: `git remote get-url origin`
2. Get local git branch: `git branch --show-current`
3. Determine Terraform root module path relative to git repo root
4. List all Schematics workspaces: `ibmcloud schematics workspace list --output JSON`
5. For each workspace, compare:
   - `template_repo.url` with local remote URL (normalize URLs for comparison)
   - `template_repo.branch` with local branch
   - `template_data[0].folder` with Terraform root path

**URL Normalization**:
- Remove `.git` suffix if present
- Handle both HTTPS and SSH URLs (convert to common format)
- Examples:
  - `https://github.com/user/repo.git` → `https://github.com/user/repo`
  - `git@github.com:user/repo.git` → `https://github.com/user/repo`

**Reporting** (Simple format):
- **Scenario A** - Connected workspace found: "Found connected workspace: [name] (ID: [id])"
- **Scenario B** - Multiple matches: "Found X workspaces connected to this repository: [list names]"
- **Scenario C** - No connection: "No Schematics workspace connected to this Terraform code"
- **Scenario D** - Partial match: "Found workspace [name] with same repo but different branch/folder"

**Implementation**:
```bash
# Get local git information
LOCAL_REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/\.git$//' | sed 's|git@github.com:|https://github.com/|')
LOCAL_BRANCH=$(git branch --show-current)
REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_DIR=$(pwd)
TF_FOLDER=$(realpath --relative-to="$REPO_ROOT" "$CURRENT_DIR")

# List workspaces and compare
ibmcloud schematics workspace list --output JSON | python3 -c "
import sys, json
data = json.load(sys.stdin)
local_remote = '$LOCAL_REMOTE'
local_branch = '$LOCAL_BRANCH'
tf_folder = '$TF_FOLDER'

for ws in data['workspaces']:
    ws_url = ws['template_repo']['url'].rstrip('.git')
    ws_branch = ws['template_repo']['branch']
    ws_folder = ws['template_data'][0]['folder']
    
    if ws_url == local_remote:
        if ws_branch == local_branch and ws_folder == tf_folder:
            print(f\"CONNECTED: {ws['name']} (ID: {ws['id']})\")
        else:
            print(f\"PARTIAL: {ws['name']} - branch:{ws_branch} folder:{ws_folder}\")
"
```

**Status Classification**:
- **Fully Connected**: Workspace matches repo, branch, and folder
- **Partially Connected**: Workspace matches repo but different branch or folder
- **Not Connected**: No workspace matches the local git repository
- **No Git**: Local Terraform not in git repository (requires Skill 2 & 3)

**Edge Cases**:
- Multiple workspaces connected to same repo/branch but different folders
- Workspace connected to fork vs. original repository
- Workspace branch deleted locally but still exists remotely
- Terraform root module in subdirectory vs. repo root

### 6. Schematics Workspace Creation
**Status**: ✅ Learned
**Description**: Ability to create and configure IBM Cloud Schematics workspace using CLI
**Key Capabilities**:
- Create new Schematics workspace from JSON configuration
- Link workspace to git repository
- Configure workspace settings (region, resource group, Terraform version)
- Set workspace name, description, and tags
- Configure template data and folder paths
- Import existing Terraform state (optional)

**Creation Method**:
Workspaces are created using `ibmcloud schematics workspace new` command with a JSON configuration file.

**Required JSON Configuration Fields**:
- `name`: Workspace name (must be unique in account)
- `type`: Array of Terraform version(s) - e.g., `["terraform_v1.12"]`
- `location`: IBM Cloud region - e.g., `"us-south"`, `"us-east"`, `"eu-de"`, `"eu-gb"`
- `resource_group`: Resource group name (default: "default")
- `template_repo`: Git repository configuration
  - `url`: Git repository URL (HTTPS or SSH)
  - `branch`: Git branch name (default: "main" or "master")
- `template_data`: Array of template configurations (usually one element)
  - `folder`: Path to Terraform code within repository (use "." for root)
  - `type`: Terraform version - e.g., `"terraform_v1.12"`

**Optional JSON Configuration Fields**:
- `description`: Workspace description
- `tags`: Array of tags for organization
- `template_repo.release`: Specific git release/tag to use
- `template_repo.repo_sha_value`: Specific commit SHA to use

**Workspace Creation Workflow**:
1. Gather required information from local Terraform and git
2. Create JSON configuration file
3. Execute `ibmcloud schematics workspace new --file <config.json>`
4. Verify workspace creation and capture workspace ID
5. Optionally import existing Terraform state

**Checks to Perform Before Creation**:
1. Verify IBM Cloud CLI authentication: `ibmcloud target`
2. Verify git repository exists and has remote configured
3. Verify Terraform code is committed and pushed to remote
4. Check if workspace with same name already exists
5. Validate resource group exists (if not using default)
6. Ensure git repository is accessible (public or token provided for private)

**Implementation**:
```bash
# Create workspace configuration JSON
cat > workspace-config.json << EOF
{
  "name": "my-terraform-workspace",
  "type": ["terraform_v1.12"],
  "description": "Workspace for my Terraform configuration",
  "location": "us-south",
  "resource_group": "default",
  "tags": ["terraform", "schematics"],
  "template_repo": {
    "url": "https://github.com/user/repo",
    "branch": "main"
  },
  "template_data": [{
    "folder": ".",
    "type": "terraform_v1.12"
  }]
}
EOF

# Create workspace
ibmcloud schematics workspace new --file workspace-config.json --output JSON

# Create workspace with GitHub token for private repo
ibmcloud schematics workspace new --file workspace-config.json --github-token $GITHUB_TOKEN --output JSON

# Create workspace and import existing state
ibmcloud schematics workspace new --file workspace-config.json --state ./terraform.tfstate --output JSON
```

**Automated Workspace Creation from Local Terraform**:
```bash
# Gather local information
LOCAL_REMOTE=$(git remote get-url origin | sed 's/\.git$//' | sed 's|git@github.com:|https://github.com/|')
LOCAL_BRANCH=$(git branch --show-current)
REPO_ROOT=$(git rev-parse --show-toplevel)
CURRENT_DIR=$(pwd)
TF_FOLDER=$(realpath --relative-to="$REPO_ROOT" "$CURRENT_DIR")
WORKSPACE_NAME=$(basename "$CURRENT_DIR")

# Create configuration
cat > workspace-config.json << EOF
{
  "name": "$WORKSPACE_NAME",
  "type": ["terraform_v1.12"],
  "description": "Auto-generated workspace for $WORKSPACE_NAME",
  "location": "us-south",
  "resource_group": "default",
  "template_repo": {
    "url": "$LOCAL_REMOTE",
    "branch": "$LOCAL_BRANCH"
  },
  "template_data": [{
    "folder": "$TF_FOLDER",
    "type": "terraform_v1.12"
  }]
}
EOF

# Create workspace
ibmcloud schematics workspace new --file workspace-config.json --output JSON
```

**Reporting** (Simple format):
- **Scenario A** - Success: "Workspace created: [name] (ID: [id])"
- **Scenario B** - Already exists: "Workspace with name [name] already exists"
- **Scenario C** - Git not accessible: "Cannot access git repository: [url]"
- **Scenario D** - Not authenticated: "Not logged into IBM Cloud. Run `ibmcloud login` first"
- **Scenario E** - Invalid config: "Invalid workspace configuration: [error details]"

**Status Classification**:
- **Created Successfully**: Workspace created and ready for use
- **Already Exists**: Workspace with same name exists (use Skill 5 to check connection)
- **Git Access Error**: Repository not accessible (check URL, branch, or token)
- **Authentication Required**: User needs to login to IBM Cloud
- **Configuration Error**: Invalid JSON or missing required fields

**Error Handling**:
- If workspace name already exists: Suggest using different name or checking existing workspace
- If git repository not accessible: Verify URL, branch exists, and repository is public or token provided
- If resource group not found: List available resource groups or use "default"
- If Terraform version not supported: List supported versions
- If not authenticated: Prompt user to run `ibmcloud login`

**Post-Creation Actions**:
1. Capture and store workspace ID from output
2. Verify workspace status: `ibmcloud schematics workspace get --id <workspace-id>`
3. Optionally run `terraform plan`: `ibmcloud schematics plan --id <workspace-id>`
4. Update local tracking of workspace connection

**Terraform Version Mapping**:
- `terraform_v1.12` → Terraform 1.12.x
- `terraform_v1.9` → Terraform 1.9.x
- `terraform_v1.5` → Terraform 1.5.x
- `terraform_v1.4` → Terraform 1.4.x
- `terraform_v1.3` → Terraform 1.3.x
- `terraform_v1.1` → Terraform 1.1.x
- `terraform_v1.0` → Terraform 1.0.x

**Best Practices**:
- Use descriptive workspace names that indicate purpose
- Always specify the Terraform version that matches your code
- Commit and push code before creating workspace
- Use tags for organization and cost tracking
- Store workspace ID for future reference
- Verify workspace creation with `workspace get` command

### 7. Terraform Test Data Generation
**Status**: ✅ Learned (Enhanced)
**Description**: Ability to generate test input data (tfvars JSON) for Terraform configurations by analyzing variable definitions. Now supports complex nested types and multi-line object schemas. **Generates only a single tfvars.json file as output.**
**Key Capabilities**:
- Parse `variables.tf` to extract variable definitions including multi-line type definitions
- Generate appropriate test values based on variable types
- Handle complex types (objects, lists, maps) with proper schema parsing
- Support nested types (objects within objects, lists within objects, etc.)
- Parse object schemas dynamically to extract field names and types
- Support sensitive variables with placeholder values
- Create a single valid JSON output file (tfvars.json format)
- Respect default values when present
- Work with any Terraform template regardless of variable schema complexity
- **Output**: Single tfvars.json file only - no additional files created

**Variable Type Handling**:
- `string`: Generate descriptive test string (e.g., "test-value-for-{var_name}")
- `number`: Generate appropriate numeric value (integers or floats based on context)
- `bool`: Generate `false` by default
- `list(string)`: Generate array with 3 sample string elements
- `list(number)`: Generate array with 3 sample numeric elements
- `list(object({...}))`: Parse object schema and generate array with 2 objects matching the schema
- `map(string)`: Generate object with 2 key-value string pairs
- `map(number)`: Generate object with 3 key-value numeric pairs
- `map(object({...}))`: Parse object schema and generate map with 2 entries, each containing an object
- `object({...})`: Parse object schema dynamically and generate object with appropriate values for each field
  - Handles multi-line object definitions
  - Supports nested types within objects (lists, maps, other objects)
  - Extracts field names and types automatically
- `sensitive`: Generate placeholder value "REPLACE_WITH_ACTUAL_VALUE"

**Generation Rules**:
1. Skip variables that have default values (unless user requests all variables)
2. Generate realistic test data that matches the variable description
3. For lists, generate 2-3 elements to show structure
4. For objects, populate all required fields
5. Use descriptive values that indicate the variable purpose
6. Mark sensitive values clearly for replacement
7. Ensure generated JSON is valid and properly formatted

**Enhanced Implementation Features**:

1. **Multi-line Type Extraction**: Uses brace counting to extract complete type definitions spanning multiple lines
2. **Object Schema Parser**: `parse_object_schema()` function extracts field names and types from object definitions
3. **Dynamic Object Generation**: `generate_object_from_schema()` creates objects based on parsed schema
4. **Type Precedence**: Checks object types before list types to avoid false matches (objects may contain list fields)

**Key Implementation Details**:
```python
# Type extraction with brace counting for multi-line definitions
type_match = re.search(r'type\s*=\s*', var_block)
if type_match:
    start_pos = type_match.end()
    brace_count = 0
    in_type = False
    end_pos = start_pos
    
    for i in range(start_pos, len(var_block)):
        char = var_block[i]
        if char == '(':
            brace_count += 1
            in_type = True
        elif char == ')':
            brace_count -= 1
            if brace_count == 0 and in_type:
                end_pos = i + 1
                break
        elif char == '\n' and brace_count == 0:
            end_pos = i
            break
        end_pos = i + 1
    
    var_type = var_block[start_pos:end_pos].strip()

# Object schema parsing
def parse_object_schema(type_str):
    """Extract field names and types from object definition"""
    # Find object({ ... }) content
    # Parse field definitions: field_name = type
    # Return dict mapping field names to types

# Dynamic object generation
def generate_object_from_schema(schema, index=None):
    """Generate test object based on parsed schema"""
    obj = {}
    for field_name, field_type in schema.items():
        if field_type == 'string':
            obj[field_name] = "value{index}" if index else "test-object-value"
        elif field_type == 'number':
            obj[field_name] = index if index else 42
        elif field_type == 'bool':
            obj[field_name] = False
        # Handle nested types...
    return obj
```

**Usage Examples**:

Example 1 - Generate test data for variables without defaults:
```bash
python3 generate_test_data.py variables.tf test-values.tfvars.json
```

Example 2 - Generate test data including variables with defaults:
```bash
python3 generate_test_data.py variables.tf test-values.tfvars.json --include-defaults
```

Example 3 - Generate from specific Terraform directory:
```bash
cd terraform-project
python3 ../generate_test_data.py ./variables.tf ./test-input.tfvars.json
```

**Reporting** (Simple format):
- **Scenario A** - Success: "Generated test-values.tfvars.json with X variables"
- **Scenario B** - No variables: "No variables found in variables.tf"
- **Scenario C** - File not found: "variables.tf not found in current directory"
- **Scenario D** - Parse error: "Error parsing variables.tf: [error details]"

**Validation**:
After generation, validate the JSON file:
```bash
# Validate JSON syntax
python3 -m json.tool test-values.tfvars.json > /dev/null && echo "Valid JSON" || echo "Invalid JSON"

# Test with Terraform
terraform validate -var-file=test-values.tfvars.json
```

**Status Classification**:
- **Generated Successfully**: JSON file created with valid test data
- **Partial Generation**: Some variables could not be parsed (complex types)
- **Validation Failed**: Generated JSON is invalid or incompatible with Terraform
- **No Variables Found**: variables.tf exists but contains no variable definitions

**Error Handling**:
- If variables.tf not found: Check current directory and suggest correct path
- If complex types cannot be parsed: Generate placeholder and warn user
- If JSON generation fails: Report parsing errors with line numbers
- If validation fails: Show Terraform error and suggest corrections

**Best Practices**:
- Always review generated values before using in production
- Replace sensitive placeholders with actual values
- Adjust generated values to match your specific requirements
- Use descriptive variable names to get better generated values
- Test generated JSON with `terraform validate` before use
- Store generated test files in version control for CI/CD
- The script works with any Terraform template - no hardcoded schemas
- Complex nested types are automatically parsed and handled

**Integration with Other Skills**:
- Use with Skill 1 (Terraform Detection) to find variables.tf
- Use with Skill 6 (Workspace Creation) to provide initial variable values
- Combine with validation workflows to test Terraform configurations

### 8. Schematics Workspace Variable Update
**Status**: ✅ Learned
**Description**: Ability to update IBM Cloud Schematics workspace variables using test data generated from Terraform variable definitions
**Key Capabilities**:
- Update workspace variables using IBM Cloud CLI
- Load variable values from JSON files (tfvars.json)
- Support both individual variable updates and bulk updates
- Handle sensitive variables appropriately
- Validate variable updates
- Integration with test data generation (Skill 7)

**Update Methods**:
Workspace variables are updated using the dedicated command:
- `ibmcloud schematics workspace update-variables` - Update workspace variables directly
- Supports JSON file input with variable definitions
- Can update multiple variables in a single operation

**Required Information**:
- Workspace ID (from Skill 4 or 5)
- Template ID (found in workspace JSON at `template_data[0].id`)
- Variable values in JSON format (from Skill 7 or user-provided)
- Variable metadata (name, type, secure flag)

**Update Workflow**:
1. Get workspace details to extract template ID: `ibmcloud schematics workspace get --id <workspace-id> --output JSON`
2. Extract template ID from workspace JSON: `template_data[0].id`
3. Load test data from JSON file (e.g., generated-test-values.tfvars.json)
4. Convert test data to Schematics variable format (variablestore array)
5. Update workspace variables: `ibmcloud schematics workspace update-variables --id <workspace-id> --template <template-id> --file <variables.json>`
6. Verify update success and report results

**Checks to Perform Before Update**:
1. Verify IBM Cloud CLI authentication: `ibmcloud target`
2. Verify workspace exists and is accessible
3. Validate JSON file format and content
4. Check for sensitive variables that need manual replacement
5. Confirm workspace is not currently running a plan/apply operation

**Implementation**:
```bash
# Set workspace ID
WORKSPACE_ID="your-workspace-id"
TEST_VALUES_FILE="generated-test-values.tfvars.json"

# Get template ID from workspace
TEMPLATE_ID=$(ibmcloud schematics workspace get --id $WORKSPACE_ID --output JSON | \
  python3 -c "import json, sys; data=json.load(sys.stdin); print(data['template_data'][0]['id'])")

echo "Using template ID: $TEMPLATE_ID"

# Convert test data to Schematics variable format
# CRITICAL: Must provide full type schemas and HCL-formatted values
python3 << 'EOF'
import json
import re

# Load test values
with open('generated-test-values.tfvars.json', 'r') as f:
    test_values = json.load(f)

# Read variables.tf to extract full type definitions
with open('variables.tf', 'r') as f:
    tf_content = f.read()

# Map variable names to their full Terraform type definitions
# Must include complete schema with newlines for complex types
def get_terraform_type(var_name, content):
    """Extract full type definition from variables.tf"""
    # Parse the variable block to get the complete type
    # For complex types like object, include full schema with newlines
    # Example: 'object({\n      key2 = string\n    })'
    # This must match the exact format in variables.tf
    pass  # Implementation depends on your variables.tf structure

def to_hcl_value(value):
    """Convert Python value to HCL format with proper quoting"""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return value  # Plain string, no quotes
    elif isinstance(value, list):
        if value and isinstance(value[0], str):
            # List of strings - quote each item (NO backslash escapes)
            items = [f'"{item}"' for item in value]
            return '[' + ', '.join(items) + ']'
        elif value and isinstance(value[0], dict):
            # List of objects
            items = [to_hcl_value(item) for item in value]
            return '[' + ', '.join(items) + ']'
        else:
            # List of numbers/bools
            items = [to_hcl_value(item) for item in value]
            return '[' + ', '.join(items) + ']'
    elif isinstance(value, dict):
        # Object - quote string values (NO backslash escapes)
        items = [f'{k} = "{v}"' if isinstance(v, str) else f'{k} = {to_hcl_value(v)}'
                 for k, v in value.items()]
        return '{' + ', '.join(items) + '}'
    else:
        return str(value)

# Convert to variablestore format
variablestore = []
for var_name, var_value in test_values.items():
    is_sensitive = (
        isinstance(var_value, str) and
        var_value == "REPLACE_WITH_ACTUAL_VALUE"
    )
    
    # Get full type definition (must include complete schema)
    tf_type = get_terraform_type(var_name, tf_content)
    
    # Convert to HCL format
    if is_sensitive:
        hcl_value = var_value
    else:
        hcl_value = to_hcl_value(var_value)
    
    variablestore.append({
        'name': var_name,
        'value': hcl_value,
        'type': tf_type,  # Full type schema, not just 'string'
        'secure': is_sensitive,
        'description': ''
    })

# Create variables JSON file
variables_json = {'variablestore': variablestore}
with open('workspace-variables.json', 'w') as f:
    json.dump(variables_json, f, indent=2)

print(f"Created workspace-variables.json with {len(variablestore)} variables")

EOF

# Update workspace variables using the dedicated command with template ID
ibmcloud schematics workspace update-variables \
  --id $WORKSPACE_ID \
  --template $TEMPLATE_ID \
  --file workspace-variables.json \
  --output JSON

# Verify update
ibmcloud schematics workspace get --id $WORKSPACE_ID --output JSON | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'template_data' in data and len(data['template_data']) > 0:
    vars = data['template_data'][0].get('variablestore', [])
    print(f'Workspace now has {len(vars)} variables')
    for var in vars:
        secure = ' (secure)' if var.get('secure', False) else ''
        print(f\"  - {var['name']}: {var.get('value', 'N/A')[:50]}...{secure}\")
"
```

**Update Individual Variable**:
```bash
# Update a single variable
WORKSPACE_ID="your-workspace-id"
VAR_NAME="testString"
VAR_VALUE="test-value-for-testString"

# Get template ID from workspace
TEMPLATE_ID=$(ibmcloud schematics workspace get --id $WORKSPACE_ID --output JSON | \
  python3 -c "import json, sys; data=json.load(sys.stdin); print(data['template_data'][0]['id'])")

# Create variable JSON
cat > single-var.json << EOF
{
  "variablestore": [
    {
      "name": "$VAR_NAME",
      "value": "$VAR_VALUE",
      "type": "string",
      "secure": false
    }
  ]
}
EOF

# Update workspace variables with template ID
ibmcloud schematics workspace update-variables \
  --id $WORKSPACE_ID \
  --template $TEMPLATE_ID \
  --file single-var.json
```

**Integration with Skill 7 (Test Data Generation)**:
```bash
# Complete workflow: Generate test data and update workspace
cd terraform-variables-sample

# Step 1: Generate test data
python3 generate_test_data.py variables.tf generated-test-values.tfvars.json

# Step 2: Get workspace ID and template ID
WORKSPACE_ID=$(ibmcloud schematics workspace list --output JSON | \
  python3 -c "import json, sys; data=json.load(sys.stdin); \
  print([w['id'] for w in data['workspaces'] if 'terraform-variables-sample' in w['name']][0])")

TEMPLATE_ID=$(ibmcloud schematics workspace get --id $WORKSPACE_ID --output JSON | \
  python3 -c "import json, sys; data=json.load(sys.stdin); print(data['template_data'][0]['id'])")

echo "Workspace ID: $WORKSPACE_ID"
echo "Template ID: $TEMPLATE_ID"

# Step 3: Convert test data to Schematics variable format and update
python3 << 'EOF'
import json
import subprocess
import sys

# Load test values
with open('generated-test-values.tfvars.json', 'r') as f:
    test_values = json.load(f)

# Convert to variablestore format with full type schemas and HCL values
variablestore = []

# Define full type schemas for each variable (must match variables.tf)
var_types = {
    'testString': 'string',
    'testNumber': 'number',
    'testBool': 'bool',
    'testList': 'list(string)',
    'testObject': 'object({\n      key2 = string\n    })',
    'testListObject': 'list(object({\n      key2 = string\n    }))',
    'testMap': 'map(string)',
    # Add all your variables here with full type schemas
}

def to_hcl_value(value):
    """Convert to HCL format - NO backslash escapes"""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    elif isinstance(value, (int, float)):
        return str(value)
    elif isinstance(value, str):
        return value
    elif isinstance(value, list):
        if value and isinstance(value[0], str):
            items = [f'"{item}"' for item in value]  # Regular quotes
            return '[' + ', '.join(items) + ']'
        elif value and isinstance(value[0], dict):
            items = [to_hcl_value(item) for item in value]
            return '[' + ', '.join(items) + ']'
        else:
            items = [to_hcl_value(item) for item in value]
            return '[' + ', '.join(items) + ']'
    elif isinstance(value, dict):
        items = [f'{k} = "{v}"' if isinstance(v, str) else f'{k} = {to_hcl_value(v)}'
                 for k, v in value.items()]
        return '{' + ', '.join(items) + '}'
    return str(value)

for var_name, var_value in test_values.items():
    is_sensitive = (
        isinstance(var_value, str) and
        var_value == "REPLACE_WITH_ACTUAL_VALUE"
    )
    
    tf_type = var_types.get(var_name, 'string')
    hcl_value = var_value if is_sensitive else to_hcl_value(var_value)
    
    variablestore.append({
        'name': var_name,
        'value': hcl_value,  # HCL-formatted string
        'type': tf_type,     # Full type schema
        'secure': is_sensitive,
        'description': ''
    })

# Create variables JSON
variables_json = {'variablestore': variablestore}
with open('workspace-variables.json', 'w') as f:
    json.dump(variables_json, f, indent=2)

print(f"Converted {len(variablestore)} variables with full type schemas")

EOF

# Step 4: Update workspace variables with template ID
ibmcloud schematics workspace update-variables \
  --id $WORKSPACE_ID \
  --template $TEMPLATE_ID \
  --file workspace-variables.json \
  --output JSON

echo "Successfully updated workspace with test data"

# Step 5: Verify update
ibmcloud schematics workspace get --id $WORKSPACE_ID --output JSON | python3 -c "
import json, sys
data = json.load(sys.stdin)
if 'template_data' in data and len(data['template_data']) > 0:
    vars = data['template_data'][0].get('variablestore', [])
    print(f'Workspace now has {len(vars)} variables')
"
```

**Reporting** (Simple format):
- **Scenario A** - Success: "Updated workspace [name] with X variables from [file]"
- **Scenario B** - Partial update: "Updated X of Y variables (Z failed)"
- **Scenario C** - Workspace not found: "Workspace [id] not found"
- **Scenario D** - Not authenticated: "Not logged into IBM Cloud. Run `ibmcloud login` first"
- **Scenario E** - Invalid JSON: "Invalid JSON file: [error details]"
- **Scenario F** - Sensitive values: "Warning: X sensitive variables need manual replacement"

**Status Classification**:
- **Updated Successfully**: All variables updated in workspace
- **Partially Updated**: Some variables updated, others failed
- **Update Failed**: Workspace update command failed
- **Validation Required**: Sensitive placeholders detected, manual review needed
- **Authentication Required**: User needs to login to IBM Cloud

**Error Handling**:
- If workspace not found: Verify workspace ID and list available workspaces
- If not authenticated: Prompt user to run `ibmcloud login`
- If workspace is locked (plan/apply running): Wait or ask user to cancel operation
- If JSON parsing fails: Report specific parsing errors
- If sensitive placeholders found: Warn user to replace before applying
- If variable type mismatch: Report incompatible types and suggest corrections

**Post-Update Actions**:
1. Verify variables were updated: `ibmcloud schematics workspace get --id <workspace-id>`
2. Check for sensitive placeholders that need replacement
3. Optionally run plan to validate: `ibmcloud schematics plan --id <workspace-id>`
4. Report summary of updated variables

**Variable Type Handling for Schematics**:

**CRITICAL FORMAT REQUIREMENTS**:
1. **Type Field**: Must include FULL type schema with newlines for complex types
   - Simple: `"string"`, `"number"`, `"bool"`
   - List: `"list(string)"`, `"list(number)"`
   - Object: `"object({\n      key2 = string\n    })"` (with actual newlines)
   - List of Object: `"list(object({\n      key2 = string\n    }))"` (with actual newlines)
   - Map: `"map(string)"`

2. **Value Field**: Must be HCL-formatted string (NOT JSON-encoded, NO backslash escapes)
   - String: `"test-value"` (plain string, Schematics adds quotes)
   - Number: `"42"` or `"3.14"` (as string)
   - Bool: `"false"` or `"true"` (as string)
   - List of strings: `["item1", "item2", "item3"]` (with regular quotes, NO backslashes)
   - List of numbers: `[1, 2, 3]` (as HCL string)
   - Object: `{key2 = "test-value"}` (with regular quotes, NO backslashes)
   - List of objects: `[{key2 = "value1"}, {key2 = "value2"}]` (with regular quotes, NO backslashes)
   - Map: `{key1 = "value1", key2 = "value2"}` (with regular quotes, NO backslashes)

**WRONG vs RIGHT Examples**:
- ❌ WRONG: `"value": "[\\\"item1\\\", \\\"item2\\\"]"` (backslash escapes cause Terraform parse errors)
- ✅ RIGHT: `"value": "[\"item1\", \"item2\"]"` (regular quotes, Schematics handles serialization)
- ❌ WRONG: `"type": "object"` (incomplete type schema)
- ✅ RIGHT: `"type": "object({\n      key2 = string\n    })"` (full schema with newlines)

**Why This Format**:
- Schematics writes the `value` field directly to schematics.tfvars
- The `type` field tells Schematics how to serialize the value
- Full type schemas ensure proper validation and serialization
- Regular quotes (not backslash-escaped) produce valid HCL syntax

**Best Practices**:
- Always review generated test values before updating workspace
- Replace sensitive placeholders (REPLACE_WITH_ACTUAL_VALUE) before applying
- Verify workspace is not running operations before updating
- Keep backup of current workspace configuration
- Test with `terraform plan` after updating variables
- Use descriptive variable names for better traceability
- Document variable updates in version control

**Integration with Other Skills**:
- Use with Skill 4 (Workspace Detection) to find workspace ID
- Use with Skill 5 (Connection Check) to verify workspace-code connection
- Use with Skill 7 (Test Data Generation) to generate variable values
- Combine with Skill 6 (Workspace Creation) for new workspace setup

**Validation**:
After updating variables, validate the workspace:
```bash
# Get updated workspace configuration
ibmcloud schematics workspace get --id $WORKSPACE_ID --output JSON

# Run plan to validate variables
ibmcloud schematics plan --id $WORKSPACE_ID

# Check plan status
ibmcloud schematics logs --id $WORKSPACE_ID --act-id <activity-id>
```

### 9. User Interaction Workflows
**Status**: To be learned
**Description**: Ability to guide users through Terraform/Schematics workflows
**Key Capabilities**:
- Detect Terraform in workspace and offer Schematics setup
- Ask user preferences before taking actions
- Provide clear status updates and next steps

---

## Skill Details

### [To be populated as skills are taught]

---

## Configuration & Prerequisites

### IBM Cloud CLI
- Command: `ibmcloud`
- Required plugins: `schematics`
- Authentication: [To be defined]

### Git
- Command: `git`
- Supported remotes: [To be defined]

### Terraform
- File patterns: `*.tf`, `*.tfvars`
- State files: `terraform.tfstate`, `terraform.tfstate.backup`

---

## Workflow Examples

### Workflow 1: New Terraform Project → Schematics
1. Detect Terraform files in workspace
2. Check if in git repository
3. If not in git: Offer to create repository
4. Check for existing Schematics workspaces
5. If no matching workspace: Offer to create one
6. Link Schematics workspace to git repository

---

## Notes
- This is a living document that will be updated as new skills are taught
- Each skill should be testable and verifiable
- User preferences should always be respected (ask before acting)