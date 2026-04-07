from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from django.http import HttpResponse
import csv
from .models import KYCApplication


def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="kyc_applications.csv"'
    writer = csv.writer(response)
    writer.writerow([
        'Reference', 'Full Name', 'Email', 'Phone', 'Nationality',
        'Country of Residence', 'ID Type', 'ID Number', 'Employment',
        'Annual Income', 'Purpose', 'PEP', 'Status', 'Submitted At'
    ])
    for app in queryset:
        writer.writerow([
            app.application_reference, app.full_name, app.email,
            f"{app.phone_country_code}{app.phone_number}",
            app.get_nationality_display(), app.get_country_of_residence_display(),
            app.get_id_type_display(), app.id_number,
            app.get_employment_status_display(), app.get_annual_income_display(),
            app.get_purpose_of_account_display(), 'Yes' if app.is_pep else 'No',
            app.get_status_display(), app.created_at.strftime('%Y-%m-%d %H:%M'),
        ])
    return response

export_to_csv.short_description = "Export selected to CSV"


def mark_approved(modeladmin, request, queryset):
    queryset.update(status='approved', reviewed_by=request.user.username, reviewed_at=timezone.now())

mark_approved.short_description = "✅ Mark as Approved"


def mark_rejected(modeladmin, request, queryset):
    queryset.update(status='rejected', reviewed_by=request.user.username, reviewed_at=timezone.now())

mark_rejected.short_description = "❌ Mark as Rejected"


def mark_under_review(modeladmin, request, queryset):
    queryset.update(status='under_review', reviewed_by=request.user.username, reviewed_at=timezone.now())

mark_under_review.short_description = "🔍 Mark as Under Review"


@admin.register(KYCApplication)
class KYCApplicationAdmin(admin.ModelAdmin):

    list_display = [
        'application_reference', 'full_name_display', 'email', 'phone_display',
        'nationality', 'id_type_display', 'status_badge',
        'documents_badge', 'pep_flag', 'created_at'
    ]

    list_filter = [
        'status', 'nationality', 'country_of_residence', 'id_type',
        'employment_status', 'purpose_of_account', 'is_pep',
        'consent_terms', 'created_at',
    ]

    search_fields = [
        'first_name', 'last_name', 'email', 'phone_number',
        'application_reference', 'id_number',
    ]

    readonly_fields = [
        'application_reference', 'created_at', 'updated_at',
        'ip_address', 'user_agent', 'id_front_preview',
        'id_back_preview', 'selfie_preview', 'documents_complete',
    ]

    actions = [mark_approved, mark_rejected, mark_under_review, export_to_csv]

    fieldsets = (
        ('📋 Application Info', {
            'fields': (
                'application_reference', 'status', 'reviewer_notes',
                'reviewed_by', 'reviewed_at', 'created_at', 'updated_at',
            )
        }),
        ('👤 Personal Information', {
            'fields': (
                ('first_name', 'last_name'),
                'date_of_birth',
                ('nationality', 'country_of_residence'),
                'email',
                ('phone_country_code', 'phone_number'),
            )
        }),
        ('🏠 Address', {
            'fields': (
                'address_line1', 'address_line2',
                ('city', 'state', 'postal_code'),
                'country',
            )
        }),
        ('🪪 Identity Document', {
            'fields': (
                ('id_type', 'id_number'),
                ('id_expiry_date', 'id_issuing_country'),
            )
        }),
        ('📎 Document Uploads', {
            'fields': (
                'id_front_image', 'id_front_preview',
                'id_back_image', 'id_back_preview',
                'selfie_image', 'selfie_preview',
                'proof_of_address',
            )
        }),
        ('💼 Financial Profile', {
            'fields': (
                ('employment_status', 'employer_name'),
                ('annual_income', 'purpose_of_account'),
                'expected_monthly_transactions',
                'source_of_funds',
            )
        }),
        ('🛡️ Compliance', {
            'fields': (
                'is_pep', 'pep_details',
                'has_criminal_record', 'criminal_record_details',
            )
        }),
        ('✅ Consents', {
            'fields': (
                'consent_terms', 'consent_privacy',
                'consent_data_processing', 'consent_marketing',
            )
        }),
        ('🔧 Metadata', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',),
        }),
    )

    def full_name_display(self, obj):
        return format_html('<strong>{}</strong>', obj.full_name)
    full_name_display.short_description = 'Name'

    def phone_display(self, obj):
        return f"{obj.phone_country_code} {obj.phone_number}"
    phone_display.short_description = 'Phone'

    def id_type_display(self, obj):
        return obj.get_id_type_display()
    id_type_display.short_description = 'ID Type'

    def status_badge(self, obj):
        colors = {
            'pending': '#F59E0B',
            'under_review': '#3B82F6',
            'approved': '#10B981',
            'rejected': '#EF4444',
            'more_info': '#8B5CF6',
        }
        labels = {
            'pending': '⏳ Pending',
            'under_review': '🔍 Under Review',
            'approved': '✅ Approved',
            'rejected': '❌ Rejected',
            'more_info': '📋 More Info',
        }
        color = colors.get(obj.status, '#6B7280')
        label = labels.get(obj.status, obj.status)
        return format_html(
            '<span style="background:{};color:white;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:600;">{}</span>',
            color, label
        )
    status_badge.short_description = 'Status'

    def documents_badge(self, obj):
        if obj.documents_complete:
            return format_html('<span style="color:#10B981;font-weight:600;">✅ Complete</span>')
        return format_html('<span style="color:#EF4444;font-weight:600;">⚠️ Incomplete</span>')
    documents_badge.short_description = 'Docs'

    def pep_flag(self, obj):
        if obj.is_pep:
            return format_html('<span style="color:#EF4444;font-weight:700;">🚩 PEP</span>')
        return format_html('<span style="color:#9CA3AF;">—</span>')
    pep_flag.short_description = 'PEP'

    def id_front_preview(self, obj):
        if obj.id_front_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height:150px;border-radius:8px;" /></a>',
                obj.id_front_image.url, obj.id_front_image.url
            )
        return "No image uploaded"
    id_front_preview.short_description = 'ID Front Preview'

    def id_back_preview(self, obj):
        if obj.id_back_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height:150px;border-radius:8px;" /></a>',
                obj.id_back_image.url, obj.id_back_image.url
            )
        return "No image uploaded"
    id_back_preview.short_description = 'ID Back Preview'

    def selfie_preview(self, obj):
        if obj.selfie_image:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="max-height:150px;border-radius:50%;border:3px solid #4400CC;" /></a>',
                obj.selfie_image.url, obj.selfie_image.url
            )
        return "No selfie uploaded"
    selfie_preview.short_description = 'Selfie Preview'
