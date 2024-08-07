from django.contrib.auth.models import User
from django.db import models

optional = {
    'null': True,
    'blank': True
}


class Ride(models.Model):
    status = models.CharField(max_length=50, default='', **optional)
    rider = models.ForeignKey('app_main.UserProfile',
                              related_name='rider',
                              on_delete=models.SET_NULL,
                              **optional)
    driver = models.ForeignKey('app_main.UserProfile',
                               related_name='driver',
                               on_delete=models.SET_NULL,
                               **optional)
    pickup_latitude = models.FloatField(**optional)
    pickup_longitude = models.FloatField(**optional)
    dropoff_latitude = models.FloatField(**optional)
    dropoff_longitude = models.FloatField(**optional)
    pickup_time = models.DateTimeField(null=True, blank=True)
    datetime_inserted = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ride'
        verbose_name_plural = 'Rides'


class RideEvent(models.Model):
    ride = models.ForeignKey('app_main.Ride', on_delete=models.SET_NULL, **optional)
    description = models.CharField(max_length=500, default='', **optional)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ride Event'
        verbose_name_plural = 'Ride Events'


class Role(models.Model):
    name = models.CharField(default='', max_length=200)
    code = models.CharField(default='', max_length=20)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey('app_main.Role', on_delete=models.SET_NULL, **optional)
    phone_number = models.CharField(max_length=20, default='', **optional)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-pk']

    def __str__(self):
        return '{} {}'.format(self.user.first_name, self.user.last_name)

