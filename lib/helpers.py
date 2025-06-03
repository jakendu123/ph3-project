from seed import session

def list_causes():
    from models import Cause
    causes = Cause.get_all()
    if causes:
        print("\n List of Causes:")
        for cause in causes:
            progress = cause.progress_percentage
            print(f"[{cause.id}] {cause.name}")
            print(f"    Goal: {cause.goal:.2f} | Raised: {cause.amount_raised:.2f} | Progress: {progress:.1f}%")
    else:
        print(" No causes found.")

def list_donors():
    from models import Donor
    donors = Donor.get_all()
    if donors:
        print("\n List of Donors:")
        for donor in donors:
            print(f"[{donor.id}] {donor.name} <{donor.email}> - Total Donated: {donor.total_donated:.2f}")
    else:
        print(" No donors found.")

def list_donations_for_cause(cause_id):
    from models import Cause
    cause = Cause.get_by_id(cause_id)
    if not cause:
        print(" Cause not found.")
        return

    print(f"\n Donations for Cause: {cause.name}")
    if cause.donations:
        total = 0
        for donation in cause.donations:
            print(f"- {donation.amount:.2f} by {donation.donor.name} on {donation.date.strftime('%Y-%m-%d')}")
            total += donation.amount
        print(f"\nTotal raised: {total:.2f} / {cause.goal:.2f}")
    else:
        print("No donations yet for this cause.")

def create_or_get_donor():
    """Create a new donor or get existing one by email"""
    from models import Donor
    
    print("\n Donor Information:")
    email = input("Enter your email: ").strip()
    
    
    existing_donor = Donor.get_by_email(email)
    if existing_donor:
        print(f"Welcome back, {existing_donor.name}!")
        return existing_donor
    
    
    name = input("Enter your name: ").strip()
    if not name:
        print(" Name cannot be empty.")
        return None
    
    new_donor = Donor(name=name, email=email)
    new_donor.save()
    print(f" New donor created: {name}")
    return new_donor

def make_donation():
    """Make a donation with donor creation/selection"""
    from models import Cause, Donation
    
    
    donor = create_or_get_donor()
    if not donor:
        return
    
    list_causes()
    
    try:
        cause_id = int(input("\nEnter Cause ID: "))
        cause = Cause.get_by_id(cause_id)
        
        if not cause:
            print(" Cause not found.")
            return
        
        amount = float(input("Enter Donation Amount: "))
        if amount <= 0:
            print(" Donation amount must be greater than zero.")
            return
        
        
        donation = Donation(donor=donor, cause=cause, amount=amount)
        donation.save()
        
        print(f" Donation of {amount:.2f} successfully added from {donor.name} to {cause.name}.")
        print(f" {cause.name} progress: {cause.progress_percentage:.1f}% of {cause.goal:.2f} goal")
        
    except ValueError:
        print(" Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f" Error making donation: {e}")

def add_new_cause():
    """Add a new cause to the system"""
    from models import Cause
    
    print("\n Add New Cause:")
    name = input("Enter cause name: ").strip()
    if not name:
        print(" Cause name cannot be empty.")
        return
    
    try:
        goal = float(input("Enter fundraising goal: "))
        if goal <= 0:
            print(" Goal must be greater than zero.")
            return
        
        new_cause = Cause(name=name, goal=goal)
        new_cause.save()
        print(f" New cause '{name}' created with goal of {goal:.2f}")
        
    except ValueError:
        print(" Invalid goal amount. Please enter a valid number.")
    except Exception as e:
        print(f" Error creating cause: {e}")
