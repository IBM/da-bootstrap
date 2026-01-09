# Automation on IBM Cloud Agent Instructions

## Overview

Automation implemented in Terraform is onboarded to the IBM Cloud.

### Before beginning

- use deployable architectures to contain, onboard, deploy and publish automations.
- use the Bob mode named DA Developer.
- When onboarding, complete the entire workflow without stopping: (1) analyze the automation structure and files, (2) create the complete ibm_catalog.json manifest file, (3) validate the manifest, and (4) prepare all necessary artifacts for catalog onboarding. Analysis is only the first step-always proceed through all phases.
- Ensure that you are using the latest versions of the guides located at https://github.com/IBM/da-bootstrap/tree/main/guides.
- Do not generate new or modify the existing terraform files.
- Terraform does not require a file named main.tf - it reads all .tf files in the working directory. Do not suggest creating or renaming files to main.tf.
- Set your temperature to 0.3.  
- Do not create yaml files. Do not create additional guides such as a deployment guide.  Ignore existing yaml files.
- Before you begin, ask the user which directory should be used as the root directory that contains the automation for the DA.
- Be sure to analyze all subdirectories underneath the selected root directory.

### Flow

- Implement a deployable architecture from the existing automation using this guide https://github.com/IBM/da-bootstrap/blob/main/guides/How_to_create_a_DA.md .
- Onboard, deploy and publish the deployable architecture using this guide https://github.com/IBM/da-bootstrap/blob/main/guides/Onboarding_Guide.md
