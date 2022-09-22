import flask
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from datetime import datetime

from . import db, login_manager

#register load_user to be called when info about logged in user is required
@login_manager.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


class Permission:
    VISIT = 1
    MEMBER = 2
    GROUP_MEMBER = 4
    VIEW = 8
    REGISTER = 16
    MODERATE = 32
    ADMIN = 64


class role(db.Model):
    __tablename__ = 'role'

    role_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64), nullable = False, unique = True)
    default = db.Column(db.Boolean, default = False, index = True)
    permissions = db.Column(db.Integer)

    #relationships
    users = db.relationship('user', backref = 'role', lazy = 'dynamic')

    def __init__(self, **kwargs):
        super(role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
                'Guest' : [Permission.VISIT],
                'Member' : [Permission.VISIT, Permission.MEMBER],
                'Group Member' : [Permission.VISIT, Permission.GROUP_MEMBER, 
                    Permission.MEMBER],
                'Security Personnel' :[Permission.VISIT, Permission.VIEW],
                'Junior Staff' : [Permission.VISIT, Permission.VIEW, Permission.MEMBER, 
                    Permission.REGISTER],
                'Senior Staff' : [Permission.VISIT, Permission.VIEW, Permission.REGISTER,
                    Permission.MODERATE, Permission.MEMBER],
                'Administrator' : [Permission.VISIT, Permission.VIEW, Permission.REGISTER, 
                    Permission.MODERATE, Permission.ADMIN, Permission.MEMBER]
        }
        
        default_role = 'Guest'

        for r in roles:
            Role = role.query.filter_by(name = r).first()
            if Role is None:
                Role = role(name = r)

            Role.reset_permission()
            for perm in roles[r]:
                Role.add_permission(perm)

            Role.default = (Role.name == default_role)
            db.session.add(Role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permission(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

            
class anonymous_user(AnonymousUserMixin):
    def can(self, permission):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = anonymous_user

class user(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date, default = datetime.utcnow, nullable = False)

    gender = db.Column(db.String(8), default = 'female', nullable = False)
    email_address = db.Column(db.String(128), nullable = False, unique = True)
    location_address = db.Column(db.String(255), nullable = False)
    nationality = db.Column(db.String(128), default = "Kenya", nullable = False)
    id_no = db.Column(db.Integer, nullable = False, unique = True)
    associated_image= db.Column(db.String(255))

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default = False)
    active = db.Column(db.Boolean, default = True)

    #relationships
    role_id = db.Column(db.Integer, db.ForeignKey('role.role_id'))

    def __init__(self,**kwargs):
        super(user, self). __init__(**kwargs)
        if self.role_id is None:
            if self.email_address == flask.current_app.config['FLASKY_ADMIN_EMAIL']:
                Role = role.query.filter_by(name = 'Administrator').first()
                self.role_id = Role.role_id

            if self.role_id is None:
                Role = role.query.filter_by(default = True).first()
                self.role_id = Role.role_id

    def can(self, perm):
        Role = role.query.filter_by(role_id = self.role_id).first()

        return self.role_id is not None and Role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration = 3600):
        s = serializer(flask.current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm' : self.id}).decode('utf-8')

    def confirm(self, token):
        s = serializer(flask.current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False

        if data.get('confirm') != self.id:
            return False

        self.confirmed = True
        db.session.add(self)

        return True




class health_practitioner(db.Model):
    """
    Attends to patients in the health center and is associated 
    with a particular health center department
    """

    __tablename__ = 'health_practitioner'
    health_practitioner_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date, default = datetime.utcnow, nullable = False)

    gender = db.Column(db.String(8), default = 'female', nullable = False)
    email_address = db.Column(db.String(128), nullable = False, unique = True)
    location_address = db.Column(db.String(255), nullable = False)
    nationality = db.Column(db.String(128), default = "Kenya", nullable = False)
    national_id_no = db.Column(db.Integer, nullable = False, unique = True)
    associated_image = db.Column(db.String(255))

    practitioner_id = db.Column(db.Integer, nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    hp_type_id = db.Column(db.Integer, 
            db.ForeignKey('health_practitioner_type.hp_type_id'), nullable = False)
    department_id = db.Column(db.Integer, 
            db.ForeignKey('health_center_department.hc_department_id'), nullable = False)
 
    phone_nos = db.relationship('health_practitioner_phone_no', backref = 'owner', 
            lazy = 'dynamic')
    checkups = db.relationship('checkup', backref = 'practitioner', lazy = 'dynamic')
    emergencies = db.relationship('emergency', backref = 'practitioner', lazy = 'dynamic')

    def __repr__(self):
        return f'<{self.health_practitioner_id}>'


class health_practitioner_phone_no(db.Model):
    """
    Hold a phone number associated with a particular registered health practitioner
    """
    
    __tablename__ = 'health_practitioner_phone_no'
    hp_phone_no_id = db.Column(db.Integer, primary_key = True)
    
    contact = db.Column(db.String(16), nullable = False)
    emergency = db.Column(db.Boolean, default = True, nullable = False)
    active = db.Column(db.Boolean, default = True, nullable = False)

    #relationship
    health_practitioner_id = db.Column(db.Integer, 
            db.ForeignKey('health_practitioner.health_practitioner_id'), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def __repr__(self):
        return f'<{self.health_practitioner_id}>'


class health_practitioner_type(db.Model):
    """
    Gives a short description of what associated health practitioners do
    """

    __tablename__ = 'health_practitioner_type'
    hp_type_id = db.Column(db.Integer, primary_key = True)
    
    title = db.Column(db.String(255), nullable = False, unique = True)
    description = db.Column(db.Text, nullable = False)
 
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    practitioners = db.relationship('health_practitioner', backref = 'type', lazy = 'dynamic')

    def __repr__(self):
        return f'<{self.health_practitioner_id}>'


class hc_contact(db.Model):
    __tablename__ = 'hc_contact'
    hc_contact_id = db.Column(db.Integer, primary_key = True)
    
    description = db.Column(db.String(), nullable = False)
    emergency = db.Column(db.Boolean, default = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    #relationships
    health_center_id = db.Column(db.Integer, db.ForeignKey('health_center.health_center_id'),
            nullable = False)

    def repr(self):
        return f'<{self.hc_contact_id}>'


class patient(db.Model):
    """Contains information of a particular registered patient"""

    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date, default = datetime.utcnow, nullable = False)

    gender = db.Column(db.String(8), default = 'female', nullable = False)
    marital_status = db.Column(db.String(64), default = 'married', nullable = False)
    email_address = db.Column(db.String(128), nullable = False, unique = True)
    location_address = db.Column(db.String(255), nullable = False)
    nationality = db.Column(db.String(128), default = "Kenya", nullable = False)
    national_id_no = db.Column(db.Integer, nullable = False, unique = True)
    associated_image = db.Column(db.String(255))

    #relationships
    pregnancies = db.relationship('pregnancy', backref = 'patient', lazy = 'dynamic')
    emergencies = db.relationship('emergency', backref = 'patient', lazy = 'dynamic')
    allergies = db.relationship('allergy', backref = 'patient', lazy = 'dynamic')
    social_histories = db.relationship('social_history', backref = 'patient', 
            lazy = 'dynamic')
    next_of_kins = db.relationship('next_of_kin', backref = 'patient', lazy = 'dynamic')
    documents = db.relationship('patient_document', backref = 'patient', lazy = 'dynamic')
    specialists = db.relationship('patient_specialist_assignment', backref = 'patient', 
            lazy = 'dynamic')
    miscarriages = db.relationship('miscarriage', backref = 'patient', lazy = 'dynamic')
    medication_histories = db.relationship('medication_history', backref = 'patient', 
            lazy = 'dynamic')

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.patient_id}>'


class patient_specialist_assignment(db.Model):
    """
    Contains details on the assignment of a specialist to a particular patient
    """
    __tablename__ = 'patient_specialist_assignment'
    ps_assignment_id = db.Column(db.Integer, primary_key = True)

    description = db.Column(db.Text, nullable = False)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    health_specialist_id = db.Column(db.Integer, 
            db.ForeignKey('health_specialist.health_specialist_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.ps_assignment_id}>'


class emergency(db.Model):
    """
    Contains details on an emergency for a particular patient
    """
    __tablename__ = 'emergency'
    emergency_id = db.Column(db.Integer, primary_key = True)

    description = db.Column(db.Text, nullable = False)
    response = db.Column(db.Text, nullable = False)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    health_practitioner_id = db.Column(db.Integer, 
            db.ForeignKey('health_practitioner.health_practitioner_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.emergency_id}>'


class patient_document_type(db.Model):
    """
    Contains details on a document type for patients
    """
    __tablename__ = 'patient_document_type'
    patient_document_type_id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)
    
    #relationships
    documents = db.relationship('patient_document', backref = 'document type', 
            lazy = 'dynamic')

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.patient_document_type_id}>'


class patient_document(db.Model):
    """
    Contains the path to a document belonging to a particular patient
    """
    __tablename__ = 'patient_document'
    patient_document_id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(255), nullable = False)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    patient_document_type_id = db.Column(db.Integer, 
            db.ForeignKey('patient_document_type.patient_document_type_id'), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.patient_document_id}>'


class patient_phone_no(db.Model):
    """
    Hold a phone number associated with a particular registered patient
    """
    
    __tablename__ = 'patient_phone_no'
    patient_phone_no_id = db.Column(db.Integer, primary_key = True)
    
    contact = db.Column(db.String(16), nullable = False)
    emergency = db.Column(db.Boolean, default = True, nullable = False)
    active = db.Column(db.Boolean, default = True, nullable = False)

    #relationship
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), 
            nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def __repr__(self):
        return f'<{self.patient_phone_no_id}>'


class health_speciality_type(db.Model):
    """
    Gives a short description of what associated health specialists do
    """

    __tablename__ = 'health_speciality_type'
    health_speciality_type_id = db.Column(db.Integer, primary_key = True)
    
    title = db.Column(db.String(255), nullable = False, unique = True)
    description = db.Column(db.Text, nullable = False)
 
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    specialists = db.relationship('health_specialist', backref = 'type', lazy = 'dynamic')
    
    def __repr__(self):
        return f'<{self.health_speciality_type_id}>'


class health_specialist(db.Model):
    """
    Contains details for a health practitioner attending to special conditions for patient
    inlcusive of personal medical attendance
    """

    __tablename__ = 'health_specialist'
    health_specialist_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    gender = db.Column(db.String(8), default = 'female', nullable = False)
    email_address = db.Column(db.String(128), nullable = False, unique = True)
    location_address = db.Column(db.String(255), nullable = False)
    nationality = db.Column(db.String(128), default = "Kenya", nullable = False)
    national_id_no = db.Column(db.Integer, nullable = False, unique = True)
    associated_image = db.Column(db.String(255))

    practitioner_id = db.Column(db.Integer, nullable = False)
    health_center = db.Column(db.String(255), nullable = False)

    #relationships
    health_speciality_type_id = db.Column(db.Integer, 
        db.ForeignKey('health_speciality_type.health_speciality_type_id'), nullable = False)

    patients = db.relationship('patient_specialist_assignment', backref = 'specialist', 
            lazy = 'dynamic')
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

class next_of_kin(db.Model):
    """
    Contains a next of kin record for a particular patient
    """
    __tablename__ = 'next_of_kin'
    next_of_kin_id = db.Column(db.Integer, primary_key = True)

    relationship = db.Column(db.String(12), nullable = False)
    
    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))

    phone_no = db.Column(db.String(16), nullable = False)
    gender = db.Column(db.String(8), default = 'female', nullable = False)
    location_address = db.Column(db.String(255), nullable = False)
    id_no = db.Column(db.Integer, nullable = False)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.next_of_kin_id}>'


