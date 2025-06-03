
"""
Simple Debug utility for the Donation Management System
"""

from seed import session
from models import Donor, Cause, Donation

def show_stats():
    """Show basic database statistics"""
    print("\n📊 DATABASE STATS")
    print("-" * 30)
    
    donor_count = len(session.query(Donor).all())
    cause_count = len(session.query(Cause).all())
    donation_count = len(session.query(Donation).all())
    
    print(f"Donors: {donor_count}")
    print(f"Causes: {cause_count}")
    print(f"Donations: {donation_count}")
    
    if donation_count > 0:
        total = sum(d.amount for d in session.query(Donation).all())
        print(f"Total donated: ${total:.2f}")

def show_donors():
    """Show all donors"""
    print("\n ALL DONORS")
    print("-" * 30)
    
    donors = session.query(Donor).all()
    if not donors:
        print("No donors found.")
        return
    
    for donor in donors:
        print(f"[{donor.id}] {donor.name} - ${donor.total_donated:.2f}")

def show_causes():
    """Show all causes"""
    print("\n ALL CAUSES")
    print("-" * 30)
    
    causes = session.query(Cause).all()
    if not causes:
        print("No causes found.")
        return
    
    for cause in causes:
        print(f"[{cause.id}] {cause.name}")
        print(f"    ${cause.amount_raised:.2f} / ${cause.goal:.2f} ({cause.progress_percentage:.1f}%)")

def show_donations():
    """Show recent donations"""
    print("\n RECENT DONATIONS")
    print("-" * 30)
    
    donations = session.query(Donation).order_by(Donation.date.desc()).limit(10).all()
    if not donations:
        print("No donations found.")
        return
    
    for donation in donations:
        print(f"${donation.amount:.2f} - {donation.donor.name} → {donation.cause.name}")

def test_donation():
    """Quick test to create a donation"""
    print("\n TEST DONATION")
    print("-" * 30)
    
    donors = session.query(Donor).all()
    causes = session.query(Cause).all()
    
    if not donors or not causes:
        print("Need at least 1 donor and 1 cause to test.")
        return
    
    print("Donors:")
    for donor in donors[:3]: 
        print(f"  [{donor.id}] {donor.name}")
    
    print("Causes:")
    for cause in causes[:3]: 
        print(f"  [{cause.id}] {cause.name}")
    
    try:
        donor_id = int(input("Donor ID: "))
        cause_id = int(input("Cause ID: "))
        amount = float(input("Amount: $"))
        
        donor = session.query(Donor).get(donor_id)
        cause = session.query(Cause).get(cause_id)
        
        if donor and cause and amount > 0:
            donation = Donation(donor=donor, cause=cause, amount=amount)
            donation.save()
            print(f"Test donation created: ${amount:.2f}")
        else:
            print("Invalid input")
    except:
        print(" Error creating test donation")

def clear_all_data():
    """Clear all data (use with caution!)"""
    print("\n CLEAR ALL DATA")
    print("-" * 30)
    
    confirm = input("Type 'DELETE' to confirm: ")
    if confirm == "DELETE":
        session.query(Donation).delete()
        session.query(Donor).delete()
        session.query(Cause).delete()
        session.commit()
        print(" All data cleared")
    else:
        print(" Cancelled")

def debug_menu():
    """Simple debug menu"""
    while True:
        print("\n" + "="*40)
        print(" DEBUG MENU")
        print("="*40)
        print("1. Show Stats")
        print("2. Show Donors")
        print("3. Show Causes")
        print("4. Show Donations")
        print("5. Test Donation")
        print("6. Clear All Data")
        print("0. Exit")
        
        choice = input("\nChoice: ")
        
        if choice == '1':
            show_stats()
        elif choice == '2':
            show_donors()
        elif choice == '3':
            show_causes()
        elif choice == '4':
            show_donations()
        elif choice == '5':
            test_donation()
        elif choice == '6':
            clear_all_data()
        elif choice == '0':
            print("Goodbye!")
            break
        else:
            print(" Invalid choice")
        
        input("\nPress Enter to continue...")

if __name__ == "__main__":
    debug_menu()
