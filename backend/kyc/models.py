from django.db import models
from django.utils import timezone


class KYCApplication(models.Model):

    # ── STATUS CHOICES ──
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('more_info', 'More Info Required'),
    ]

    ID_TYPE_CHOICES = [
        ('passport', 'Passport'),
        ('nric', 'NRIC / National ID'),
        ('driving_license', "Driver's License"),
        ('fin', 'FIN (Foreign Identification Number)'),
    ]

    EMPLOYMENT_CHOICES = [
        ('employed', 'Employed'),
        ('self_employed', 'Self-Employed'),
        ('business_owner', 'Business Owner'),
        ('student', 'Student'),
        ('retired', 'Retired'),
        ('unemployed', 'Unemployed'),
    ]

    INCOME_CHOICES = [
        ('below_25k', 'Below $25,000'),
        ('25k_50k', '$25,000 – $50,000'),
        ('50k_100k', '$50,000 – $100,000'),
        ('100k_200k', '$100,000 – $200,000'),
        ('above_200k', 'Above $200,000'),
        ('prefer_not', 'Prefer not to say'),
    ]

    PURPOSE_CHOICES = [
        ('personal', 'Personal Payments'),
        ('travel', 'Travel & Tourism'),
        ('business', 'Business Payments'),
        ('remittance', 'Remittance / Sending Money'),
        ('ecommerce', 'E-Commerce'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]

    COUNTRY_CHOICES = [
        ('SG', 'Singapore'),
        ('MY', 'Malaysia'),
        ('ID', 'Indonesia'),
        ('TH', 'Thailand'),
        ('PH', 'Philippines'),
        ('VN', 'Vietnam'),
        ('CN', 'China'),
        ('IN', 'India'),
        ('AU', 'Australia'),
        ('GB', 'United Kingdom'),
        ('US', 'United States'),
        ('JP', 'Japan'),
        ('KR', 'South Korea'),
        ('HK', 'Hong Kong'),
        ('TW', 'Taiwan'),
        ('BR', 'Brazil'),
        ('ZA', 'South Africa'),
        ('AE', 'United Arab Emirates'),
        ('OTHER', 'Other'),
    ]

    # ── PERSONAL INFORMATION ──
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=5, choices=COUNTRY_CHOICES)
    country_of_residence = models.CharField(max_length=5, choices=COUNTRY_CHOICES)
    email = models.EmailField(unique=True)
    phone_country_code = models.CharField(max_length=6, default='+65')
    phone_number = models.CharField(max_length=20)

    # ── ADDRESS ──
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=5, choices=COUNTRY_CHOICES)

    # ── IDENTITY DOCUMENT ──
    id_type = models.CharField(max_length=20, choices=ID_TYPE_CHOICES)
    id_number = models.CharField(max_length=50)
    id_expiry_date = models.DateField()
    id_issuing_country = models.CharField(max_length=5, choices=COUNTRY_CHOICES)

    # ── DOCUMENT UPLOADS ──
    id_front_image = models.ImageField(upload_to='kyc_docs/id_front/', blank=True, null=True)
    id_back_image = models.ImageField(upload_to='kyc_docs/id_back/', blank=True, null=True)
    selfie_image = models.ImageField(upload_to='kyc_docs/selfie/', blank=True, null=True)
    proof_of_address = models.FileField(upload_to='kyc_docs/poa/', blank=True, null=True)

    # ── FINANCIAL PROFILE ──
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    employer_name = models.CharField(max_length=200, blank=True)
    annual_income = models.CharField(max_length=20, choices=INCOME_CHOICES)
    purpose_of_account = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    expected_monthly_transactions = models.CharField(max_length=100, blank=True)
    source_of_funds = models.TextField(blank=True)

    # ── PEP / COMPLIANCE ──
    is_pep = models.BooleanField(default=False, verbose_name='Politically Exposed Person (PEP)')
    pep_details = models.TextField(blank=True, verbose_name='PEP Details')
    has_criminal_record = models.BooleanField(default=False)
    criminal_record_details = models.TextField(blank=True)

    # ── CONSENTS ──
    consent_terms = models.BooleanField(default=False, verbose_name='Agreed to Terms & Conditions')
    consent_privacy = models.BooleanField(default=False, verbose_name='Agreed to Privacy Policy')
    consent_data_processing = models.BooleanField(default=False, verbose_name='Consented to Data Processing')
    consent_marketing = models.BooleanField(default=False, verbose_name='Opted into Marketing')

    # ── APPLICATION STATUS ──
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reviewer_notes = models.TextField(blank=True)
    reviewed_by = models.CharField(max_length=100, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    # ── METADATA ──
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    application_reference = models.CharField(max_length=20, unique=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'KYC Application'
        verbose_name_plural = 'KYC Applications'

    def __str__(self):
        return f"{self.first_name} {self.last_name} — {self.application_reference} ({self.get_status_display()})"

    def save(self, *args, **kwargs):
        if not self.application_reference:
            import random, string
            self.application_reference = 'SKN-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def documents_complete(self):
        return bool(self.id_front_image and self.selfie_image)
