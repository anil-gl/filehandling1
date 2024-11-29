import os
import unittest
from unittest import mock
from io import StringIO
from logg_userRegistration import initialize_file, add_user, display_users, update_user, delete_user, USER_FILE

class TestUserRegistrationSystem(unittest.TestCase):

    def setUp(self):
        """Set up a clean state before each test by initializing the user file."""
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)
        initialize_file()

    def tearDown(self):
        """Clean up the user file after each test."""
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)

    def test_initialize_file(self):
        """Test if the file is created with the correct header."""
        self.assertTrue(os.path.exists(USER_FILE))
        with open(USER_FILE, 'r') as file:
            content = file.read().strip()
        self.assertEqual(content, "ID,Name,Email")

    def test_add_user(self):
        """Test adding a valid user to the system."""
        user_data = "1,John Doe,john@example.com"
        with mock.patch('builtins.input', side_effect=["1", "John Doe", "john@example.com"]):
            add_user()
        with open(USER_FILE, 'r') as file:
            lines = file.readlines()
        self.assertEqual(lines[1].strip(), user_data)

    def test_add_user_with_blank_fields(self):
        """Test adding a user with blank fields should raise an error."""
        with mock.patch('builtins.input', side_effect=["", "", ""]):
            with mock.patch('sys.stdout', new=StringIO()) as fake_output:
                add_user()
                self.assertIn("All fields (ID, Name, Email) are required.", fake_output.getvalue().strip())

    def test_display_users(self):
        """Test displaying users when there is data in the file."""
        user_data = ["ID,Name,Email\n", "1,Jane Doe,jane@example.com\n"]
        with open(USER_FILE, 'w') as file:
            file.writelines(user_data)
        with mock.patch('sys.stdout', new=StringIO()) as fake_output:
            display_users()
            printed_output = fake_output.getvalue().strip()
        self.assertEqual(printed_output, "ID,Name,Email\n1,Jane Doe,jane@example.com")

    def test_update_user(self):
        """Test updating an existing user's details."""
        with open(USER_FILE, 'a') as file:
            file.write("1,Old Name,old@example.com\n")
        with mock.patch('builtins.input', side_effect=["1", "New Name", "new@example.com"]):
            update_user()
        with open(USER_FILE, 'r') as file:
            lines = file.readlines()
        self.assertEqual(lines[1].strip(), "1,New Name,new@example.com")

    def test_update_non_existent_user(self):
        """Test attempting to update a user that does not exist."""
        with mock.patch('builtins.input', side_effect=["999", "New Name", "new@example.com"]):
            with mock.patch('sys.stdout', new=StringIO()) as fake_output:
                update_user()
                self.assertIn("User ID 999 not found", fake_output.getvalue().strip())

    def test_delete_user(self):
        """Test deleting an existing user from the system."""
        with open(USER_FILE, 'a') as file:
            file.write("1,John Doe,john@example.com\n")
        with mock.patch('builtins.input', side_effect=["1"]):
            delete_user()
        with open(USER_FILE, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 1)  # Only the header remains

    def test_delete_non_existent_user(self):
        """Test attempting to delete a user that does not exist."""
        with mock.patch('builtins.input', side_effect=["999"]):
            with mock.patch('sys.stdout', new=StringIO()) as fake_output:
                delete_user()
                self.assertIn("User ID 999 not found", fake_output.getvalue().strip())

if __name__ == "__main__":
    unittest.main()