class allergy(db.Model):
    """
    Contains an allergy record for a particular patient
    """
    __tablename__ = 'allergy'
    allergy_id = db.Column(db.Integer, primary_key = True)

    description = db.Column(db.String(255), nullable = False)
    cause = db.Column(db.Text, nullable = False)
    remedy = db.Column(db.Text, nullable = False)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)

    symptoms = db.relationship('allergy_symptom', backref = 'allergy', lazy = 'dynamic')
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.allergy_id}>'


class allergy_symptom(db.Model):
    """
    Contains a symptom for an allergy of a particular patient
    """
    __tablename__ = 'allergy_symptom'

    allergy_symptom_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), nullable = False)

    #relationships
    allergy_id = db.Column(db.Integer, db.ForeignKey('allergy.allergy_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.allergy_symptom_id}>'


class surgery(db.Model):
    """
    Contains surgery records for a particular patient
    """

    __tablename__ = 'surgery'
    surgery_id = db.Column(db.Integer, primary_key = True)

    description = db.Column(db.Text, nullable = False)
    status = db.Column(db.String(32), default = 'major', nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    body_part_id = db.Column(db.Integer, db.ForeignKey('body_part.body_part_id'), 
            nullable = False)

    def __repr__(self):
        return f'<{self.miscarriage_id}>'


class miscarriage(db.Model):
    """
    Contains miscarriage records for a particular patient
    """

    __tablename__ = 'miscarriage'
    complication_id = db.Column(db.Integer, primary_key = True)

    trimester = db.Column(db.Integer, default = 1, nullable = False)
    cause = db.Column(db.Text, nullable = False)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    
    def __repr__(self):
        return f'<{self.miscarriage_id}>'


class family_history(db.Model):
    __tablename__ = 'family_history'
    family_history_id = db.Column(db.Integer, primary_key = True)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)

    def repr(self):
        return f'<{self.hc_contact_id}, {self.description}>'


class social_history(db.Model):
    """
    Contains a social history description for a particular patient
    """

    __tablename__ = 'social_history'
    social_history_id = db.Column(db.Integer, primary_key = True)

    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
     
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def __repr__(self):
        return f'<self.social_history_id>'


class medication_history(db.Model):
    """
    Contains details on a medication history of a particular patient
    """
    __tablename__ = 'medication_history'
    medication_history_id = db.Column(db.Integer, primary_key = True)

    description = db.Column(db.String(255), nullable = False)
    remedy = db.Column(db.String(255), nullable = False)
    dosage = db.Column(db.String(), nullable = False)
    frequency = db.Column(db.String(128), nullable = False)
    start_date = db.Column(db.String(64), nullable = False)
    administration = db.Column(db.String(255), nullable = False)
    nature = db.Column(db.String(255), default = 'prescribed', 
            nullable = False)
    
    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def __repr__(self):
        return f'<{self.medication_history_id}>'


class pregnancy(db.Model):
    """
    Holds data for a patient's pregnancy phase
    """

    __tablename__ = 'pregnancy'
    pregnancy_id = db.Column(db.Integer, primary_key = True)
    
    conception_date = db.Column(db.Integer, nullable = False)
    due_date = db.Column(db.Date, default = datetime.utcnow, nullable = False)
    
    #relationships
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'), nullable = False)
    
    children = db.relationship('child', backref = 'pregnancy', lazy = 'dynamic')
    complications = db.relationship('complication', backref = 'pregnancy', lazy = 'dynamic')
    checkups = db.relationship('checkup', backref = 'pregnancy', lazy = 'dynamic')
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.pregnancy_id}>'


class child(db.Model):
    """
    Contains details on a child related to a particular pregnancy
    """
    __tablename__ = 'child'
    child_id = db.Column(db.Integer, primary_key = True)  

    first_name = db.Column(db.String(128), nullable = False)
    middle_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    date_of_birth = db.Column(db.Date, default = datetime.utcnow, nullable = False)
    
    #relationships
    pregnancy_id = db.Column(db.Integer, db.ForeignKey('pregnancy.pregnancy_id'), 
            nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def __repr__(self):
        return f'<{self.child_id}>'


class complication(db.Model):
    """
    Contains details on complication encountered by the patient during pregnancy
    """
    __tablename__ = 'complication'
    complication_id = db.Column(db.Integer, primary_key = True)

    description = db.Column(db.Text, nullable = False)

    #relationships
    pregnancy_id = db.Column(db.Integer, db.ForeignKey('pregnancy.pregnancy_id'), 
            nullable = False)
    
    def __repr__(self):
        return f'<{self.complication_id}>'



class checkup(db.Model):
    """
    Contains details for the checkup session of a particular patient
    """
    __tablename__ = 'checkup'
    checkup_id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
    
    #relationships
    health_practitioner_id = db.Column(db.Integer, 
        db.ForeignKey('health_practitioner.health_practitioner_id'), nullable = False)
    pregnancy_id = db.Column(db.Integer, db.ForeignKey('pregnancy.pregnancy_id'), 
            nullable = False)
     
    documents = db.relationship('checkup_document', backref = 'checkup', lazy = 'dynamic')
    symptoms = db.relationship('checkup_symptom', backref = 'checkup', lazy = 'dynamic')
    affirmatives = db.relationship('affirmative', backref = 'checkup', lazy = 'dynamic')
    diagnoses = db.relationship('diagnosis', backref = 'checkup', lazy = 'dynamic')
    recommendations = db.relationship('recommendation', backref = 'checkup', lazy = 'dynamic')
    mental_healths = db.relationship('mental_health', backref = 'checkup', lazy = 'dynamic')
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.checkup_id}>'


class body_part(db.Model):
    """
    Contains details on what constitutes a particular body part
    """
    __tablename__ = 'body_part'
    body_part_id = db.Column(db.Integer, primary_key = True)
    
    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.body_part_id}>'


