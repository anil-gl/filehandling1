import os
import logging

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
    Initializes the user data file if it does not exist.
    Creates a file with a header "ID,Name,Email".
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

def add_user():
    """
    Adds a new user to the user data file.
    Prompts the user to enter ID, Name, and Email, and appends the information to the file.
    """
    try:
        user_id = input("Enter User ID: ")
        name = input("Enter User Name: ")
        email = input("Enter User Email: ")
        
        # Append the user data to the file
        with open(USER_FILE, 'a') as file:
            file.write(f"{user_id},{name},{email}\n")
        logging.info(f"User '{name}' added successfully with ID {user_id}.")
    except Exception as e:
        logging.error(f"Error adding user: {e}")

def display_users():
    """
    Displays all users from the user data file.
    Reads the file and prints each line (user data).
    """
    try:
        if not os.path.exists(USER_FILE):
            raise FileNotFoundError(f"File '{USER_FILE}' not found.")

        with open(USER_FILE, 'r') as file:
            print("\n--- User Data ---")
            for line in file:
                print(line.strip())
        logging.info("Displayed all users successfully.")
    except FileNotFoundError as e:
        logging.error(e)
    except Exception as e:
        logging.error(f"Error reading file: {e}")

def update_user():
    """
    Updates a user's details in the user data file based on their ID.
    Prompts for the user ID and allows updating the name and/or email.
    """
    try:
        user_id = input("Enter User ID to update: ")
        new_name = input("Enter new name (leave blank to keep unchanged): ")
        new_email = input("Enter new email (leave blank to keep unchanged): ")
        
        updated = False
        users = []

        # Read all users and update the target user
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
        else:
            logging.warning(f"User ID {user_id} not found.")
    except Exception as e:
        logging.error(f"Error updating user: {e}")

def delete_user():
    """
    Deletes a user from the user data file based on their ID.
    Prompts for the user ID and removes the corresponding record if found.
    """
    try:
        user_id = input("Enter User ID to delete: ")
        deleted = False
        users = []

        # Read all users and remove the target user
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
        else:
            logging.warning(f"User ID {user_id} not found.")
    except Exception as e:
        logging.error(f"Error deleting user: {e}")

def main():
    """
    Main function that provides a menu for interacting with the user registration system.
    """
    initialize_file()

    while True:
        print("\n--- User Registration System ---")
        print("1. Add User")
        print("2. Display All Users")
        print("3. Update User")
        print("4. Delete User")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

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
            break
        else:
            logging.warning("Invalid choice entered by the user.")

if __name__ == "__main__":
    main()
