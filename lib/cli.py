from helpers import list_causes, list_donors, list_donations_for_cause, make_donation, add_new_cause

def menu():
    print(" Welcome to the Donation Management CLI")

    while True:
        print("\n" + "="*40)
        print(" MAIN MENU")
        print("="*40)
        print("1. List Causes")
        print("2. List Donors")
        print("3. View Donations for a Cause")
        print("4. Make a Donation")
        print("5. Add New Cause")
        print("6. Exit")
        print("="*40)
        
        choice = input("Choose an option (1-6): ").strip()

        if choice == "1":
            list_causes()
        elif choice == "2":
            list_donors()
        elif choice == "3":
            try:
                cause_id = int(input("Enter Cause ID: "))
                list_donations_for_cause(cause_id)
            except ValueError:
                print(" Please enter a valid integer for Cause ID.")
        elif choice == "4":
            make_donation()
        elif choice == "5":
            add_new_cause()
        elif choice == "6":
            print("Goodbye and thank you for supporting great causes!")
            break
        else:
            print(" Invalid choice. Please select a valid option (1-6).")

if __name__ == "__main__":
    menu()
