from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ('user', 'paid_at', 'course', 'lesson', 'amount', 'method')
    list_filter   = ('method', 'paid_at')
    search_fields = ('user__username',)

