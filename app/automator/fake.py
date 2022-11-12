import datetime, time, os
from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError

from .. import db
from ..models import (health_center, health_center_type, health_center_department,
        department_schedule, department_service, patient, patient_document, 
        health_practitioner, health_practitioner_type, patient_document_type, social_history,
        miscarriage, medication_history, body_part, surgery, pregnancy) 


def add_social_history():
    from .list_of_social_histories import socials

    patients = patient.query.all()

    for Patient in patients:
        for i in range(randint(1, 5)):
            data = socials[randint(0, len(socials) - 1)]
            Social_History = social_history(
                    title = data[0],
                    description = data[1],
                    patient_id = Patient.patient_id
                    )
            db.session.add(Social_History)
            db.session.commit()
            print('Registration of social history record {patient.first_name} successfull')
    print("Registration of social histories complete with status done")


def add_body_part():
    from .list_of_body_parts import parts
    
    for part in parts:
        Body_Part = body_part(
                title = part[0],
                description = part[1]
                )
        db.session.add(Body_Part)
        db.session.commit()
        print('Registration of body part successfull')
    
    print('Registration of body parts complete with status done...')


def add_surgery():
    from .list_of_surgeries import surgeries

    patients = patient.query.all()
    fake = Faker(locale = 'en_CA')

    for i in range(int(0.4 * len(patients))):
        patient_id = randint(1, len(patients))
        patient_surgeries = surgery.query.filter_by(patient_id = patient_id).all()
        
        #a single patient cannot have more than five surgeries
        if len(patient_surgeries) > 5:
            continue

        #obtain a random surgery
        current_date = datetime.date(1980, 1, 1)
        record = surgeries[randint(0, len(surgeries) - 1)]
        for i in range(1, 5):
            Surgery = surgery(
                    description = record[0],
                    status = record[1],
                    body_part_id = record[2],
                    patient_id = patient_id
                    )
            #ensure dates rhyme
            while True:
                date = fake.date_of_birth()
                if date >= current_date and date <= datetime.date(2007, 12, 12):
                    Surgery.date = date
                    current_date = date
                    break

            db.session.add(Surgery)
            db.session.commit()

            print(f"Surgery record #{i} successfull.")

    print('Registration of surgeries complete with the status doene...')


def add_medication_history():
    from .list_of_medications import medications, sources
    patients = patient.query.all()
    
    for i in range(randint(1, (patients*4))):
        patient_id = randint(1, len(patients))

        medication = medication_history.query.filter_by(patient_id = patient_id).all()
        if len(medication) > 5:
            continue

        medicine = medications[randint(0, len(medications) - 1)]
        Medication = medication_history(
                description = medicine[0],
                remedy = medicine[1],
                dosage = medicine[2],
                frequency = medicine[3],
                administration = medicine[4],
                source = sources[randint(0, len(sources) - 1)],
                patient_id = patient_id
                )
        
        while True:
            date = fake.date_of_birth()
            if date >= datetime.date(1980, 1, 1) and date <= datetime.date(2007, 12, 12):
                Medication.start_date = date
                break
        
        db.session.add(Medication)
        db.session.commit()
        print(f'Registration of medication history record #{i} successfull.')

    print('Registration of medication histories complete with status done...')


def register_miscarriage(count = 20):
    from .list_of_miscarriage_causes import causes
    patients = patient.query.all()
    trimesters = ['First', 'Second']
    
    for i in range(count):
        patient_id = randint(1, len(patients))

        #ensure that we don't have more than one record
        Miscarriage = miscarriage.query.filter_by(patient_id = patient_id).first()
        if Miscarriage:
            continue

        #store our miscarriage record
        Miscarriage = miscarriage(
                cause = causes[randint(0, len(causes) - 1)],
                trimester = trimesters[randint(0, len(trimesters) - 1)],
                patient_id = patient_id 
                )
        db.session.add(Miscarriage)
        db.session.commit()
        print(f'Miscarriage record #{i} done successfully')

    print("Registration of miscarriages complete with status done...")


def register_pregnancy(count = 100):
    fake = Faker(locale = 'en_CA')
    patients = patient.query.all()

    for i in range(count):
        Pregnancy = pregnancy(patient_id = randint(1, len(patients)))
        #generate a realistic date
        while True:
            date = fake.date_of_birth()

            if date >= datetime.date(1980, 1, 1) and date <= datetime.date(2007, 12, 12):
                Pregnancy.conception_date = date
                Pregnancy.due_date = date + datetime.timedelta(hours = 24 * 9 * 30)
                break
        db.session.add(Pregnancy)
        db.session.commit()

        print(f'Registration of pregnancy record #{i} complete')

    print("Registration of pregnancies complete with status done...")


def add_patient_documents():
    patients = patient.query.all()
    document_types = patient_document_type.query.all()

    for Patient in patients:
        for i in range(0, len(document_types) - 1):
            Document = patient_document(
                filename = "basic_document.pdf",
                patient_document_type_id = randint(0, len(document_types) - 1),
                patient_id = Patient.patient_id
                )
            db.session.add(Document)
            db.session.commit()
            print("Registration of patient document complete with status done")

    print("Registration of patient documents complete with status done")


def add_patient_document_types():
    from .list_of_document_types import document_types
    for item in document_types:
        Document_Type = patient_document_type(
                title = item[0],
                description = item[1]
                )
        db.session.add(Document_Type)
        db.session.commit()

        print(f'{item[0]} registered successfully...')
    print('Registration of patient document types complete with status done...')


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
            female_directory = os.path.join(file_directory, "static/Image-Repository/practitioners/female")
            male_directory = os.path.join(file_directory, "static/Image-Repository/practitioners/male")

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
            file_directory = os.path.dirname(os.path.abspath(__file__))
            image_directory = os.path.join(file_directory, "static/Image-Repository/departments")

            department_images = [image for image in os.listdir(image_directory)]
            Department.associated_image = department_images[randint(0, len(department_images) - 1)]
            
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
            file_directory = os.path.dirname(os.path.abspath(__file__))
            image_directory = os.path.join(file_directory, "static/Image-Repository/centers")

            center_images = [image for image in os.listdir(image_directory)]
            Health_Center.associated_image = center_images[randint(0, len(center_images) - 1)]
            
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
