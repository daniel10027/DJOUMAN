from django.contrib import admin
from .models import (
    User, Profile, Organization,
    ServiceCategory, Service, Equipment,
    Booking, Mission,
    Payment, Payout,
    Contract, Dispute, Review,
    CommissionPolicy,
    KycDocument, DeviceToken, WebhookEvent
)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "role", "status", "is_active", "is_staff", "date_joined")
    search_fields = ("username", "email", "phone")
    list_filter = ("role", "status", "is_active", "is_staff")

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name")
    search_fields = ("name", "user__username", "user__email")

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "status", "created_at")
    search_fields = ("name", "slug")
    list_filter = ("status",)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug", "is_active")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "slug")
    list_filter = ("is_active",)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "category", "owner", "base_price", "currency", "is_active", "created_at")
    search_fields = ("title", "description", "owner__username", "owner__email")
    list_filter = ("category", "is_active", "currency")

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "price_per_day", "deposit", "currency", "is_active", "created_at")
    search_fields = ("title", "owner__username", "owner__email")
    list_filter = ("is_active", "currency")

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "service", "equipment", "start_at", "end_at", "status", "price", "commission_rate", "commission_amount")
    search_fields = ("client__username", "client__email")
    list_filter = ("status", "currency", "start_at", "end_at")

@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "freelance", "status", "started_at", "completed_at")
    search_fields = ("freelance__username", "freelance__email")
    list_filter = ("status",)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "method", "amount", "currency", "fees", "status", "provider_ref", "idempotency_key", "created_at")
    search_fields = ("provider_ref", "idempotency_key")
    list_filter = ("method", "status", "currency", "created_at")

@admin.register(Payout)
class PayoutAdmin(admin.ModelAdmin):
    list_display = ("id", "beneficiary", "amount", "currency", "status", "created_at")
    search_fields = ("beneficiary__username", "beneficiary__email")
    list_filter = ("status", "currency", "created_at")

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "file_url", "signed_at", "created_at")
    search_fields = ("booking__id",)

@admin.register(Dispute)
class DisputeAdmin(admin.ModelAdmin):
    list_display = ("id", "booking", "opener", "reason", "status", "created_at")
    search_fields = ("opener__username", "opener__email", "reason")
    list_filter = ("status", "created_at")

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "target_user", "booking", "rating", "created_at")
    search_fields = ("author__username", "target_user__username")
    list_filter = ("rating", "created_at")

@admin.register(CommissionPolicy)
class CommissionPolicyAdmin(admin.ModelAdmin):
    list_display = ("id", "service_category", "rate", "min_amount", "max_amount", "is_active")
    list_filter = ("is_active",)


@admin.register(KycDocument)
class KycAdmin(admin.ModelAdmin):
    list_display = ("id","user","doc_type","status","created_at","reviewed_by","reviewed_at")
    list_filter = ("status","doc_type")
    search_fields = ("user__username","user__email")

@admin.register(DeviceToken)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id","user","platform","token","last_seen_at")
    search_fields = ("user__username","token")

@admin.register(WebhookEvent)
class WebhookEventAdmin(admin.ModelAdmin):
    list_display = ("id","source","event_id","status","created_at","processed_at")
    search_fields = ("source","event_id")
    list_filter = ("source","status")
