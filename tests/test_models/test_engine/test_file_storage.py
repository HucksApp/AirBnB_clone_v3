#!/usr/bin/python3
"""
Unit Test for BaseModel Class
"""
import unittest
from datetime import datetime
import models
from models import engine
from models.engine.file_storage import FileStorage
import json
import os
import subprocess
from tests import PRETIFY

User = models.user.User
BaseModel = models.base_model.BaseModel
FileStorage = engine.file_storage.FileStorage
storage = models.storage

storage_type = os.environ.get('HBNB_TYPE_STORAGE')
F = './file.json'
pretify_test = os.environ.get('PRETIFY')


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestFileStorageDocs(unittest.TestCase):
    """Class for testing BaseModel docs"""

    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing ------- Documentation'
            n = 'For FileStorage Class'
            PRETIFY(t, n)

    def test_doc_file(self):
        """... documentation for the file"""
        expected = ("\nFileStorage engine class\n")
        actual = models.engine.file_storage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = ("\n    serializes and deserializes between object"
                    "\n    instances and json rep storage\n    ")
        actual = FileStorage.__doc__
        self.assertEqual(expected, actual)

    def test_doc_all(self):
        """... documentation for all function"""
        expected = 'returns private attribute: __objects'
        actual = FileStorage.all.__doc__
        self.assertEqual(expected, actual)

    def test_doc_new(self):
        """... documentation for new function"""
        expected = ("sets in __objects the obj with key <obj class "
                    "name>.id")
        actual = FileStorage.new.__doc__
        self.assertEqual(expected, actual)

    def test_doc_get(self):
        """... documentation for get function"""
        expected = 'query for  one object'
        actual = FileStorage.get.__doc__
        self.assertEqual(expected, actual)

    def test_doc_count(self):
        """... documentation for get function"""
        expected = ("query to count object of a class"
                    " or all object in storage")
        actual = FileStorage.count.__doc__
        self.assertEqual(expected, actual)

    def test_doc_save(self):
        """... documentation for save function"""
        expected = 'serializes __objects to the JSON file (path: __file_path)'
        actual = FileStorage.save.__doc__
        self.assertEqual(expected, actual)

    def test_doc_reload(self):
        """... documentation for reload function"""
        expected = ("if file exists, deserializes JSON file"
                    " to __objects")
        actual = FileStorage.reload.__doc__
        self.assertEqual(expected, actual)


@unittest.skipIf(storage_type == 'db', 'skip if environ is db')
class TestBmFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing FileStorate'
            n = 'For FileStorage Class'
            PRETIFY(t, n)
        if os.path.isfile(F):
            cmd = "m=$(pwd);mv $m/file.json $m/tmp.json && touch $m/file.json"
            subprocess.call(cmd, shell=True, executable="/bin/bash")

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(F):
            cmd = "m=$(pwd);rm $m/file.json;mv $m/tmp.json $m/file.json"
            subprocess.call(cmd, shell=True, executable="/bin/bash")

    def setUp(self):
        """initializes new storage object for testing"""
        self.storage = FileStorage()
        self.bm_obj = BaseModel()

    def test_instantiation(self):
        """... checks proper FileStorage instantiation"""
        self.assertIsInstance(self.storage, FileStorage)

    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        if os.path.isfile(F):
            os.remove(F)
        self.bm_obj.save()
        self.assertTrue(os.path.isfile(F))

    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        if os.path.isfile(F):
            os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_to_json(self):
        """... to_json should return serializable dict object"""
        my_model_json = self.bm_obj.to_dict()
        actual = 1
        try:
            serialized = json.dumps(my_model_json)
        except:
            actual = 0
        self.assertTrue(1 == actual)

    def test_reload(self):
        """... checks proper usage of reload function"""
        if os.path.isfile(F):
            os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if bm_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    def test_save_reload_class(self):
        """... checks proper usage of class attribute in file storage"""
        if os.path.isfile(F):
            os.remove(F)
        self.bm_obj.save()
        bm_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k, v in all_obj.items():
            if bm_id in k:
                if type(v).__name__ == 'BaseModel':
                    actual = 1
        self.assertTrue(1 == actual)


