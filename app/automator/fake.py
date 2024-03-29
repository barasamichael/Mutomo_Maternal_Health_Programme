import datetime, time, os
from faker import Faker
from random import randint
from sqlalchemy.exc import IntegrityError
from datetime import datetime, time
from .. import db
from ..models import (health_center, health_center_type, health_center_department,
        department_schedule, service, patient, patient_document, checkup, 
        health_practitioner, health_practitioner_type, patient_document_type, social_history,
        miscarriage, medication_history, body_part, surgery, pregnancy, family_history,
        allergy, allergy_symptom, next_of_kin, patient_phone_no, checkup_symptom,
        recommendation, day, service, service_assignment)


def add_service_assignment():
    services = service.query.all()

    for schedule in department_schedule.query.all():
        for i in range(randint(len(services) // 3, len(services) - 1)):
            Assignment = service_assignment(
                    department_schedule_id = schedule.department_schedule_id,
                    service_id = randint(0, len(services) - 1) 
                    )
            db.session.add(Assignment)
            db.session.commit()
            print("Assignment of service successfull...")
        print("Assignment of services for schedule id {schedule.department_schedule_id} complete with status done...")
    print("Generation of service assignment records complete with status done...")


def add_schedule():
    departments = health_center_department.query.all()
    days = day.query.all()
    times = [[time(9, 15), time(3, 15)], [time(10, 15), time(5, 15)]]
    
    for department in departments:
        for day_item in days:
            for item in times:
                Schedule = department_schedule(
                    start_time = datetime.combine(datetime.today(), item[0]),
                    end_time = datetime.combine(datetime.today(), item[1]),
                    day_id = day_item.day_id,
                    hc_department_id = department.hc_department_id
                    )
                db.session.add(Schedule)
                db.session.commit()
                print("Addition of schedule successfull...")
    print("Generation of schedules complete with status done...")


def add_service():
    from .list_of_services import services

    for item in services:
        Service = service(title = item[0], description = item[1])
        db.session.add(Service)
        db.session.commit()
        print("Addition of service complete with status done...")
    print("Generation of services complete with status done...")


def add_day():
    days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    for item in days:
        Day = day(description = item)
        db.session.add(Day)
        db.session.commit()
        print(f"{item} added successfully...")
    print("Generation of days complete with status done...")


def add_checkup_recommendation():
    from .list_of_recommendations import recommendations
    checkups = checkup.query.all()
    for Checkup in checkups:
        for i in range(randint(4, 7)):
            Recommendation = recommendation(
                description = recommendations[randint(0, len(recommendations) - 1)],
                checkup_id = Checkup.checkup_id
                )
            db.session.add(Recommendation)
            print(f"Addition of checkup recommendation {i} successfull...") 
    db.session.commit()
    print("Addition of checkup symptoms complete with status done....")


def add_checkup_symptom():
    from .list_of_checkup_symptoms import symptoms

    checkups = checkup.query.all()
    parts = body_part.query.all()

    for Checkup in checkups:
        Symptom = checkup_symptom(
            description = symptoms[randint(0, len(symptoms) - 1)],
            checkup_id = Checkup.checkup_id,
            body_part_id = parts[randint(0, len(parts) - 1)].body_part_id
            )
        db.session.add(Symptom)
        print("Addition of checkup symptom successfull...")
    
    db.session.commit()
    print("Addition of checkup symptoms complete with status done...")


def add_phone_number():
    patients = patient.query.all()

    for Patient in patients:
        for i in range(randint(1, 3)):
            # determine whether it is an emergency or not
            emergency = True
            if (randint(0, 1) == 0):
                emergency = False

            # save contact
            Phone_No = patient_phone_no(
                contact = "+254" + str(randint(700000000, 799999999)),
                emergency = emergency,
                patient_id = Patient.patient_id
                )
            db.session.add(Phone_No)
            db.session.commit()
            print("Addition of phone number successfull...")
    print("Generation of patient phone numbers complete with status done...")


def add_next_of_kin():
    from .list_of_kins import kins
    
    fake = Faker(locale = 'en_CA')
    
    patients = patient.query.all()
    for Patient in patients:
        for i in range(randint(2, 5)):
            index = randint(0, 1)
            Next_Of_Kin = next_of_kin(
                    first_name = fake.first_name(),
                    middle_name = fake.last_name(),
                    last_name = fake.last_name(),
                    relationship = kins[index][1][randint(0, len(kins[index][1]) - 1)],
                    gender = kins[index][0],
                    location_address = fake.address(),
                    phone_no = "+254" + str(randint(700000000, 799999999)),
                    id_no = randint(7984884, 9099998),
                    patient_id = Patient.patient_id
                    )
            db.session.add(Next_Of_Kin)
            db.session.commit()

            print("Next of kin added successfully...")
    print("Generation of next of kin records complete with status done...")


def add_allergy():
    from .list_of_allergies import allergies

    patients = patient.query.all()

    for Patient in patients:
        for i in range(randint(0, 2)):
            index = randint(0, len(allergies) - 1)
            Allergy = allergy(
                    description = allergies[index][0], 
                    cause = allergies[index][1],
                    remedy = allergies[index][2], 
                    patient_id = Patient.patient_id
                    )
            db.session.add(Allergy)
            db.session.commit()
            print("Allergy record added successfully...")

            Allergy = allergy.query.order_by(allergy.allergy_id.desc()).first()
            # generate symptoms
            for i in range(randint(len(allergies[index][3]) // 3, len(allergies[index][3]))):
                symptom = allergy_symptom(
                        description = allergies[index][3][randint(0, len(allergies[index][3]) - 1)],
                        allergy_id = Allergy.allergy_id
                        )
                db.session.add(symptom)

            db.session.commit()
            print("Allergy symptoms registered successfully...")
    print("Generation of allergy records complete with exit status done....")


def add_family_history():
    from .list_of_family_histories import members, histories

    patients = patient.query.all()

    for Patient in patients:
        for i in range(randint(0, 3)):
            # let us populate the description for a disease
            description = ""
            for i in range(randint((len(members) - 1) // 3, len(members) - 1)):
               value = members[randint(0, len(members) - 1)]
               if value not in description:
                   description += ", " + value

            # save the data in the database
            Family_History = family_history(
                    title = histories[randint(0, len(histories) - 1)],
                    description = description,
                    patient_id = Patient.patient_id
                    )
            db.session.add(Family_History)
            db.session.commit()

def add_social_history():
    from .list_of_social_histories import socials

    patients = patient.query.all()

    for Patient in patients:
        for i in range(randint(0, 3)):
            # save the data in the database
            social_index = randint(0, len(socials) - 1)
            Social_History = social_history(
                    title = socials[social_index][0],
                    description = socials[social_index][1][randint(0, len(socials[social_index][1]) - 1)],
                    patient_id = Patient.patient_id
                    )
            db.session.add(Social_History)
            db.session.commit()
            print(f'Registration of social history record {Patient.first_name} successfull')
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

    fake = Faker(locale = 'en_CA')
    for Patient in patients:
        medication = medication_history.query.filter_by(patient_id = Patient.patient_id).all()
        if len(medication) > 15:
            continue
        
        for i in range(7, 15):
            
            medicine = medications[randint(0, len(medications) - 1)]
            Medication = medication_history(
                    description = medicine[0],
                    remedy = medicine[1],
                    dosage = medicine[2],
                    frequency = medicine[3],
                    administration = medicine[4],
                    nature = medicine[5],
                    source = sources[randint(0, len(sources) - 1)],
                    patient_id = Patient.patient_id
                    )
        
            while True:
                date = fake.date_of_birth()
                if date >= datetime.date(2010, 1, 1) and date <= datetime.date(2022, 12, 12):
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

def add_checkup():
    pregnancies = pregnancy.query.all()
    print(pregnancies)

    for Pregnancy in pregnancies:
        practitioners = health_practitioner.query.all()
        practitioner = practitioners[randint(1, len(practitioners) - 1)]

        date = Pregnancy.conception_date
        for i in range(randint(1, 8)):
            session = checkup(
                    pregnancy_id = Pregnancy.pregnancy_id,
                    health_practitioner_id = practitioner.health_practitioner_id,
                    )

            #generate a realistic date
            date = date + datetime.timedelta(hours = 24 * randint(20, 30))
            if date > Pregnancy.due_date:
                break
            session.date = date
            
            db.session.add(session)
            db.session.commit()
            print(f"Session {i} for pregnancy ID {Pregnancy.pregnancy_id} added successfully...")
    
    print("Registration of checkup sessions complete with status done...")


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

    add_checkup_recommendation()
    add_checkup_symptom()
    add_phone_number()
    add_next_of_kin()
    add_body_part()
    add_patient_documents()
    add_patient_document_types()
    add_health_center_types()
    add_health_centers()
    add_health_center_departments()
    add_health_practitioner_types()
    add_health_practitioners()
    add_patient(2000)
    add_medication_history()
    register_pregnancy(1000)
    add_checkup()
    register_miscarriage(100)
    add_surgery()
    add_family_history()
    add_social_history()
    add_allergy()
    
    print('Generation of data complete with status : done')