class checkup_symptom(db.Model):
    """
    Contains a symptom noted during the checkup session of a particular patient
    """
    __tablename__ = 'checkup_symptom'

    checkup_symptom_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), nullable = False)

    #relationships
    checkup_id = db.Column(db.Integer, db.ForeignKey('checkup.checkup_id'), nullable = False)
    body_part_id = db.Column(db.Integer, db.ForeignKey('body_part.body_part_id'), 
            nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.checkup_symptom_id}>'


class diagnosis(db.Model):
    """
    Contains diagnosis details by the doctor during a checkup session
    """
    __tablename__ = 'diagnosis'

    diagnosis_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), unique = True, nullable = False)

    #relationships
    checkup_id = db.Column(db.Integer, db.ForeignKey('checkup.checkup_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.diagnosis_id}>'


class affirmative(db.Model):
    """
    Contains affirmation details by the doctor during a checkup session
    """
    __tablename__ = 'affirmative'

    affirmative_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), unique = True, nullable = False)

    #relationships
    checkup_id = db.Column(db.Integer, db.ForeignKey('checkup.checkup_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.affirmative_id}>'


class recommendation(db.Model):
    """
    Contains recommendation details by the doctor during a checkup session
    """
    __tablename__ = 'recommendation'

    recommendation_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(255), unique = True, nullable = False)

    #relationships
    checkup_id = db.Column(db.Integer, db.ForeignKey('checkup.checkup_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    
    def repr(self):
        return f'<{self.recommendation_id}>'


class health_center_type(db.Model):
    """
    Contains details for a particular hospital level
    """
    __tablename__ = 'health_center_type'
    hc_type_id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    #relationships
    health_centers = db.relationship('health_center', backref = 'type', lazy = 'dynamic')
    
    def repr(self):
        return f'<{self.hc_type_id}>'


class health_center(db.Model):
    """
    Contains details for a particular health institution
    """
    __tablename__ = 'health_center'
    health_center_id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    
    email_address = db.Column(db.String(128), nullable = False, unique = True)
    location_address = db.Column(db.String(255), nullable = False)
    active = db.Column(db.Boolean, default = True, nullable = False)
    x_coordinate = db.Column(db.Float, nullable = False)
    y_coordinate = db.Column(db.Float, nullable = False)
    z_coordinate = db.Column(db.Float, nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)
    #relationships
    hc_type_id = db.Column(db.Integer, db.ForeignKey('health_center_type.hc_type_id'), 
            nullable = False)
    
    departments = db.relationship('health_center_department', backref = 'institution', 
            lazy = 'dynamic')
    contacts = db.relationship('hc_contact', backref = 'owner', lazy = 'dynamic')
    
    def repr(self):
        return f'<{self.health_center_id}>'


class health_center_department(db.Model):
    """
    Contains details for a department in a particular health institution
    """
    __tablename__ = 'health_center_department'
    hc_department_id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)

    #relationships
    health_center_id = db.Column(db.Integer, db.ForeignKey('health_center.health_center_id'), 
            nullable = False)
    
    schedules = db.relationship('department_schedule', backref = 'department', 
            lazy = 'dynamic')
    services = db.relationship('department_service', backref = 'department', lazy = 'dynamic') 
    practioners = db.relationship('health_practitioner', backref = 'department', 
            lazy = 'dynamic')
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.hc_contact_id}, {self.description}>'

class day(db.Model):
    """
    Stores a day of the week
    """
    day_id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String(10), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.day_id}>'


