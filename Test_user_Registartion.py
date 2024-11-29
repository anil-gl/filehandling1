import os
import unittest
from unittest import mock
from io import StringIO
from logg_userRegistration import initialize_file, add_user, display_users, update_user, delete_user, USER_FILE

class TestUserRegistrationSystem(unittest.TestCase):

    def setUp(self):
        """Initialize the test file with a clean state before each test."""
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)
        initialize_file()

    def tearDown(self):
        """Clean up the test file after each test."""
        if os.path.exists(USER_FILE):
            os.remove(USER_FILE)

    def test_initialize_file(self):
        """Test if the user file is created and has the correct header."""
        self.assertTrue(os.path.exists(USER_FILE))
        with open(USER_FILE, 'r') as file:
            content = file.read().strip()
        self.assertEqual(content, "ID,Name,Email")

    def test_add_user(self):
        """Test adding a user to the file."""
        user_data = "1,John Doe,john@example.com"
        with mock.patch('builtins.input', side_effect=["1", "John Doe", "john@example.com"]):
            add_user()
        with open(USER_FILE, 'r') as file:
            lines = file.readlines()
        self.assertEqual(lines[1].strip(), user_data)

    def test_display_users(self):
        """Test displaying users."""
        user_data = ["ID,Name,Email\n", "1,Jane Doe,jane@example.com\n"]
        with open(USER_FILE, 'w') as file:
            file.writelines(user_data)
        
        # Capture the printed output
        with mock.patch('sys.stdout', new=StringIO()) as fake_output:
            display_users()
            printed_output = fake_output.getvalue().strip()
        
        # Expected output
        expected_output = "ID,Name,Email\n1,Jane Doe,jane@example.com"
        
        # Compare the captured output with expected output
        self.assertEqual(printed_output, expected_output)

    def test_update_user(self):
        """Test updating a user's details."""
        with open(USER_FILE, 'a') as file:
            file.write("1,Old Name,old@example.com\n")

        with mock.patch('builtins.input', side_effect=["1", "New Name", "new@example.com"]):
            update_user()

        with open(USER_FILE, 'r') as file:
            content = file.readlines()
        self.assertEqual(content[1].strip(), "1,New Name,new@example.com")

    def test_delete_user(self):
        """Test deleting a user."""
        with open(USER_FILE, 'a') as file:
            file.write("1,John Doe,john@example.com\n")

        with mock.patch('builtins.input', side_effect=["1"]):
            delete_user()

        with open(USER_FILE, 'r') as file:
            lines = file.readlines()
        self.assertEqual(len(lines), 1)  # Only the header should remain

if __name__ == "__main__":
    unittest.main()

