
from sqlalchemy.orm import sessionmaker
from models import Donor, Cause, Donation, engine

Session = sessionmaker(bind=engine)
session = Session()

session.query(Donation).delete()
session.query(Donor).delete()
session.query(Cause).delete()

d1 = Donor(name="fredrick", email="okothfredrick1992@gmail.com")
d2 = Donor(name="derrick", email="deriickotieno@gmail.com")

c1 = Cause(name="orphanage", goal=5000)
c2 = Cause(name="Red-cross", goal=3000)

don1 = Donation(amount=100, donor=d1, cause=c1)
don2 = Donation(amount=250, donor=d2, cause=c1)
don3 = Donation(amount=150, donor=d1, cause=c2)

session.add_all([d1, d2, c1, c2, don1, don2, don3])
session.commit()
