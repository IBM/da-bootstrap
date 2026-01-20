# Guide: Running Existing Terraform Automation

## Overview

This guide helps you determine the best approach for running your existing Terraform automation. The key decisions involve where to run the automation (locally vs. cloud) and what type of automation you have (standard Terraform vs. Deployable Architecture).

## Decision Flow

![Terraform Automation Decision Flow](./terraform-automation-decision-flow.svg)

## Key Decisions

### 1. Where to Run the Automation

#### Local Execution
- Uses native Terraform CLI commands
- State file stored locally on your machine
- Best for rapid development and testing
- Ideal when making frequent changes, fixing bugs, or validating syntax
- No need to update remote repositories between changes
- Automation remains private to your local environment

#### Cloud Execution (IBM Cloud Schematics)
- Uses IBM Cloud Schematics service to run Terraform
- State file stored in the cloud
- Enables shared access to state across team members
- Requires storing Terraform files in a Git repository
- Changes require updating the repository before execution
- Better for production and team collaboration

### 2. Type of Automation

#### Standard Terraform
- Regular Terraform code without advanced features
- Can be run locally or on the cloud
- Can evolve into a Deployable Architecture later
- When running on cloud, two options:
  - **Direct Schematics execution**: Reference Git repository directly
  - **Private Catalog offering**: Formal versioned offering in IBM Cloud Private Catalog

#### Deployable Architecture (DA)
- Terraform with advanced IBM Cloud features
- Must be deployed on IBM Cloud
- Requires IBM Cloud Projects service
- Cannot be run locally due to advanced feature dependencies

### 3. Publishing and Sharing (Optional)

If you plan to share or publish your automation with other cloud users:
- Must onboard to IBM Cloud Private Catalog as an offering
- Can be decided at any point in the development lifecycle
- Applies to both Standard Terraform and Deployable Architectures

## Path Summaries

### Path 1: Local Development (Standard Terraform)
**When to use**: Rapid iteration, testing, debugging, syntax validation
**Steps**: Use Terraform CLI locally → State stored locally → Private to your machine

### Path 2: Cloud Execution - Direct Schematics (Standard Terraform)
**When to use**: Team collaboration, shared state, production deployments
**Steps**: Store in Git → Execute via Schematics → State stored in cloud

### Path 3: Cloud Execution - Private Catalog (Standard Terraform)
**When to use**: Formal versioning, sharing across organization, governance
**Steps**: Store in Git → Onboard to Private Catalog → Execute via Schematics → State stored in cloud

### Path 4: Deployable Architecture
**When to use**: Advanced IBM Cloud features, enterprise deployments, complex architectures
**Steps**: Store in Git → Onboard to Private Catalog → Deploy via Projects service → State stored in cloud

## Getting Started - Interactive Decision Process

Follow these questions in order to determine the right path for your automation:

### Which Terraform project do you want to run?

**Note: Skip this question if you only have one Terraform project in your workspace.**

If you have multiple Terraform projects in your workspace, first identify which one you want to work with:

1. List all Terraform projects in your workspace
2. Review each project's purpose and contents
3. Select the specific project directory you want to run

**→ Once you've identified your project (or if you only have one), proceed to the next question**

---

### What type of automation do you have?

**How to detect:**
- Check if `ibm_catalog.json` file exists in the project root
- If it exists, open it and look for the `product_kind` property
- If `product_kind` has value `"solution"`, it's a **Deployable Architecture**
- All other values (or if file doesn't exist) indicate **Standard Terraform**

**Option A: Standard Terraform**
- Regular `.tf` files with standard Terraform resources
- Either no `ibm_catalog.json` file, OR `ibm_catalog.json` exists but `product_kind` is NOT `"solution"`
- Can be run locally or on the cloud
- May use IBM Cloud provider but no DA-specific configurations

**Option B: Deployable Architecture (DA)**
- Contains `ibm_catalog.json` file with `"product_kind": "solution"`
- Uses IBM Cloud Projects service features
- Has DA-specific metadata and configurations
- Must be deployed on IBM Cloud (cannot run locally)

**→ If Standard Terraform, proceed to next question**
**→ If Deployable Architecture, skip to "For Deployable Architecture" section (must use cloud)**

---

### Where and how do you want to run your automation?

**Option A: Local Execution (Path 1)**
- Fast iteration and testing
- State stored on your machine
- No need to commit changes between runs
- Private to your environment
- **→ Follow Path 1 instructions below**

**Option B: Cloud - Direct Schematics Execution (Path 2)**
- Quick setup - reference Git repository directly in Schematics
- Shared state in the cloud
- No formal versioning or catalog
- Good for testing and internal team use
- Faster to get started with cloud execution
- **→ Follow Path 2 instructions below**

**Option C: Cloud - Private Catalog Offering (Path 3)**
- Formal versioned offering in IBM Cloud Private Catalog
- Shared state in the cloud via Schematics
- Better governance and sharing across organization
- Requires onboarding process
- More structured approach for production use
- **→ Follow Path 3 instructions below**

---

### For Deployable Architecture - Catalog Setup

Deployable Architectures must be deployed on IBM Cloud via Private Catalog.

**→ Follow Path 4 instructions below**

---

## Detailed Path Instructions

### Path 1: Local Development

For detailed instructions on running Terraform locally, see:
- **[Guide: Running Terraform Locally](./running-terraform-locally.md)**

**State Management**: State file (`terraform.tfstate`) stored locally in project directory

---

### Path 2: Direct Schematics Execution

For detailed instructions on running Terraform via IBM Cloud Schematics, see:
- **[Guide: Running Terraform with IBM Cloud Schematics](./running-terraform-with-schematics.md)**

**State Management**: State stored in IBM Cloud Schematics service

---

### Path 3: Private Catalog Offering

For detailed instructions on onboarding and deploying Terraform as a Private Catalog offering, see:
- **[Guide: Onboarding Terraform to IBM Cloud Private Catalog](./onboarding-terraform-to-private-catalog.md)**
- **[Guide: Deploying from IBM Cloud Private Catalog](./deploying-from-private-catalog.md)**

**State Management**: State stored in IBM Cloud Schematics service

---

### Path 4: Deployable Architecture

For detailed instructions on onboarding and deploying a Deployable Architecture, see:
- **[Guide: Onboarding Deployable Architecture to IBM Cloud Catalog](./onboarding-deployable-architecture.md)**
- **[Guide: Deploying Deployable Architecture via IBM Cloud Projects](./deploying-deployable-architecture-via-projects.md)**

**State Management**: State stored in IBM Cloud Projects service

---

## Notes

- Both local and cloud execution are valid starting points
- Standard Terraform can be enhanced to become a Deployable Architecture at any time
- Publishing/sharing decisions can be made later in the development lifecycle
- The choice of execution location can change as your automation matures
- **Always answer the decision questions before proceeding** to avoid assumptions
- You can switch paths as your requirements evolve