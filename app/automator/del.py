import datetime,time, glob
from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError

from . import db
from .models import (user, member, occupation, document_type, month, loan_type, 
        registration_fee, employer, employment, monthly_deposit, phone_number, review,
        branch, event, event_image, loan_overdue, loan_overdue_payment, loan)


def add_member(count = 99):
    """
    add_member(count = 99)
        Populates details on member and adds them into the database
        count is the number of members to generate
    """

    fake = Faker(locale = 'en_CA')

    for i in range(count):
        Member = member()

        #generate profile details
        Member.first_name = fake.first_name()
        Member.middle_name = fake.last_name()
        Member.last_name = fake.last_name()
        Member.email_address = fake.email()
        Member.location_address = fake.address() + "\n" + fake.city()
        Member.id_no = randint(500306778, 500393939)

        #generate a realistic date
        while True:
            date = fake.date_of_birth()

            if date >= datetime.date(1976, 1, 1) and date <= datetime.date(1997, 12, 12):
                Member.date_of_birth = date
                break

        #randomly generate gender of user
        random_integer = randint(1, 11)
        Member.gender = "male" if random_integer % 2 == 0 else "female"

        Member.nationality = "Canada"
        Member.status = "activated"
        
        #save to the database
        db.session.add(Member)
        try:
            db.session.commit()
            print(f"Entry #{i} successful...")
            i += 1
        except IntegrityError:
            db.session.rollback()

    print("member profile generation complete with status : done!")



def add_user(count = 34):
    """
    add_user(count)
        Populates details on user and adds them into the database
        count is the number of users to generate

    """

    fake = Faker(locale = 'en_CA')

    for i in range(count):
        User = user()

        #generate profile
        User.first_name = fake.first_name()
        User.middle_name = fake.last_name()
        User.last_name = fake.last_name()
        User.email_address = fake.email()
        User.location_address = fake.address() + "\n" + fake.city()
        User.id_no = randint(500306778, 500393939)

        #generate a realistic date
        while True:
            date = fake.date_of_birth()
        
            if date >= datetime.date(1976, 1, 1) and date <= datetime.date(1997, 12, 12):
                User.date_of_birth = date
                break

        #randomly generate gender of user
        random_integer = randint(1, 11)
        User.gender = "male" if random_integer % 2 == 0 else "female"
        
        User.nationality = "Canada"
        User.password = "password"

        #save to the database
        db.session.add(User)
        try:
            db.session.commit()
            print(f"Entry #{i} successful...")
            i += 1
        except IntegrityError:
            db.session.rollback()
    
    print("user profile generation complete with status : done!")


def add_occupation(count = 99):
    """
    add_occupation(count)
        Generates {count} occupations and adds them to database
        count is the number of occupations to generate
    """

    fake = Faker(locale = 'en_CA')

    for i in range(count):
        Occupation = occupation(description = fake.job())
        
        db.session.add(Occupation)
        try:
            db.session.commit()
            print(f"Entry #{i} successful...")
            i += 1
        except IntegrityError:
            db.session.rollback()

    print("occupation generation complete with status : done!")


def add_document_type():
    """Registers document types populated from a list onto the database"""

    types = ['Passport', 'National ID Card', 'Military ID Card', 'Birth Certificate', 
            'Driver License']

    for i in types:
        Document_Type = document_type(description = i)

        db.session.add(Document_Type)

        try:
            db.session.commit()
            print(f"Entry #{i} successful...")
            i += 1

        except:
            db.session.rollback()

    print("generation of document types complete with status : done!")


def add_month(count = 8):
    """Generates months records to be used for monthly deposits"""

    #by default starting month is current month
    current_month = int(time.strftime("%m"))

    for i in range(count):
        t = (int(time.strftime("%Y")), current_month, 31, 10, 39, 45, 1, 48, 0)
        t = time.mktime(t)
        Month = month(
                description = time.strftime("%B %Y", (time.localtime((t))))
                )
        
        current_month += 1 #add one month
        db.session.add(Month)
        try:
            db.session.commit()
            print("Entry %r added..." %time.strftime("%B %Y", (time.localtime((t)))))
        except IntegrityError:
            db.session.rollback()

    print("generation of months complete with status : done!")


