from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings  # Import settings to use AUTH_USER_MODEL
from datetime import date

class CustomUser(AbstractUser):
    public_visibility = models.BooleanField(default=True)
    age = models.IntegerField(null=True, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    address = models.TextField(max_length=255,null=True, blank=True)

    @property
    def age(self):
        if self.birth_year:
            return date.today().year - self.birth_year
        return None

    def __str__(self):
        return self.username
    
    
class UploadedFile(models.Model):
    VISIBILITY_CHOICES = [
        ('public', 'Public'),
        ('private', 'Private'),
    ]

    file_name = models.CharField(max_length=255,default='default_file_name')  # To store the file's name
    file_path = models.TextField(null=True, blank=True)  # Allow it to be empty
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='uploaded_files')
    title = models.CharField(max_length=255)
    description = models.TextField()
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='public')
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    year_published = models.PositiveIntegerField(null=True, blank=True)
    file = models.FileField(upload_to='uploaded_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def is_visible_to_user(self, user):
        """
        Check if a file is visible to the given user.
        Public files are visible to everyone.
        Private files are visible only to the owner.
        """
        if self.visibility == 'public' or self.user == user:
            return True
        return False