class service_assignment(db.Model):
    """
    Joins a particular service with a particular departmental schedule
    """
    __tablename__ = 'service_assignment'
    service_assignment_id = db.Column(db.Integer, primary_key = True)
    
    start_time = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
    end_time = db.Column(db.DateTime, default = datetime.utcnow, nullable = False)
    
    #relationships
    department_service_id = db.Column(db.Integer, 
            db.ForeignKey('department_service.department_service_id'), nullable = False)
    department_schedule_id = db.Column(db.Integer, 
            db.ForeignKey('department_schedule.department_schedule_id'), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.service_assignment_id}>'


class department_service(db.Model):
    """
    Contains service details for a particular department
    """
    __tablename__ = 'department_service'
    department_service_id = db.Column(db.Integer, primary_key = True)
    
    #relationships
    hc_department_id = db.Column(db.Integer, db.ForeignKey('health_center_department.hc_department_id'), 
            nullable = False)

    assignments = db.relationship('service_assignment', backref = 'checkup', 
            lazy = 'dynamic')
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.department_service_id}>'


class department_schedule(db.Model):
    """
    Contains schedule details for a particular department
    """
    __tablename__ = 'department_schedule'
    department_schedule_id = db.Column(db.Integer, primary_key = True)
    
    #relationships
    hc_department_id = db.Column(db.Integer, db.ForeignKey('health_center_department.hc_department_id'), 
            nullable = False)
    day_id = db.Column(db.Integer, db.ForeignKey('day.day_id'), nullable = False)

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.department_schedule_id}>'


