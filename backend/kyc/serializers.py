from rest_framework import serializers
from .models import KYCApplication


class KYCApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = KYCApplication
        fields = [
            # Personal
            'first_name', 'last_name', 'date_of_birth', 'nationality',
            'country_of_residence', 'email', 'phone_country_code', 'phone_number',
            # Address
            'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country',
            # Identity
            'id_type', 'id_number', 'id_expiry_date', 'id_issuing_country',
            # Documents
            'id_front_image', 'id_back_image', 'selfie_image', 'proof_of_address',
            # Financial
            'employment_status', 'employer_name', 'annual_income',
            'purpose_of_account', 'expected_monthly_transactions', 'source_of_funds',
            # Compliance
            'is_pep', 'pep_details', 'has_criminal_record', 'criminal_record_details',
            # Consents
            'consent_terms', 'consent_privacy', 'consent_data_processing', 'consent_marketing',
        ]

    def validate_consent_terms(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the Terms & Conditions.")
        return value

    def validate_consent_privacy(self, value):
        if not value:
            raise serializers.ValidationError("You must agree to the Privacy Policy.")
        return value

    def validate_consent_data_processing(self, value):
        if not value:
            raise serializers.ValidationError("You must consent to data processing.")
        return value

    def validate(self, data):
        # Validate ID expiry is in the future
        from django.utils import timezone
        if data.get('id_expiry_date') and data['id_expiry_date'] < timezone.now().date():
            raise serializers.ValidationError({'id_expiry_date': 'ID document has expired.'})
        return data


class KYCStatusSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = KYCApplication
        fields = ['application_reference', 'status', 'status_display', 'created_at', 'updated_at']
