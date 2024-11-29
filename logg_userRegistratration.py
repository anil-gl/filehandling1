import logging
import os
import re  # For email validation

# Configure logging
logging.basicConfig(
    filename='user_system.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# File path for storing user data
USER_FILE = 'user_data.txt'

def initialize_file():
    """
    Initializes the user data file with a header if it does not exist.
    
    This function creates the user data file with the columns 'ID', 'Name', and 'Email'.
    Logs an info message if the file is created or already exists.
    """
    try:
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, 'w') as file:
                file.write("ID,Name,Email\n")  # Write header
            logging.info(f"File '{USER_FILE}' created successfully.")
        else:
            logging.info(f"File '{USER_FILE}' already exists.")
    except PermissionError:
        logging.error(f"Permission denied: Cannot create '{USER_FILE}'")
    except Exception as e:
        logging.error(f"Error initializing file: {e}")

def validate_email(email):
    """
    Validates the format of the email address.
    
    Args:
        email (str): The email address to validate.
        
    Returns:
        bool: True if the email format is valid, False otherwise.
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def add_user():
    """
    Adds a new user to the user data file.
    
    Prompts the user for ID, name, and email. Validates the input and ensures the user ID is unique.
    Logs the addition of the user and handles errors such as blank fields or invalid email format.
    """
    try:
        user_id = input("Enter User ID: ").strip()
        name = input("Enter User Name: ").strip()
        email = input("Enter User Email: ").strip()
        
        if not user_id or not name or not email:
            raise ValueError("All fields (ID, Name, Email) are required.")
        if not validate_email(email):
            raise ValueError("Invalid email format.")

        # Check if the user ID already exists
        with open(USER_FILE, 'r') as file:
            for line in file:
                if line.split(',')[0] == user_id:
                    raise ValueError(f"User ID {user_id} already exists.")

        # Append the user data to the file
        with open(USER_FILE, 'a') as file:
            file.write(f"{user_id},{name},{email}\n")
        logging.info(f"User '{name}' added successfully with ID {user_id}.")
        print("User added successfully.")
    except ValueError as ve:
        logging.warning(f"Validation error: {ve}")
        print(f"Error: {ve}")
    except Exception as e:
        logging.error(f"Error adding user: {e}")
        print("An unexpected error occurred while adding the user.")

def display_users():
    """
    Displays all users from the user data file.
    
    Reads and prints the contents of the user data file, or informs the user if no data is found.
    Logs the operation and handles file-related errors.
    """
    try:
        if not os.path.exists(USER_FILE):
            raise FileNotFoundError(f"File '{USER_FILE}' not found.")

        with open(USER_FILE, 'r') as file:
            users = file.readlines()
            if len(users) == 1:
                print("No users found.")
                logging.info("Displayed users: No users found.")
            else:
                for line in users:
                    print(line.strip())
                logging.info("Displayed all users successfully.")
    except FileNotFoundError as e:
        logging.error(e)
        print(e)
    except Exception as e:
        logging.error(f"Error reading file: {e}")
        print("An unexpected error occurred while displaying users.")

def update_user():
    """
    Updates a user's details in the user data file based on their ID.
    
    Prompts the user for the ID of the user to update and allows changing their name and/or email.
    Validates input and ensures the user exists before updating.
    Logs the operation and handles errors such as invalid input or user not found.
    """
    try:
        user_id = input("Enter User ID to update: ").strip()
        if not user_id:
            raise ValueError("User ID is required.")

        new_name = input("Enter new name (leave blank to keep unchanged): ").strip()
        new_email = input("Enter new email (leave blank to keep unchanged): ").strip()

        if new_email and not validate_email(new_email):
            raise ValueError("Invalid email format.")

        updated = False
        users = []

        with open(USER_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == user_id:
                    if new_name:
                        parts[1] = new_name
                    if new_email:
                        parts[2] = new_email
                    updated = True
                users.append(','.join(parts))

        if updated:
            with open(USER_FILE, 'w') as file:
                file.write("\n".join(users) + "\n")
            logging.info(f"User ID {user_id} updated successfully.")
            print("User updated successfully.")
        else:
            logging.warning(f"User ID {user_id} not found.")
            print(f"Error: User ID {user_id} not found.")
    except ValueError as ve:
        logging.warning(f"Validation error: {ve}")
        print(f"Error: {ve}")
    except Exception as e:
        logging.error(f"Error updating user: {e}")
        print("An unexpected error occurred while updating the user.")

def delete_user():
    """
    Deletes a user from the user data file based on their ID.
    
    Prompts the user for the ID to delete and removes the corresponding entry if found.
    Logs the operation and handles errors such as invalid input or user not found.
    """
    try:
        user_id = input("Enter User ID to delete: ").strip()
        if not user_id:
            raise ValueError("User ID is required.")

        deleted = False
        users = []

        with open(USER_FILE, 'r') as file:
            for line in file:
                parts = line.strip().split(',')
                if parts[0] == user_id:
                    deleted = True
                    continue  # Skip adding this user
                users.append(','.join(parts))

        if deleted:
            with open(USER_FILE, 'w') as file:
                file.write("\n".join(users) + "\n")
            logging.info(f"User ID {user_id} deleted successfully.")
            print("User deleted successfully.")
        else:
            logging.warning(f"User ID {user_id} not found.")
            print(f"Error: User ID {user_id} not found.")
    except ValueError as ve:
        logging.warning(f"Validation error: {ve}")
        print(f"Error: {ve}")
    except Exception as e:
        logging.error(f"Error deleting user: {e}")
        print("An unexpected error occurred while deleting the user.")

def main():
    """
    Main function providing a menu for user interaction.
    
    Displays a menu with options to add, display, update, or delete users, or exit the program.
    Handles user input and calls the appropriate functions.
    """
    initialize_file()

    while True:
        print("\n--- User Registration System ---")
        print("1. Add User")
        print("2. Display All Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            add_user()
        elif choice == '2':
            display_users()
        elif choice == '3':
            update_user()
        elif choice == '4':
            delete_user()
        elif choice == '5':
            logging.info("Program exited by the user.")
            print("Exiting the program.")
            break
        else:
            logging.warning("Invalid choice entered by the user.")
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()
