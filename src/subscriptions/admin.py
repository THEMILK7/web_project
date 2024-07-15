from django.contrib import admin
from .models import Subscription

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user','cours_id','plan', 'price', 'start_date', 'end_date')
    list_filter = ('plan', 'start_date')
    list_editable = ("end_date",)
    search_fields = ('user__user__username', 'plan')  # Adjust fields based on actual User model structure

admin.site.register(Subscription, SubscriptionAdmin)