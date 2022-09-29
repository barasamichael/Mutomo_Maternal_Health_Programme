import datetime, time, os
from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models import (health_center, health_center_type, health_center_department,
        department_schedule, department_service, patient, patient_document, 
        health_practitioner, health_practitioner_type) 

def add_health_practitioners():
    fake = Faker(locale = 'en_CA')

    departments = health_center_department.query.all()
    practitioner_types = health_practitioner_type.query.all()

    for department in departments:
        print('Generation for {} starting ...\n'.format(department.title))
        count = randint(5, 15)

        for i in range(count):
            Practitioner = health_practitioner(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                middle_name = fake.last_name(),
                email_address = fake.email(),
                national_id_no = randint(43067798, 59393939),
                practitioner_id = randint(430798, 593939),
                nationality = 'Canada',
                location_address = fake.address(),
                department_id = department.hc_department_id,
                hp_type_id = randint(1, len(practitioner_types))
                )
        
            #generate a realistic date
            while True:
                date = fake.date_of_birth()

                if date >= datetime.date(1980, 1, 1) and date <= datetime.date(2007, 12, 12):
                    Practitioner.date_of_birth = date
                    break
        
            #randomly generate gender of user
            random_integer = randint(1, 11)
            Practitioner.gender = "male" if random_integer % 2 == 0 else "female"
        
            #upload user image
            file_directory = os.path.dirname(os.path.abspath(__file__))
            female_directory = os.path.join(file_directory, "static/Image-Repository/female")
            male_directory = os.path.join(file_directory, "static/Image-Repository/male")

            female_images = [image for image in os.listdir(female_directory)]
            male_images = [image for image in os.listdir(male_directory)]
        
            if Practitioner.gender == 'female':
                Practitioner.associated_image = female_images[randint(0, len(female_images) - 1)]

            elif Practitioner.gender == 'male':
                Practitioner.associated_image = male_images[randint(0, len(male_images) - 1)]
        
            db.session.add(Practitioner)
            try:
                db.session.commit()
                print('Practitioner #{} added successfully...'.format(i))
        
            except IntegrityError:
                db.session.rollback()
                print('Registration #{} failed due to Integrity Error'.format(i))
        print('Generation for {} complete with status : done\n'.format(department.title))

    print("Generation of health practitioners complete with status : done")


def add_patient(count = 100):
    """
    Generates patient details and adds them to the database
    Default number of records generated is 100
    """
    fake = Faker(locale = 'en_CA')

    for i in range(count):
        Patient = patient(
                first_name = fake.first_name(),
                last_name = fake.last_name(),
                middle_name = fake.last_name(),
                email_address = fake.email(),
                national_id_no = randint(43067798, 59393939),
                nationality = 'Canada',
                location_address = fake.address()
                )
        #generate a realistic date
        while True:
            date = fake.date_of_birth()

            if date >= datetime.date(1980, 1, 1) and date <= datetime.date(2007, 12, 12):
                Patient.date_of_birth = date
                break

        #marital status
        statuses = ['married', 'single', 'separated', 'widowed', 'divorced']
        Patient.marital_status = statuses[randint(0, len(statuses) - 1)]

        #upload user image
        file_directory = os.path.dirname(os.path.abspath(__file__))
        image_directory = os.path.join(file_directory, "static/Image-Repository/female")

        female_images = [image for image in os.listdir(image_directory)]
        Patient.associated_image = female_images[randint(0, len(female_images) - 1)]

        
        db.session.add(Patient)
        try:
            db.session.commit()
            print('Patient #{} added successfully...'.format(i))
        except IntegrityError:
            db.session.rollback()
            print('Registration #{} failed due to Integrity Error'.format(i))

    print('Registration of {} patients complete with status : done'.format(count))


def add_health_practitioner_types():
    """
    Randomly registers health_practitioner_types
    """
    from .list_of_practitioners import practitioners
    
    for title, description in practitioners.values():

        Practitioner_Type = health_practitioner_type(title = title, description = description)
        db.session.add(Practitioner_Type)

        try:
            db.session.commit()
            print("{} registered successfully.".format(title))

        except IntegrityError:
            db.session.rollback()
            print("Registration of {} failed due to integrity constraints".format(title))

    print("Registration of health practitioner types complete with status : done")


def add_health_center_departments():
    """
    Randomly registers departments for all health centers
    """
    from .list_of_departments import departments
    
    for center in health_center.query.all():
        
        for i in range(1, randint(10, len(departments))):
            Department = health_center_department(
                    title = departments.get(i)[0],
                    description = departments.get(i)[1],
                    health_center_id = center.health_center_id
                    )
            db.session.add(Department)
            
            try:
                db.session.commit()
                print("{} registered successfully...".format(departments.get(i)[0]))
            except IntegrityError:
                db.session.rollback()
                print("Registration failed due to integrity error...")

        print("Registration of departments for '{}' complete". format(center.title))
    print("Registration of departments complete with status : done")


def add_health_centers():
    """
    Extracts health center data from a kml document and appends them to the database
    """
    from pykml import parser
    fake = Faker(locale = 'en_CA')

    #Number of registered health center types
    health_center_types = len(health_center_type.query.all())

    directory = os.path.dirname(os.path.abspath(__file__))
    with open(os.path.join(directory, "templates/hospitals.kml"), 'r') as file:
        root = parser.parse(file).getroot()
        pms = root.findall('.//{http://earth.google.com/kml/2.1}Placemark')

        for pm in pms:
            coordinates = pm.Point.coordinates.text.split(',')

            Health_Center = health_center(
                    title = str(pm.name),
                    email_address = fake.email(),
                    location_address = fake.address() + "\n" + fake.city(),
                    x_coordinate = float(coordinates[0]),
                    y_coordinate = float(coordinates[1]),
                    z_coordinate = float(coordinates[2]),
                    hc_type_id = randint(1, health_center_types)
                    )
            db.session.add(Health_Center)
            try:
                db.session.commit()
                print("{} registered successfully...".format(str(pm.name)))
            except IntegrityError:
                db.session.rollback()
                print("{} Registration Unsuccessful (Integrity Error)...".format(str(pm.name)))
    
    print("Registration of health centers complete with status : done")


def add_health_center_types():
    """
    Automatically registers health center types from a given dictionary
    """

    data = {
            'Tertiary referral hospital, national hospitals' : 'Governed by the National Government',
            'Secondary referral hospital, provincial hospital' : 'Provincial hospital managed by the county government',
            'Primary facilities, district hospitals and equivalent' : 'District hospital and equivalent',
            'Health Centre, Sub-District Hospital, Maternity Centre' : '    Located at the sub county level',
            'Dispensaries and clinics' : 'Managed by the local government and individuals',
            'Community level' : 'Managed by the local community and occasional donors'
            }
    for key, value in data.items():
        Health_Center_Type = health_center_type(title = key, description = value)
        db.session.add(Health_Center_Type)

        try:
            db.session.commit()
            print("{} added successfully...".format(key))
        except IntegrityError:
            db.session.rollback()
            print("Registration of {} failed (Integrity Error)".format(key))
    
    print("Registration of health center types complete with status : done")

def initialize_system():
    print('Initiliazing system...')
    print('Flushing database...')
    db.drop_all()

    print('Creating database...')
    db.create_all()

    print('Generating data...')

    add_health_center_types()
    add_health_centers()
    add_health_center_departments()
    add_health_practitioner_types()
    add_health_practitioners()
    add_patient(2000)

    print('Generation of data complete with status : done')