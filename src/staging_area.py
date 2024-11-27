# Vocabulary Manager - Step 1: Basic Structure

# Staging area to temporarily hold words/phrases
staging_area = []

def display_menu():
    print("\n--- Vocabulary Manager ---")
    print("1. Add a word or phrase to the staging area")
    print("2. View staging area")
    print("3. Exit")

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

# Main program loop
def main():
    while True:
        display_menu()
        choice = input("Choose an option (1-3): ")
        
        if choice == "1":
            add_to_staging()
        elif choice == "2":
            view_staging_area()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
