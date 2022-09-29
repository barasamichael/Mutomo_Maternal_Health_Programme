"""empty message

Revision ID: 25139f91ef43
Revises: 
Create Date: 2022-09-25 06:32:42.875187

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25139f91ef43'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('body_part',
    sa.Column('body_part_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('body_part_id')
    )
    op.create_table('checkup_document_type',
    sa.Column('checkup_document_type_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('checkup_document_type_id')
    )
    op.create_table('day',
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=10), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('day_id')
    )
    op.create_table('health_center_type',
    sa.Column('hc_type_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('hc_type_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('health_practitioner_type',
    sa.Column('hp_type_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('hp_type_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('health_speciality_type',
    sa.Column('health_speciality_type_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('health_speciality_type_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('patient',
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('middle_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=8), nullable=False),
    sa.Column('marital_status', sa.String(length=64), nullable=False),
    sa.Column('email_address', sa.String(length=128), nullable=False),
    sa.Column('location_address', sa.String(length=255), nullable=False),
    sa.Column('nationality', sa.String(length=128), nullable=False),
    sa.Column('national_id_no', sa.Integer(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('patient_id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('national_id_no')
    )
    op.create_table('patient_document_type',
    sa.Column('patient_document_type_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('patient_document_type_id')
    )
    op.create_table('role',
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=False),
    sa.Column('default', sa.Boolean(), nullable=True),
    sa.Column('permissions', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('role_id'),
    sa.UniqueConstraint('name')
    )
    op.create_index(op.f('ix_role_default'), 'role', ['default'], unique=False)
    op.create_table('allergy',
    sa.Column('allergy_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('cause', sa.Text(), nullable=False),
    sa.Column('remedy', sa.Text(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('allergy_id')
    )
    op.create_table('family_history',
    sa.Column('family_history_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('family_history_id')
    )
    op.create_table('health_center',
    sa.Column('health_center_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('email_address', sa.String(length=128), nullable=False),
    sa.Column('location_address', sa.String(length=255), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('x_coordinate', sa.Float(), nullable=False),
    sa.Column('y_coordinate', sa.Float(), nullable=False),
    sa.Column('z_coordinate', sa.Float(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('hc_type_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['hc_type_id'], ['health_center_type.hc_type_id'], ),
    sa.PrimaryKeyConstraint('health_center_id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('title')
    )
    op.create_table('health_specialist',
    sa.Column('health_specialist_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('middle_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('gender', sa.String(length=8), nullable=False),
    sa.Column('email_address', sa.String(length=128), nullable=False),
    sa.Column('location_address', sa.String(length=255), nullable=False),
    sa.Column('nationality', sa.String(length=128), nullable=False),
    sa.Column('national_id_no', sa.Integer(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('practitioner_id', sa.Integer(), nullable=False),
    sa.Column('health_center', sa.String(length=255), nullable=False),
    sa.Column('health_speciality_type_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['health_speciality_type_id'], ['health_speciality_type.health_speciality_type_id'], ),
    sa.PrimaryKeyConstraint('health_specialist_id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('national_id_no')
    )
    op.create_table('medication_history',
    sa.Column('medication_history_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('remedy', sa.String(length=255), nullable=False),
    sa.Column('dosage', sa.String(), nullable=False),
    sa.Column('frequency', sa.String(length=128), nullable=False),
    sa.Column('start_date', sa.String(length=64), nullable=False),
    sa.Column('administration', sa.String(length=255), nullable=False),
    sa.Column('nature', sa.String(length=255), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('medication_history_id')
    )
    op.create_table('miscarriage',
    sa.Column('complication_id', sa.Integer(), nullable=False),
    sa.Column('trimester', sa.Integer(), nullable=False),
    sa.Column('cause', sa.Text(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('complication_id')
    )
    op.create_table('next_of_kin',
    sa.Column('next_of_kin_id', sa.Integer(), nullable=False),
    sa.Column('relationship', sa.String(length=12), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('middle_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('phone_no', sa.String(length=16), nullable=False),
    sa.Column('gender', sa.String(length=8), nullable=False),
    sa.Column('location_address', sa.String(length=255), nullable=False),
    sa.Column('id_no', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('next_of_kin_id')
    )
    op.create_table('patient_document',
    sa.Column('patient_document_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('patient_document_type_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_document_type_id'], ['patient_document_type.patient_document_type_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('patient_document_id')
    )
    op.create_table('patient_phone_no',
    sa.Column('patient_phone_no_id', sa.Integer(), nullable=False),
    sa.Column('contact', sa.String(length=16), nullable=False),
    sa.Column('emergency', sa.Boolean(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('patient_phone_no_id')
    )
    op.create_table('pregnancy',
    sa.Column('pregnancy_id', sa.Integer(), nullable=False),
    sa.Column('conception_date', sa.Integer(), nullable=False),
    sa.Column('due_date', sa.Date(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('pregnancy_id')
    )
    op.create_table('social_history',
    sa.Column('social_history_id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('social_history_id')
    )
    op.create_table('surgery',
    sa.Column('surgery_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('status', sa.String(length=32), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=True),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('body_part_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['body_part_id'], ['body_part.body_part_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('surgery_id')
    )
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('middle_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=8), nullable=False),
    sa.Column('email_address', sa.String(length=128), nullable=False),
    sa.Column('location_address', sa.String(length=255), nullable=False),
    sa.Column('nationality', sa.String(length=128), nullable=False),
    sa.Column('id_no', sa.Integer(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('confirmed', sa.Boolean(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.Column('role_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('id_no')
    )
    op.create_table('allergy_symptom',
    sa.Column('allergy_symptom_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('allergy_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['allergy_id'], ['allergy.allergy_id'], ),
    sa.PrimaryKeyConstraint('allergy_symptom_id')
    )
    op.create_table('child',
    sa.Column('child_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('middle_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('pregnancy_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['pregnancy_id'], ['pregnancy.pregnancy_id'], ),
    sa.PrimaryKeyConstraint('child_id')
    )
    op.create_table('complication',
    sa.Column('complication_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('pregnancy_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pregnancy_id'], ['pregnancy.pregnancy_id'], ),
    sa.PrimaryKeyConstraint('complication_id')
    )
    op.create_table('hc_contact',
    sa.Column('hc_contact_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(), nullable=False),
    sa.Column('emergency', sa.Boolean(), nullable=True),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('health_center_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['health_center_id'], ['health_center.health_center_id'], ),
    sa.PrimaryKeyConstraint('hc_contact_id')
    )
    op.create_table('health_center_department',
    sa.Column('hc_department_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('health_center_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['health_center_id'], ['health_center.health_center_id'], ),
    sa.PrimaryKeyConstraint('hc_department_id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('patient_specialist_assignment',
    sa.Column('ps_assignment_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('health_specialist_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['health_specialist_id'], ['health_specialist.health_specialist_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('ps_assignment_id')
    )
    op.create_table('department_schedule',
    sa.Column('department_schedule_id', sa.Integer(), nullable=False),
    sa.Column('hc_department_id', sa.Integer(), nullable=False),
    sa.Column('day_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['day_id'], ['day.day_id'], ),
    sa.ForeignKeyConstraint(['hc_department_id'], ['health_center_department.hc_department_id'], ),
    sa.PrimaryKeyConstraint('department_schedule_id')
    )
    op.create_table('department_service',
    sa.Column('department_service_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('hc_department_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['hc_department_id'], ['health_center_department.hc_department_id'], ),
    sa.PrimaryKeyConstraint('department_service_id')
    )
    op.create_table('health_practitioner',
    sa.Column('health_practitioner_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=128), nullable=False),
    sa.Column('middle_name', sa.String(length=128), nullable=True),
    sa.Column('last_name', sa.String(length=128), nullable=True),
    sa.Column('date_of_birth', sa.Date(), nullable=False),
    sa.Column('gender', sa.String(length=8), nullable=False),
    sa.Column('email_address', sa.String(length=128), nullable=False),
    sa.Column('location_address', sa.String(length=255), nullable=False),
    sa.Column('nationality', sa.String(length=128), nullable=False),
    sa.Column('national_id_no', sa.Integer(), nullable=False),
    sa.Column('associated_image', sa.String(length=255), nullable=True),
    sa.Column('practitioner_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.Column('hp_type_id', sa.Integer(), nullable=False),
    sa.Column('department_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['department_id'], ['health_center_department.hc_department_id'], ),
    sa.ForeignKeyConstraint(['hp_type_id'], ['health_practitioner_type.hp_type_id'], ),
    sa.PrimaryKeyConstraint('health_practitioner_id'),
    sa.UniqueConstraint('email_address'),
    sa.UniqueConstraint('national_id_no')
    )
    op.create_table('checkup',
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('health_practitioner_id', sa.Integer(), nullable=False),
    sa.Column('pregnancy_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['health_practitioner_id'], ['health_practitioner.health_practitioner_id'], ),
    sa.ForeignKeyConstraint(['pregnancy_id'], ['pregnancy.pregnancy_id'], ),
    sa.PrimaryKeyConstraint('checkup_id')
    )
    op.create_table('emergency',
    sa.Column('emergency_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('response', sa.Text(), nullable=False),
    sa.Column('patient_id', sa.Integer(), nullable=False),
    sa.Column('health_practitioner_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['health_practitioner_id'], ['health_practitioner.health_practitioner_id'], ),
    sa.ForeignKeyConstraint(['patient_id'], ['patient.patient_id'], ),
    sa.PrimaryKeyConstraint('emergency_id')
    )
    op.create_table('health_practitioner_phone_no',
    sa.Column('hp_phone_no_id', sa.Integer(), nullable=False),
    sa.Column('contact', sa.String(length=16), nullable=False),
    sa.Column('emergency', sa.Boolean(), nullable=False),
    sa.Column('active', sa.Boolean(), nullable=False),
    sa.Column('health_practitioner_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['health_practitioner_id'], ['health_practitioner.health_practitioner_id'], ),
    sa.PrimaryKeyConstraint('hp_phone_no_id')
    )
    op.create_table('service_assignment',
    sa.Column('service_assignment_id', sa.Integer(), nullable=False),
    sa.Column('start_time', sa.DateTime(), nullable=False),
    sa.Column('end_time', sa.DateTime(), nullable=False),
    sa.Column('department_service_id', sa.Integer(), nullable=False),
    sa.Column('department_schedule_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['department_schedule_id'], ['department_schedule.department_schedule_id'], ),
    sa.ForeignKeyConstraint(['department_service_id'], ['department_service.department_service_id'], ),
    sa.PrimaryKeyConstraint('service_assignment_id')
    )
    op.create_table('affirmative',
    sa.Column('affirmative_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['checkup_id'], ['checkup.checkup_id'], ),
    sa.PrimaryKeyConstraint('affirmative_id'),
    sa.UniqueConstraint('description')
    )
    op.create_table('checkup_document',
    sa.Column('checkup_document_id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('checkup_document_type_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['checkup_document_type_id'], ['checkup_document_type.checkup_document_type_id'], ),
    sa.ForeignKeyConstraint(['checkup_id'], ['checkup.checkup_id'], ),
    sa.PrimaryKeyConstraint('checkup_document_id')
    )
    op.create_table('checkup_symptom',
    sa.Column('checkup_symptom_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('body_part_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['body_part_id'], ['body_part.body_part_id'], ),
    sa.ForeignKeyConstraint(['checkup_id'], ['checkup.checkup_id'], ),
    sa.PrimaryKeyConstraint('checkup_symptom_id')
    )
    op.create_table('diagnosis',
    sa.Column('diagnosis_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['checkup_id'], ['checkup.checkup_id'], ),
    sa.PrimaryKeyConstraint('diagnosis_id'),
    sa.UniqueConstraint('description')
    )
    op.create_table('mental_health',
    sa.Column('mental_health_id', sa.Integer(), nullable=False),
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['checkup_id'], ['checkup.checkup_id'], ),
    sa.PrimaryKeyConstraint('mental_health_id')
    )
    op.create_table('recommendation',
    sa.Column('recommendation_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False),
    sa.Column('checkup_id', sa.Integer(), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=True),
    sa.Column('last_updated', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['checkup_id'], ['checkup.checkup_id'], ),
    sa.PrimaryKeyConstraint('recommendation_id'),
    sa.UniqueConstraint('description')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recommendation')
    op.drop_table('mental_health')
    op.drop_table('diagnosis')
    op.drop_table('checkup_symptom')
    op.drop_table('checkup_document')
    op.drop_table('affirmative')
    op.drop_table('service_assignment')
    op.drop_table('health_practitioner_phone_no')
    op.drop_table('emergency')
    op.drop_table('checkup')
    op.drop_table('health_practitioner')
    op.drop_table('department_service')
    op.drop_table('department_schedule')
    op.drop_table('patient_specialist_assignment')
    op.drop_table('health_center_department')
    op.drop_table('hc_contact')
    op.drop_table('complication')
    op.drop_table('child')
    op.drop_table('allergy_symptom')
    op.drop_table('user')
    op.drop_table('surgery')
    op.drop_table('social_history')
    op.drop_table('pregnancy')
    op.drop_table('patient_phone_no')
    op.drop_table('patient_document')
    op.drop_table('next_of_kin')
    op.drop_table('miscarriage')
    op.drop_table('medication_history')
    op.drop_table('health_specialist')
    op.drop_table('health_center')
    op.drop_table('family_history')
    op.drop_table('allergy')
    op.drop_index(op.f('ix_role_default'), table_name='role')
    op.drop_table('role')
    op.drop_table('patient_document_type')
    op.drop_table('patient')
    op.drop_table('health_speciality_type')
    op.drop_table('health_practitioner_type')
    op.drop_table('health_center_type')
    op.drop_table('day')
    op.drop_table('checkup_document_type')
    op.drop_table('body_part')
    # ### end Alembic commands ###
