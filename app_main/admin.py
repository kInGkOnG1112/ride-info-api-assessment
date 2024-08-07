from django.contrib import admin
from app_main.models import (
    Ride,
    RideEvent,
    Role,
    UserProfile
)


@admin.register(Ride)
class RideAdmin(admin.ModelAdmin):
    raw_id_fields = ('rider', 'driver')
    list_display = ('status', 'rider', 'driver', 'pickup_time')


@admin.register(RideEvent)
class RideEventAdmin(admin.ModelAdmin):
    raw_id_fields = ('ride',)
    list_display = ('ride', 'description', 'created_at')


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)
    list_display = ('user', 'role', 'phone_number')
    search_fields = (
        'user__email',
        'user__first_name',
        'user__last_name',
        'phone_number',
    )


