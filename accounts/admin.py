from django.contrib import admin
from .models import BankAccountType, User, UserAddress, UserBankAccount

class BankAccountTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('username', 'email')

class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'address_line1', 'city', 'state', 'postal_code')
    search_fields = ('user__username', 'address_line1', 'city')

class UserBankAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'account_type', 'account_number', 'balance')
    search_fields = ('user__username', 'account_number')
    list_filter = ('account_type',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "account_type":
            kwargs["queryset"] = BankAccountType.objects.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

# Registering models with admin
admin.site.register(BankAccountType, BankAccountTypeAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(UserAddress, UserAddressAdmin)
admin.site.register(UserBankAccount, UserBankAccountAdmin)




