#!/usr/bin/env python3
"""
IBM Catalog Manifest Validation Tool

Validates ibm_catalog.json files for Deployable Architectures according to
IBM Cloud Catalog requirements.
"""

import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Tuple, Any

class CatalogValidator:
    def __init__(self, catalog_path: str):
        self.catalog_path = Path(catalog_path)
        self.errors = []
        self.warnings = []
        self.catalog_data = None
        
    def validate(self) -> bool:
        """Run all validation checks"""
        print(f"\n{'='*70}")
        print(f"Validating: {self.catalog_path}")
        print(f"{'='*70}\n")
        
        # Load and parse JSON
        if not self._load_json():
            return False
            
        # Run validation checks
        self._validate_structure()
        self._validate_products()
        self._validate_flavors()
        self._validate_iam_permissions()
        self._validate_configuration()
        self._validate_architecture()
        
        # Print results
        self._print_results()
        
        return len(self.errors) == 0
    
    def _load_json(self) -> bool:
        """Load and parse JSON file"""
        try:
            with open(self.catalog_path, 'r') as f:
                self.catalog_data = json.load(f)
            print("✅ JSON syntax is valid")
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON syntax: {e}")
            print(f"❌ Invalid JSON syntax: {e}")
            return False
        except FileNotFoundError:
            self.errors.append(f"File not found: {self.catalog_path}")
            print(f"❌ File not found: {self.catalog_path}")
            return False
    
    def _validate_structure(self):
        """Validate top-level structure"""
        if 'products' not in self.catalog_data:
            self.errors.append("Missing required field: 'products'")
            return
        
        if not isinstance(self.catalog_data['products'], list):
            self.errors.append("'products' must be an array")
            return
            
        if len(self.catalog_data['products']) == 0:
            self.errors.append("'products' array is empty")
        else:
            print(f"✅ Found {len(self.catalog_data['products'])} product(s)")
    
    def _validate_products(self):
        """Validate product-level fields"""
        required_fields = ['name', 'label', 'product_kind', 'short_description', 
                          'long_description', 'offering_docs_url', 'provider_name']
        
        for idx, product in enumerate(self.catalog_data.get('products', [])):
            product_name = product.get('name', f'Product {idx}')
            print(f"\n📦 Validating product: {product_name}")
            
            # Check required fields
            for field in required_fields:
                if field not in product:
                    self.errors.append(f"Product '{product_name}': Missing required field '{field}'")
                elif not product[field]:
                    self.warnings.append(f"Product '{product_name}': Field '{field}' is empty")
            
            # Validate product_kind
            if product.get('product_kind') not in ['solution', 'module']:
                self.errors.append(f"Product '{product_name}': product_kind must be 'solution' or 'module'")
            else:
                print(f"  ✅ Product kind: {product.get('product_kind')}")
            
            # Check tags
            if 'tags' in product and isinstance(product['tags'], list):
                print(f"  ✅ Tags: {len(product['tags'])} tag(s)")
            else:
                self.warnings.append(f"Product '{product_name}': No tags defined")
            
            # Check keywords
            if 'keywords' in product and isinstance(product['keywords'], list):
                print(f"  ✅ Keywords: {len(product['keywords'])} keyword(s)")
            else:
                self.warnings.append(f"Product '{product_name}': No keywords defined")
            
            # Check icon
            if 'offering_icon_url' not in product:
                self.warnings.append(f"Product '{product_name}': No offering_icon_url defined")
            else:
                print(f"  ✅ Icon URL defined")
    
    def _validate_flavors(self):
        """Validate flavor configurations"""
        for product in self.catalog_data.get('products', []):
            product_name = product.get('name', 'Unknown')
            
            if 'flavors' not in product:
                self.errors.append(f"Product '{product_name}': Missing 'flavors' array")
                continue
            
            if not isinstance(product['flavors'], list) or len(product['flavors']) == 0:
                self.errors.append(f"Product '{product_name}': 'flavors' must be a non-empty array")
                continue
            
            print(f"\n🍦 Validating {len(product['flavors'])} flavor(s) for '{product_name}'")
            
            for idx, flavor in enumerate(product['flavors']):
                flavor_name = flavor.get('name', f'Flavor {idx}')
                print(f"\n  Flavor: {flavor_name}")
                
                # Required flavor fields
                required_flavor_fields = ['label', 'name', 'install_type', 'working_directory']
                for field in required_flavor_fields:
                    if field not in flavor:
                        self.errors.append(f"Flavor '{flavor_name}': Missing required field '{field}'")
                    else:
                        print(f"    ✅ {field}: {flavor[field]}")
                
                # Validate install_type
                if flavor.get('install_type') not in ['fullstack', 'extension']:
                    self.errors.append(f"Flavor '{flavor_name}': install_type must be 'fullstack' or 'extension'")
    
    def _validate_iam_permissions(self):
        """Validate IAM permission CRNs"""
        crn_pattern = re.compile(r'^crn:v1:bluemix:public:iam::::(?:role|serviceRole):\w+$')
        
        for product in self.catalog_data.get('products', []):
            for flavor in product.get('flavors', []):
                flavor_name = flavor.get('name', 'Unknown')
                
                if 'iam_permissions' not in flavor:
                    self.warnings.append(f"Flavor '{flavor_name}': No IAM permissions defined")
                    continue
                
                print(f"\n  🔐 Validating IAM permissions for flavor '{flavor_name}'")
                
                for perm in flavor.get('iam_permissions', []):
                    service_name = perm.get('service_name', 'Unknown')
                    
                    if 'service_name' not in perm:
                        self.errors.append(f"Flavor '{flavor_name}': IAM permission missing 'service_name'")
                    
                    if 'role_crns' not in perm:
                        self.errors.append(f"Flavor '{flavor_name}': IAM permission for '{service_name}' missing 'role_crns'")
                        continue
                    
                    for crn in perm.get('role_crns', []):
                        if not crn_pattern.match(crn):
                            self.errors.append(f"Flavor '{flavor_name}': Invalid CRN format for service '{service_name}': {crn}")
                        else:
                            print(f"    ✅ {service_name}: Valid CRN")
    
    def _validate_configuration(self):
        """Validate configuration parameters"""
        for product in self.catalog_data.get('products', []):
            for flavor in product.get('flavors', []):
                flavor_name = flavor.get('name', 'Unknown')
                
                if 'configuration' not in flavor:
                    self.warnings.append(f"Flavor '{flavor_name}': No configuration parameters defined")
                    continue
                
                print(f"\n  ⚙️  Validating configuration for flavor '{flavor_name}'")
                
                config_params = flavor.get('configuration', [])
                print(f"    Found {len(config_params)} parameter(s)")
                
                required_params = [p for p in config_params if p.get('required', False)]
                print(f"    ✅ {len(required_params)} required parameter(s)")
                
                for param in config_params:
                    param_key = param.get('key', 'Unknown')
                    
                    # Check required parameter fields
                    if 'key' not in param:
                        self.errors.append(f"Flavor '{flavor_name}': Configuration parameter missing 'key'")
                    
                    if 'type' not in param:
                        self.errors.append(f"Flavor '{flavor_name}': Parameter '{param_key}' missing 'type'")
                    
                    # Validate type
                    valid_types = ['string', 'password', 'number', 'boolean', 'array', 'multiline']
                    if param.get('type') not in valid_types:
                        self.warnings.append(f"Flavor '{flavor_name}': Parameter '{param_key}' has unusual type: {param.get('type')}")
    
    def _validate_architecture(self):
        """Validate architecture diagrams and descriptions"""
        for product in self.catalog_data.get('products', []):
            for flavor in product.get('flavors', []):
                flavor_name = flavor.get('name', 'Unknown')
                
                if 'architecture' not in flavor:
                    self.warnings.append(f"Flavor '{flavor_name}': No architecture section defined")
                    continue
                
                print(f"\n  🏗️  Validating architecture for flavor '{flavor_name}'")
                
                arch = flavor['architecture']
                
                # Check descriptions
                if 'descriptions' in arch:
                    print(f"    ✅ Architecture description present")
                else:
                    self.warnings.append(f"Flavor '{flavor_name}': No architecture description")
                
                # Check features
                if 'features' in arch and isinstance(arch['features'], list):
                    print(f"    ✅ {len(arch['features'])} architecture feature(s)")
                
                # Check diagrams
                if 'diagrams' not in arch:
                    self.warnings.append(f"Flavor '{flavor_name}': No architecture diagrams defined")
                    continue
                
                for diagram in arch.get('diagrams', []):
                    if 'diagram' not in diagram:
                        self.errors.append(f"Flavor '{flavor_name}': Diagram missing 'diagram' object")
                        continue
                    
                    diag = diagram['diagram']
                    
                    if 'url' not in diag:
                        self.errors.append(f"Flavor '{flavor_name}': Diagram missing 'url'")
                    else:
                        print(f"    ✅ Diagram URL: {diag['url']}")
                    
                    if 'type' not in diag:
                        self.warnings.append(f"Flavor '{flavor_name}': Diagram missing 'type'")
    
    def _print_results(self):
        """Print validation results"""
        print(f"\n{'='*70}")
        print("VALIDATION RESULTS")
        print(f"{'='*70}\n")
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
            print()
        
        if self.errors:
            print(f"❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            print()
            print("❌ VALIDATION FAILED")
        else:
            print("✅ VALIDATION PASSED")
            if self.warnings:
                print(f"   (with {len(self.warnings)} warning(s))")
        
        print(f"\n{'='*70}\n")

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_catalog.py <path_to_ibm_catalog.json>")
        sys.exit(1)
    
    catalog_path = sys.argv[1]
    validator = CatalogValidator(catalog_path)
    
    success = validator.validate()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

# Made with Bob
