from django.contrib import admin

from .models import Token

class TokenAdmin(admin.ModelAdmin):
	list_display = ('token', 'daily_computation_time', 'used_computation_time', 'last_api_call')
	ordering = ('last_api_call',)
	
admin.site.register(Token, TokenAdmin)
