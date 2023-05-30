from django.contrib import admin
from .models import *


# Register your models here.


class PolicyAdmin(admin.ModelAdmin):
    list_display = '__all__'


class ClaimAdmin(admin.ModelAdmin):
    list_display = '__all__'


class PaymentAdmin(admin.ModelAdmin):
    list_display = '__all__'


admin.site.register(Policy)
admin.site.register(Claim)
admin.site.register(Payment)
