from django.db import models

class Doctor(models.Model):
    doctor_id = models.AutoField(primary_key=True, db_column="DOCTOR_ID")
    first_name = models.CharField(max_length=64, db_column="DOCTOR_FIRST_NAME")
    last_name = models.CharField(max_length=64, db_column="DOCTOR_LAST_NAME")
    gender = models.CharField(max_length=16, db_column="GENDER")
    country_code = models.IntegerField(db_column="COUNTRY_CODE")
    mobile = models.CharField(max_length=16, db_column="MOBILE")
    email = models.EmailField(max_length=128, db_column="EMAIL")
    specialization = models.CharField(max_length=255, null=True, blank=True, db_column="SPECIALIZATION")
    qualification = models.CharField(max_length=255, null=True, blank=True, db_column="QUALIFICATION")
    mobile_number_verified = models.BooleanField(default=False, db_column="MOBILE_NUMBER_VERIFIED")
    email_verified = models.BooleanField(default=False, db_column="EMAIL_VERIFIED")
    street = models.TextField(null=True, blank=True, db_column="STREET")
    area = models.CharField(max_length=255, null=True, blank=True, db_column="AREA")
    city = models.CharField(max_length=255, null=True, blank=True, db_column="CITY")
    state = models.CharField(max_length=255, null=True, blank=True, db_column="STATE")
    zipcode = models.CharField(max_length=255, null=True, blank=True, db_column="ZIPCODE")
    country = models.CharField(max_length=264, null=True, blank=True, db_column="COUNTRY")
    practice_name = models.CharField(max_length=1024, null=True, blank=True, db_column="PRACTICE_NAME")
    hospital_name = models.CharField(max_length=255, null=True, blank=True, db_column="HOSPITAL_NAME")
    hospital_address = models.CharField(max_length=512, null=True, blank=True, db_column="HOSPITAL_ADDRESS")
    clinic_zipcode = models.CharField(max_length=50, null=True, blank=True, db_column="CLINIC_ZIPCODE")
    birthday = models.DateField(null=True, blank=True, db_column="DOCTOR_BIRTHDAY")
    marriage_anniversary = models.DateField(null=True, blank=True, db_column="DOCTOR_MARRIAGE_ANNIVERSARY")
    list_of_services_offered = models.TextField(null=True, blank=True, db_column="LIST_OF_SERVICES_OFFERED")
    gbp_available = models.BooleanField(default=False, db_column="GBP_AVAILABLE")
    working_hours = models.CharField(max_length=128, null=True, blank=True, db_column="WORKING_HOURS")
    designation = models.CharField(max_length=128, null=True, blank=True, db_column="DESIGNATION")
    professional_experience_years = models.IntegerField(null=True, blank=True, db_column="PROFESSIONAL_EXPERIENCE_YEARS")
    introduction = models.TextField(null=True, blank=True, db_column="INTRODUCTION")
    publications_achievements = models.TextField(null=True, blank=True, db_column="PUBLICATIONS_ACHIEVEMENTS")
    memberships = models.TextField(null=True, blank=True, db_column="MEMBERSHIPS")
    doctor_photo = models.CharField(max_length=255, null=True, blank=True, db_column="DOCTOR_PHOTO")
    departments = models.TextField(null=True, blank=True, db_column="DEPARTMENTS")
    preferred_world_days = models.TextField(null=True, blank=True, db_column="PREFERRED_WORLD_DAYS")
    language_preference = models.TextField(null=True, blank=True, db_column="LANGUAGE_PREFERENCE")
    language_triggers = models.TextField(null=True, blank=True, db_column="LANGUAGE_TRIGGERS")
    is_active = models.BooleanField(default=False, db_column="IS_ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CREATED_AT")
    updated_at = models.DateTimeField(auto_now=True, db_column="UPDATED_AT")
    billing_entity_name = models.CharField(max_length=255, null=True, blank=True, db_column="BILLING_ENTITY_NAME")
    alternate_contact_name = models.CharField(max_length=64, null=True, blank=True, db_column="ALTERNATE_CONTACT_NAME")
    alternate_contact_number = models.CharField(max_length=16, null=True, blank=True, db_column="ALTERNATE_CONTACT_NUMBER")
    mail_verification_token = models.CharField(max_length=512, null=True, blank=True, db_column="MAIL_VERIFIFCATION_TOKEN")
    gst_no = models.CharField(max_length=32, null=True, blank=True, db_column="GST_NO")
    otp = models.CharField(max_length=10, null=True, blank=True, db_column="OTP")
    otp_generated_time = models.DateTimeField(null=True, blank=True, db_column="OTP_GENERATED_TIME")
    password = models.TextField(null=True, blank=True, db_column="PASSWORD")
    username = models.TextField(null=True, blank=True, db_column="USERNAME")

    class Meta:
        db_table = "DOCTOR"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

