#!/usr/bin/python3
"""
Unit Test for City Class
"""
import unittest
from datetime import datetime
import models
import json
import os
from tests import PRETIFY


City = models.city.City
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')
pretify_test = os.environ.get('PRETIFY')


class TestCityDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing Documentation'
            n = 'City Class'
            PRETIFY(t, n)

    def test_doc_file(self):
        """... documentation for the file"""
        expected = 'City Model Class'
        actual = models.city.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'City class handles all application cities'
        actual = City.__doc__
        self.assertEqual(expected, actual)


class TestCityInstances(unittest.TestCase):
    """testing for class instances"""
    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing Attributes and Methods'
            n = 'City Class'
            PRETIFY(t, n)

    def setUp(self):
        """initializes new city for testing"""
        self.city = City()

    def test_instantiation(self):
        """... checks if City is properly instantiated"""
        self.assertIsInstance(self.city, City)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.city)
        my_list = ['City', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation(self):
        """... should not have updated attribute"""
        self.city = City()
        my_str = str(self.city)
        actual = 0
        if 'updated_at' in my_str:
            if 'created_at' in my_str:
                actual += 1
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """... save function should add updated_at attribute"""
        self.city.save()
        actual = type(self.city.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """... to_json should return serializable dict object"""
        self.city_json = self.city.to_dict()
        actual = 1
        try:
            serialized = json.dumps(self.city_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """... to_json should include class key with value City"""
        self.city_json = self.city.to_dict()
        actual = None
        if self.city_json['__class__']:
            actual = self.city_json['__class__']
        expected = 'City'
        self.assertEqual(expected, actual)

    def test_state_attribute(self):
        """... add state attribute"""
        self.city.state_id = 'IL'
        if hasattr(self.city, 'state_id'):
            actual = self.city.state_id
        else:
            actual = ''
        expected = 'IL'
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main
