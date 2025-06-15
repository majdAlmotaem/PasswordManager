import unittest
import os
from core import db

test_db_path = 'data/test_vault.db'

class TestDB(unittest.TestCase):
    def setUp(self):
        # Ensure a clean test database
        if os.path.exists(test_db_path):
            os.remove(test_db_path)
        db.initialize_db(test_db_path)

    def tearDown(self):
        if os.path.exists(test_db_path):
            os.remove(test_db_path)

    def test_add_and_get_entry(self):
        db.add_entry('gmail', 'user1', 'pass1', 'note1', test_db_path)
        entries = db.get_entries(test_db_path)
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(entry[1], 'gmail')
        self.assertEqual(entry[2], 'user1')
        self.assertEqual(entry[3], 'pass1')
        self.assertEqual(entry[4], 'note1')

    def test_update_entry(self):
        db.add_entry('gmail', 'user1', 'pass1', 'note1', test_db_path)
        entry_id = db.get_entries(test_db_path)[0][0]
        db.update_entry(entry_id, 'gmail', 'user2', 'pass2', 'note2', test_db_path)
        entry = db.get_entries(test_db_path)[0]
        self.assertEqual(entry[2], 'user2')
        self.assertEqual(entry[3], 'pass2')
        self.assertEqual(entry[4], 'note2')

    def test_delete_entry(self):
        db.add_entry('gmail', 'user1', 'pass1', 'note1', test_db_path)
        entry_id = db.get_entries(test_db_path)[0][0]
        db.delete_entry(entry_id, test_db_path)
        entries = db.get_entries(test_db_path)
        self.assertEqual(len(entries), 0)

if __name__ == '__main__':
    unittest.main()