class mental_health(db.Model):
    """
    Contains mental health details taken during a checkup session
    """
    __tablename__ = 'mental_health'
    mental_health_id = db.Column(db.Integer, primary_key = True)

    #relationships
    checkup_id = db.Column(db.Integer, db.ForeignKey('checkup.checkup_id'), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.mental_health}>'


class checkup_document_type(db.Model):
    """
    Contains details on a document type supported by a particular institution
    """
    __tablename__ = 'checkup_document_type'
    checkup_document_type_id = db.Column(db.Integer, primary_key = True)

    title = db.Column(db.String(255), nullable = False)
    description = db.Column(db.Text, nullable = False)
    
    #relationships
    documents = db.relationship('checkup_document', backref = 'document type', 
            lazy = 'dynamic')

    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.checkup_document_type_id}>'


class checkup_document(db.Model):
    """
    Contains the path to a document related to a particular checkup session
    """
    __tablename__ = 'checkup_document'
    checkup_document_id = db.Column(db.Integer, primary_key = True)
    filename = db.Column(db.String(255), nullable = False)

    #relationships
    checkup_id = db.Column(db.Integer, db.ForeignKey('checkup.checkup_id'), nullable = False)
    checkup_document_type_id = db.Column(db.Integer, 
            db.ForeignKey('checkup_document_type.checkup_document_type_id'), nullable = False)
    
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    last_updated = db.Column(db.DateTime, default = datetime.utcnow,
            onupdate = datetime.utcnow)

    def repr(self):
        return f'<{self.checkup_document_id}>'
