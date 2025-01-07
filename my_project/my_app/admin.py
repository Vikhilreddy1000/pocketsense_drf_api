from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.urls import include, path
from .models import CustomUser, Group, Expense, Settlement, Category



class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email","username")
    list_filter = ("email","first_name","last_name",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Professional details", {"fields": ("username", "first_name", "last_name", "college", "semester", "default_payment_methods")}),
        ("Additional detaisl", {"fields": ("otp", "otp_verification", "phone_no", "country_code")}),

    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password", "is_active"
            )}
        ),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(CustomUser,CustomUserAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    fields = [
        'title',
        'amount',
        'category',
        'receipt_image',
        'created_by',
        'split_type',
    ]
    list_display = [
        'title',
        'amount',
        'category',
        'created_by',
        'split_type',
    ]

admin.site.register(Expense,ExpenseAdmin)

class GroupAdmin(admin.ModelAdmin):
    fields = [
        'name',
        'members',
        'created_by'
    ]
    list_display = [
        'name',
        'created_by'
    ]

admin.site.register(Group,GroupAdmin)

class SettlementAdmin(admin.ModelAdmin):
    fields = [
        'expense',
        'settled_by',
        'payment_status',
        'settlement_method'
    ]
    list_display = [
        'expense',
        'settled_by',
        'payment_status',
        'settlement_method',
        'due_date'
    ]
admin.site.register(Settlement,SettlementAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = [
        'name'
    ]
    list_display = [
        'name'
    ]

admin.site.register(Category,CategoryAdmin)






