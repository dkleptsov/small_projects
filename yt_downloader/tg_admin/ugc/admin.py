from django.contrib import admin

# Register your models here.
from .forms import ProfileForm
from .models import Message
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at')
    
    def get_queryset(self, request):
        return