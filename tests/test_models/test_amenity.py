#!/usr/bin/python3
"""
Unit Test for Amenity Class
"""
import unittest
from datetime import datetime
import models
import json
import os
from tests import PRETIFY

Amenity = models.amenity.Amenity
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')
pretify_test = os.environ.get('PRETIFY')


class TestAmenityDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing Documentation'
            n = 'Amenity  Class'
            PRETIFY(t, n)

    def test_doc_file(self):
        """... documentation for the file"""
        expected = 'Amenity Model Class'
        actual = models.amenity.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'Amenity class handles all application amenities'
        actual = Amenity.__doc__
        self.assertEqual(expected, actual)


class TestAmenityInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing Attributes and Methods'
            n = 'Amenity  Class'
            PRETIFY(t, n)

    def setUp(self):
        """initializes new amenity for testing"""
        self.amenity = Amenity()

    def test_instantiation(self):
        """... checks if Amenity is properly instantiated"""
        self.assertIsInstance(self.amenity, Amenity)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_string(self):
        """... checks if BaseModel is properly casted to string"""
        my_str = str(self.amenity)
        my_list = ['Amenity', 'id', 'created_at']
        actual = 0
        for sub_str in my_list:
            if sub_str in my_str:
                actual += 1
        self.assertTrue(3 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation(self):
        """... should not have updated attribute"""
        my_str = str(self.amenity)
        actual = 0
        if 'updated_at' in my_str:
            if 'created_at' in my_str:
                actual += 1
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """... save function should add updated_at attribute"""
        self.amenity.save()
        actual = type(self.amenity.updated_at)
        expected = type(datetime.now())
        self.assertEqual(expected, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """... to_json should return serializable dict object"""
        self.amenity_json = self.amenity.to_dict()
        actual = 1
        try:
            serialized = json.dumps(self.amenity_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """... to_json should include class key with value Amenity"""
        self.amenity_json = self.amenity.to_dict()
        actual = None
        if self.amenity_json['__class__']:
            actual = self.amenity_json['__class__']
        expected = 'Amenity'
        self.assertEqual(expected, actual)

    def test_amenity_attribute(self):
        """... add amenity attribute"""
        self.amenity.name = "testatt"
        if hasattr(self.amenity, 'name'):
            actual = self.amenity.name
        else:
            actual = ''
        expected = "testatt"
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main
