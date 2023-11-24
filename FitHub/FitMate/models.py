from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth import get_user_model
from PIL import Image 

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email
    

#profile

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name= models.CharField(max_length=50)     
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    fitness_level = models.CharField(
        max_length=20,
        choices=[
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
        ],
        blank=True
    )

    # Fitness goals and preferences
    fitness_goals = models.TextField(blank=True)
    workout_preferences = models.TextField(blank=True)
    nutritional_preferences = models.TextField(blank=True)

    age = models.IntegerField(blank=True, null=True)
    gender = models.CharField(
        max_length=10,
        choices=[
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Other', 'Other'),
        ],
        blank=True
    )
    height = models.FloatField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    medical_conditions = models.TextField(blank=True)
    medications = models.TextField(blank=True)
    allergies = models.BooleanField(default=False)
    suggested_workout = models.CharField(max_length=50, blank=True, null=True)





    def __str__(self):
        return self.user.email

class Gallery(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    gallery_pic = models.ImageField(upload_to='profile_pictures/')

    def __str__(self):
        return self.name
    

class Trainer(models.Model):
    name = models.CharField(max_length=50)
    expertise = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class MembershipPlan(models.Model):
    name = models.CharField(max_length=50)
    duration_months = models.IntegerField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Enrollment(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=30)
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female')])
    emergency_contact_name = models.CharField(max_length=50)
    emergency_contact_phone = models.CharField(max_length=15)
    agreement = models.BooleanField()
    joining_date = models.DateField()
    payment_status = models.BooleanField(default=False)
    membership_plan = models.ForeignKey(MembershipPlan, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    due_date = models.DateField()

    def __str__(self):
        return self.user.email
    


class VirtualFitnessClass(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date_time = models.DateTimeField()
    instructor = models.ForeignKey(Trainer, on_delete=models.CASCADE, null=True, blank=True)
    meeting_link = models.URLField()

    def __str__(self):
        return self.title