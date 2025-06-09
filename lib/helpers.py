from seed import session

def list_causes():
    from models import Cause
    causes = Cause.get_all()
    if causes:
        print("\nList of Causes:")
        for cause in causes:
            progress = cause.progress_percentage
            print(f"[{cause.id}] {cause.name}")
            print(f"    Goal: ksh {cause.goal:.2f} | Raised: ksh {cause.amount_raised:.2f} | Progress: {progress:.1f}%")
    else:
        print("No causes found.")

def list_donors():
    from models import Donor
    donors = Donor.get_all()
    if donors:
        print("\nList of Donors:")
        for donor in donors:
            print(f"[{donor.id}] {donor.name} <{donor.email}> - Total Donated: ksh {donor.total_donated:.2f}")
    else:
        print("No donors found.")

def list_donations_for_cause(cause_id):
    from models import Cause
    cause = Cause.get_by_id(cause_id)
    if not cause:
        print("Cause not found.")
        return

    print(f"\n💰 Donations for Cause: {cause.name}")
    if cause.donations:
        total = 0
        for donation in cause.donations:
            print(f"- ksh {donation.amount:.2f} by {donation.donor.name} on {donation.date.strftime('%Y-%m-%d')}")
            total += donation.amount
        print(f"\nTotal raised: ksh {total:.2f} / ksh {cause.goal:.2f}")
    else:
        print("No donations yet for this cause.")

def create_or_get_donor():
    from models import Donor

    print("\nDonor Information:")
    email = input("Enter your email: ").strip()

    existing_donor = Donor.get_by_email(email)
    if existing_donor:
        print(f"Welcome back, {existing_donor.name}!")
        return existing_donor

    name = input("Enter your name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return None

    new_donor = Donor(name=name, email=email)
    new_donor.save()
    print(f"New donor created: {name}")
    return new_donor

def make_donation():
    from models import Cause, Donation

    donor = create_or_get_donor()
    if not donor:
        return

    list_causes()

    try:
        cause_id = int(input("\nEnter Cause ID: "))
        cause = Cause.get_by_id(cause_id)

        if not cause:
            print("Cause not found.")
            return

        amount = float(input("Enter Donation Amount (ksh): "))
        if amount <= 0:
            print("Donation amount must be greater than zero.")
            return

        donation = Donation(donor=donor, cause=cause, amount=amount)
        donation.save()

        print(f"Donation of ksh {amount:.2f} successfully added from {donor.name} to {cause.name}.")
        print(f"{cause.name} progress: {cause.progress_percentage:.1f}% of ksh {cause.goal:.2f} goal")

    except ValueError:
        print("Invalid input. Please enter valid numbers.")
    except Exception as e:
        print(f"Error making donation: {e}")

def add_new_cause():
    from models import Cause

    print("\n🎯 Add New Cause:")
    name = input("Enter cause name: ").strip()
    if not name:
        print("Cause name cannot be empty.")
        return

    try:
        goal = float(input("Enter fundraising goal (ksh): "))
        if goal <= 0:
            print("Goal must be greater than zero.")
            return

        new_cause = Cause(name=name, goal=goal)
        new_cause.save()
        print(f"New cause '{name}' created with goal of ksh {goal:.2f}")

    except ValueError:
        print("Invalid goal amount. Please enter a valid number.")
    except Exception as e:
        print(f"Error creating cause: {e}")

def delete_donor():
    from models import Donor

    print("\nDelete DONOR")
    print("-" * 30)

    donors = session.query(Donor).all()
    if not donors:
        print("No donors found.")
        return

    print("Available donors:")
    for donor in donors:
        print(f"[{donor.id}] {donor.name} <{donor.email}> - ksh {donor.total_donated:.2f}")

    try:
        donor_id = int(input("\nEnter Donor ID to delete: "))
        donor = session.query(Donor).get(donor_id)

        if not donor:
            print("Donor not found.")
            return

        donation_count = len(donor.donations)
        print(f"\nWARNING: This will delete:")
        print(f"- Donor: {donor.name}")
        print(f"- {donation_count} donation(s) totaling ksh {donor.total_donated:.2f}")

        confirm = input(f"\nType '{donor.name}' to confirm deletion: ")
        if confirm == donor.name:
            donor.delete()
            print(f"Donor '{donor.name}' and all donations deleted successfully.")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid donor ID.")
    except Exception as e:
        print(f"Error deleting donor: {e}")

def delete_cause():
    from models import Cause

    print("\nDelete CAUSE")
    print("-" * 30)

    causes = session.query(Cause).all()
    if not causes:
        print("No causes found.")
        return

    print("Available causes:")
    for cause in causes:
        print(f"[{cause.id}] {cause.name} - ksh {cause.amount_raised:.2f} / ksh {cause.goal:.2f}")

    try:
        cause_id = int(input("\nEnter Cause ID to delete: "))
        cause = session.query(Cause).get(cause_id)

        if not cause:
            print("Cause not found.")
            return

        donation_count = len(cause.donations)
        print(f"\nWARNING: This will delete:")
        print(f"- Cause: {cause.name}")
        print(f"- {donation_count} donation(s) totaling ksh {cause.amount_raised:.2f}")

        confirm = input(f"\nType '{cause.name}' to confirm deletion: ")
        if confirm == cause.name:
            cause.delete()
            print(f"Cause '{cause.name}' and all donations deleted successfully.")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid cause ID.")
    except Exception as e:
        print(f"Error deleting cause: {e}")

def delete_donation():
    from models import Donation

    print("\nDelete DONATION")
    print("-" * 30)

    donations = session.query(Donation).order_by(Donation.date.desc()).limit(20).all()
    if not donations:
        print("No donations found.")
        return

    print("Recent donations:")
    for donation in donations:
        print(f"[{donation.id}] ksh {donation.amount:.2f} - {donation.donor.name} → {donation.cause.name} ({donation.date.strftime('%Y-%m-%d')})")

    try:
        donation_id = int(input("\nEnter Donation ID to delete: "))
        donation = session.query(Donation).get(donation_id)

        if not donation:
            print("Donation not found.")
            return

        print(f"\nWARNING: This will delete:")
        print(f"- Amount: ksh {donation.amount:.2f}")
        print(f"- From: {donation.donor.name}")
        print(f"- To: {donation.cause.name}")
        print(f"- Date: {donation.date.strftime('%Y-%m-%d %H:%M')}")

        confirm = input("\nType 'delete' to confirm: ")
        if confirm == "delete":
            donation.delete()
            print(f"Donation of ksh {donation.amount:.2f} deleted successfully.")
        else:
            print("Deletion cancelled.")

    except ValueError:
        print("Please enter a valid donation ID.")
    except Exception as e:
        print(f"Error deleting donation: {e}")
