import unittest

from veld_spec import validate


class TestVeldMetadata(unittest.TestCase):
    
    def test_chain_barebone_valid(self):
        result = validate(yaml_to_validate="./veld_yaml_files/chain_barebone_valid.yaml")
        print(result[1])
        self.assertTrue(result[0])
    
    def test_chain_barebone_invalid(self):
        result = validate(yaml_to_validate="./veld_yaml_files/chain_barebone_invalid.yaml")
        print(result[1])
        self.assertFalse(result[0])
    
    def test_code_barebone_valid(self):
        result = validate(yaml_to_validate="./veld_yaml_files/code_barebone_valid.yaml")
        print(result[1])
        self.assertTrue(result[0])
    
    def test_code_barebone_invalid(self):
        result = validate(yaml_to_validate="./veld_yaml_files/code_barebone_invalid.yaml")
        print(result[1])
        self.assertFalse(result[0])
    
    def test_data_barebone_valid(self):
        result = validate(yaml_to_validate="./veld_yaml_files/data_barebone_valid.yaml")
        print(result[1])
        self.assertTrue(result[0])
    
    def test_data_barebone_invalid(self):
        result = validate(yaml_to_validate="./veld_yaml_files/data_barebone_invalid.yaml")
        print(result[1])
        self.assertFalse(result[0])
