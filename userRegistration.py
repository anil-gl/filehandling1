import os

# File path for storing user data
USER_FILE = 'user_data.txt'

# Function to initialize the user file if it doesn't exist
def initialize_file():
    try:
        if not os.path.exists(USER_FILE):
            with open(USER_FILE, 'w') as file:
                file.write("ID,Name,Email\n")  # Write header
            print(f"File '{USER_FILE}' created successfully.")
        else:
            print(f"File '{USER_FILE}' already exists.")
    except PermissionError:
        print(f"Permission denied: Cannot create '{USER_FILE}'")
    except Exception as e:
        print(f"Error initializing file: {e}")

# Function to add a new user
def add_user():
    try:
        user_id = input("Enter User ID: ")
        name = input("Enter User Name: ")
        email = input("Enter User Email: ")
        
        # Append the user data to the file
        with open(USER_FILE, 'a') as file:
            file.write(f"{user_id},{name},{email}\n")
        print(f"User '{name}' added successfully.")
    except Exception as e:
        print(f"Error adding user: {e}")

# Function to display all users
def display_users():
    try:
        if not os.path.exists(USER_FILE):
            raise FileNotFoundError(f"File '{USER_FILE}' not found.")

        with open(USER_FILE, 'r') as file:
            print("\n--- User Data ---")
            for line in file:
                print(line.strip())
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(f"Error reading file: {e}")

# Function to update user details by ID
def update_user():
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
            print(f"User ID {user_id} updated successfully.")
        else:
            print(f"User ID {user_id} not found.")
    except Exception as e:
        print(f"Error updating user: {e}")

# Function to delete a user by ID
def delete_user():
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
            print(f"User ID {user_id} deleted successfully.")
        else:
            print(f"User ID {user_id} not found.")
    except Exception as e:
        print(f"Error deleting user: {e}")

# Main function with a menu for user interaction
def main():
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
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()