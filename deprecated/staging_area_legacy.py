# Vocabulary Manager - Step 3: Adding Delete Functionality

# Staging area and database
staging_area = []
approved_entries = []

def display_menu():
    print("\n--- Vocabulary Manager ---")
    print("1. Add a word or phrase to the staging area")
    print("2. View staging area")
    print("3. Edit a word/phrase in the staging area")
    print("4. Approve a word/phrase and move to the database")
    print("5. View approved database")
    print("6. Delete a word/phrase from the staging area")
    print("7. Delete multiple words/phrases from the staging area")
    print("8. Exit")

def add_to_staging():
    word_or_phrase = input("Enter a word or phrase: ")
    staging_area.append(word_or_phrase)
    print(f"'{word_or_phrase}' has been added to the staging area.")

def view_staging_area():
    if not staging_area:
        print("The staging area is empty.")
    else:
        print("\nStaging Area:")
        for i, item in enumerate(staging_area, 1):
            print(f"{i}. {item}")

def edit_staging_area():
    if not staging_area:
        print("The staging area is empty.")
        return
    view_staging_area()
    try:
        index = int(input("\nEnter the number of the word/phrase to edit: ")) - 1
        if index < 0 or index >= len(staging_area):
            print("Invalid choice.")
            return
        new_word_or_phrase = input("Enter the new word or phrase: ")
        staging_area[index] = new_word_or_phrase
        print(f"'{new_word_or_phrase}' has been updated.")
    except ValueError:
        print("Please enter a valid number.")

def approve_and_move_to_database():
    if not staging_area:
        print("The staging area is empty.")
        return
    view_staging_area()
    try:
        index = int(input("\nEnter the number of the word/phrase to approve: ")) - 1
        if index < 0 or index >= len(staging_area):
            print("Invalid choice.")
            return
        approved_entries.append(staging_area.pop(index))
        print(f"'{approved_entries[-1]}' has been approved and moved to the database.")
    except ValueError:
        print("Please enter a valid number.")

def view_approved_database():
    if not approved_entries:
        print("The database is empty.")
    else:
        print("\nApproved Database:")
        for i, item in enumerate(approved_entries, 1):
            print(f"{i}. {item}")

def delete_from_staging_area():
    if not staging_area:
        print("The staging area is empty.")
        return
    view_staging_area()
    try:
        index = int(input("\nEnter the number of the word/phrase to delete: ")) - 1
        if index < 0 or index >= len(staging_area):
            print("Invalid choice.")
            return
        deleted_item = staging_area.pop(index)
        print(f"'{deleted_item}' has been deleted.")
    except ValueError:
        print("Please enter a valid number.")

def delete_multiple_from_staging_area():
    if not staging_area:
        print("The staging area is empty.")
        return
    view_staging_area()
    try:
        indices = input("\nEnter the numbers of the words/phrases to delete (comma separated): ")
        indices = [int(x.strip()) - 1 for x in indices.split(",")]
        indices.sort(reverse=True)  # Sort to prevent index shifting while deleting
        for index in indices:
            if 0 <= index < len(staging_area):
                deleted_item = staging_area.pop(index)
                print(f"'{deleted_item}' has been deleted.")
            else:
                print(f"Invalid index {index + 1}.")
    except ValueError:
        print("Please enter valid numbers.")

# Main program loop
def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-8): ")
        
        if choice == "1":
            add_to_staging()
        elif choice == "2":
            view_staging_area()
        elif choice == "3":
            edit_staging_area()
        elif choice == "4":
            approve_and_move_to_database()
        elif choice == "5":
            view_approved_database()
        elif choice == "6":
            delete_from_staging_area()
        elif choice == "7":
            delete_multiple_from_staging_area()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

