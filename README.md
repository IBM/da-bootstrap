# da-bootstrap

A comprehensive resource for AI-driven application to create and share a deployable architecture (DA) tile.

1. Create a Deployable Architecture (DA) manifest `ibm_catalog.json`
2. Onboard a terraform automation as a DA to a private catalog in the IBM cloud
3. Share a DA to other accounts and or onboard the automation to the public catalog

## Table of Contents

- [guide to Creating a DA manifest](https://github.com/IBM/da-bootstrap/blob/main/guides/How_to_create_a_DA.md)
- [manifest_validation_checklist](https://github.com/IBM/da-bootstrap/blob/main/guides/Manifest_validation_checklist.md)
- [guide to Onboarding a DA](https://github.com/IBM/da-bootstrap/blob/main/guides/Onboarding_Guide.md)

## First steps 

Bob should add the global custom mode named "📚 DA Developer" to his list of global modes defined in the file "custom_modes.yaml" file if it is not already present.  After adding the "📚 DA Developer" mode, Bob should switch modes to "📚 DA Developer" mode.  The mode is defined as:
```
- slug: da-developer
    name: 📚 DA Developer
    roleDefinition: Specialized mode for creating and managing IBM Cloud Deployable Architectures (DAs).  Helps with creating manifests,  architecture diagrams, and onboarding to IBM Cloud Catalog.
    description: Specialized mode for creating and managing IBM Cloud Deployable Architectures (DAs).
    customInstructions: |-
      Use guides found in this github repository https://github.com/IBM/da-bootstrap as needed to create a DA manifest.

      Use guides found in this github repository https://github.com/IBM/da-bootstrap as needed to onboard the DA to a private catalog.

      Set your temperature to 0.3.  Do not create yaml files. Do not create additional guides.

      Before you begin, ask the user which directory should be used as the root directory that contains the automation for the DA.
    groups:
      - read
      - edit
      - browser
      - command
    source: global
```    