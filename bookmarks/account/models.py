from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth import get_user_model

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'Profile of {self.user.username}'
1
class Contact(models.Model):

    #foreignkey for the user who creates the relationship
    user_from = models.ForeignKey('auth.User', related_name='rel_from_set', on_delete=models.CASCADE)
    #foreignkey for the user being followed
    user_to = models.ForeignKey('auth.User', related_name='rel_to_set', on_delete=models.CASCADE)
    #datetimefield to store the time when the relationship was created
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    
    def __str__(self):
        return f'{self.user_from} follows {self.user_to}'

"""
following = models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False)

symmetrical is set to False because by default it is set to True. by doing this, if A follows B, B would not automatically follow A.

ideally, should add this to the User model, but we are using the django.contrib.auth user model, hence we have to do the following:

the django.contrib.auth user model will contain a ManyToManyField of 'following'.
"""

user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self', through=Contact, related_name='followers', symmetrical=False))