def add_loan_type():
    """Generates loan types and adds them to the database"""

    types = [
            {
                'description' : 'Individual Loan',
                'rate' : 1.2,
                'max_period' : 3,
                'multiplier' : 3,
                'overdue_penalty' : 10
            },
            {
                'description' : 'Group Member Loan',
                'rate' : 1,
                'max_period' : 4,
                'multiplier' : 4,
                'overdue_penalty' : 10
            },
            {
                'description' : 'Group Loan',
                'rate' : 0.8,
                'max_period' : 5,
                'multiplier' : 3,
                'overdue_penalty' : 10
            }
    ] 
    for item in types:
        Loan_Type = loan_type(
                description = item.get('description'),
                max_period = item.get("max_period"),
                multiplier = item.get("multiplier"),
                overdue_penalty = item.get("overdue_penalty"),
                rate = item.get("rate")
                )
        db.session.add(Loan_Type)

        try:
            db.session.commit()
            print(f"Entry {item.get('description')} added ...")
        except:
            db.session.rollback()
    
    print('generation of loan types complete with status : done!')


def add_registration_fee():
    members = member.query.all()

    for item in members:
        #by default member hasn't paid any registration fees
        total = 0

        fee = registration_fee.query.filter_by(member_id = item.member_id).first()
        if fee:
            total = fee.amount

        while total <= 1900:
            random_integer = randint(1, 12)
            Fee = registration_fee(
                    member_id = item.member_id,
                    amount = random_integer * 100
                    )
            
            db.session.add(Fee)
            try:
                db.session.commit()
                total += random_integer * 100
                print(f"Entry for Member ID {item.member_id} successful...")
            except:
                db.session.rollback()
    print("Generation of member registration fee records complete with status : done!")


def add_employer(count = 50):
    fake = Faker(locale = 'en_CA')

    for i in range(count):
        Employer = employer(
                name = fake.company(),
                location_address = fake.address() + "\n" + fake.city(),
                email_address = fake.email(),
                phone_no = fake.phone_number()
                )
        db.session.add(Employer)
        
        try:
            db.session.commit()
            print(f"Entry #{i + 1} successful...")
            count += 1
        except IntegrityError:
            db.session.rollback()

    print('generated employer records with status : done!')


def add_employment():
    members = member.query.all()

    for item in members:
        Employment = employment(
                member_id = item.member_id,
                occupation_id = randint(1, 99),
                employer_id = randint(1, 50)
                )
        db.session.add(Employment)
        try:
            db.session.commit()
            print(f"Entry for member ID {item.member_id} added ...")
        
        except IntegrityError:
            db.session.rollback()

    print("generated employment records with status : done!")


def add_monthly_deposit():
    members = member.query.all()
    
    t = time.mktime((int(time.strftime("%Y")), int(time.strftime("%m")), 
                31, 10, 39, 45, 1, 48, 0))
    description = time.strftime("%B %Y", (time.localtime((t))))
    Month = month.query.filter_by(description = description).first()

    for item in members:
        total = 0
        while total <= 7000:
            random_amount = randint(1, 50)
            deposit = monthly_deposit(
                    amount = random_amount * 100,
                    member_id = item.member_id,
                    month_id = Month.month_id
                    )
            db.session.add(deposit)
            db.session.commit()
            total += random_amount * 100
            print(f"Entry for member {item.member_id} successful...")

    print('generation of monthly deposits completed with status : done!')


def add_user_image():
    users = user.query.all()

    male_images = [i.split('/')[2] for i in glob.glob("Image-Repository/male/*.jpeg")]
    female_images = [i.split('/')[2] for i in glob.glob("Image-Repository/female/*.jpeg")]
    
    for item in users:
        if item.gender == "male":
            item.associated_image = male_images[randint(1, len(male_images) - 1)]
        else:
            item.associated_image = female_images[randint(1, len(female_images) - 1)]

        db.session.add(item)
        db.session.commit()
        print(f"Profile image for user ID {item.id} successful...")

    print("Generation of user profile images complete with status : done!")