class TestUserFsInstances(unittest.TestCase):
    """testing for class instances"""

    @classmethod
    def setUpClass(cls):
        if pretify_test == 'True':
            t = 'Testing FileStorate'
            n = 'User Class'
            PRETIFY(t, n)
        if os.path.isfile(F):
            cmd = "m=$(pwd);mv $m/file.json $m/tmp.json && touch $m/file.json"
            subprocess.call(cmd, shell=True, executable="/bin/bash")

    @classmethod
    def tearDownClass(cls):
        if os.path.isfile(F):
            cmd = "m=$(pwd);rm $m/file.json;mv $m/tmp.json $m/file.json"
            subprocess.call(cmd, shell=True, executable="/bin/bash")

    def setUp(self):
        """initializes new user for testing"""
        self.user = User()
        self.bm_obj = BaseModel()

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_storage_file_exists(self):
        """... checks proper FileStorage instantiation"""
        if os.path.isfile(F):
            os.remove(F)
        self.user.save()
        self.assertTrue(os.path.isfile(F))

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_obj_saved_to_file(self):
        """... checks proper FileStorage instantiation"""
        if os.path.isfile(F):
            os.remove(F)
        self.user.save()
        u_id = self.user.id
        actual = 0
        with open(F, mode='r', encoding='utf-8') as f_obj:
            storage_dict = json.load(f_obj)
        for k in storage_dict.keys():
            if u_id in k:
                actual = 1
        self.assertTrue(1 == actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_reload(self):
        """... checks proper usage of reload function"""
        if os.path.isfile(F):
            os.remove(F)
        self.bm_obj.save()
        u_id = self.bm_obj.id
        actual = 0
        new_storage = FileStorage()
        new_storage.reload()
        all_obj = new_storage.all()
        for k in all_obj.keys():
            if u_id in k:
                actual = 1
        self.assertTrue(1 == actual)


@unittest.skipIf(storage_type == 'db', 'skip if environ is not db')
class TestStorageGet(unittest.TestCase):
    """
    Testing `get()` method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        if pretify_test == 'True':
            t = 'Testing Get() Method'
            n = 'Place  Class'
            PRETIFY(t, n)

    def setUp(self):
        """
        setup method
        """
        self.state = models.state.State(name="Florida")
        self.state.save()

    def test_get_method_obj(self):
        """
        testing get() method
        :return: True if pass, False if not pass
        """

        result = storage.get(cls="State", id=self.state.id)
        self.assertIsInstance(result, models.state.State)

    def test_get_method_return(self):
        """
        testing get() method for id match
        :return: True if pass, false if not pass
        """
        result = storage.get(cls="State", id=str(self.state.id))
        self.assertEqual(self.state.id, result.id)

    def test_get_method_none(self):
        """
        testing get() method for None return
        :return: True if pass, false if not pass
        """
        result = storage.get(cls="State", id="doesnotexist")

        self.assertIsNone(result)


@unittest.skipIf(storage_type == 'db', 'skip if environ is not db')
class TestStorageCount(unittest.TestCase):
    """
    tests count() method in DBStorage
    """

    @classmethod
    def setUpClass(cls):
        """
        setup tests for class
        """
        if pretify_test == 'True':
            t = 'Testing Count() Method'
            n = 'Place Class'
            PRETIFY(t, n)

    def setup(self):
        """
        setup method
        """
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()
        models.state.State()

    def test_count_all(self):
        """
        testing counting all instances
        :return: True if pass, false if not pass
        """
        result = storage.count()

        self.assertEqual(len(storage.all()), result)

    def test_count_state(self):
        """
        testing counting state instances
        :return: True if pass, false if not pass
        """
        result = storage.count(cls="State")

        self.assertEqual(len(storage.all("State")), result)

    def test_count_city(self):
        """
        testing counting non existent
        :return: True if pass, false if not pass
        """
        result = storage.count(cls="City")

        self.assertEqual(
            int(0 if len(storage.all("City")) is None else
                len(storage.all("City"))), result)


if __name__ == '__main__':
    unittest.main