def add_member_image():
    members = member.query.all()

    male_images = [i.split('/')[2] for i in glob.glob("Image-Repository/male/*.jpeg")]
    female_images = [i.split('/')[2] for i in glob.glob("Image-Repository/female/*.jpeg")]
    
    for item in members:
        if item.gender == "male":
            item.associated_image = male_images[randint(1, len(male_images) - 1)]
        else:
            item.associated_image = female_images[randint(1, len(female_images) - 1)]

        db.session.add(item)
        db.session.commit()
        print(f"Profile image for member ID {item.member_id} successful...")

    print("Generation of member profile images complete with status : done!")


def add_contact():
    members = member.query.all()

    for item in members:
        phone_no = phone_number(
                member_id = item.member_id,
                phone_no = "07" + str(randint(10000000, 99999999))
                )
        db.session.add(phone_no)
        
        try:
            db.session.commit()
            print(f"Entry for member ID {item.member_id} successful...")

        except IntegrityError:
            db.session.rollback()
    
    print("Generation of member phone numbers complete with status : done!")

def add_review():
    members = {
            34 : 
            """I have gained financial stability, thanks to the low interest rate loans 
            offered by the organization. All I can say is 'asante'.""", 
            78 : 
            """Being a member has benefited me greatly. I have been able to 
            establish my self financially. Nevertheless, I have been able to invest in 
            real estate, thanks to this organization.""", 
            77 : 
            """
            Top notch staff, reputable hospitality alongside affordable financial aids is 
            all I needed to attain financial growth. To all non-members, I urge you to 
            take a step towards growth and development by becoming a member.
            """
            }

    for key in members.keys():
        Review = review(
                member_id = key,
                description = members.get(key)
                )
        db.session.add(Review)
        db.session.commit()
        print(f"Review from member ID {key} successful...")

    print("Generation of member review complete with status : done!")


def add_branch(count = 5):
    fake = Faker(locale = 'en_CA')

    for i in range(count):
        Branch = branch(
                town = fake.city(),
                location_address = fake.address(),
                email_address = fake.email(),
                phone_no = fake.phone_number()
                )
        db.session.add(Branch)
        try:
            db.session.commit()
            print(f'Branch #{i} complete with status : done!')
        except:
            db.session.rollback()

    print('Generation of branches complete with status : done!')


def add_loan():
    members = member.query.filter_by().all()
    for item in members:
        Loan = loan(
                loan_type = 1,
                amount = randint(5, 10) * 1000,
                member_id = item.member_id
                )
        db.session.add(Loan)
        db.session.commit()
        print(f'Loan for member ID {item.member_id} acquired successfully...')
    print('Generation of loans complete with status : done!')


def add_loan_overdue(count = 30):
    t = time.mktime((int(time.strftime("%Y")), int(time.strftime("%m")),
                31, 10, 39, 45, 1, 48, 0))
    description = time.strftime("%B %Y", (time.localtime((t))))
    
    for i in range(count):
        loan_id = randint(1, 100)
        Loan = loan.query.filter_by(loan_id = loan_id).first()
        Loan_Overdue = loan_overdue(
                amount = ((10/100) * Loan.amount),
                loan_id = loan_id,
                month = description
                )
        db.session.add(Loan_Overdue)
        db.session.commit()
        print(f"Entry #{i} completed successfully...")
    print("Generation of loan overdue records complete with status : done!")


def initiate_all():
    db.drop_all()
    db.create_all()

    add_member()
    add_user()
    add_document_type()
    add_contact()
    add_user_image()
    add_member_image()
    add_month()
    add_monthly_deposit()
    add_registration_fee()
    add_loan_type()
    add_occupation()
    add_employer()
    add_employment()
    add_review()
    add_branch()
    add_loan()
