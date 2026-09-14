from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone
from django.contrib.auth.models import User

created_at = models.DateTimeField(default=timezone.now)


class Profile(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=20,
        blank=True
    )

    profile_picture = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
         return f"{self.user.username}'s Profile"


class PartnersInquiries(models.Model):
  SERVICE_CHOICES = [
        ('Training', 'Training'),
        ('Staffing', 'Staffing'),
        ('Consulting', 'Consulting'),
    ]
  
  SKILLS_NEEDED = [
        ('General', 'General Labor(No skills required)'),
        ('Skilled', 'Skilled Labor(Experience required)'),
      
    ]
  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  company_name = models.CharField(max_length=100)
  email = models.EmailField(_("Email"), max_length=254)
  phone = PhoneNumberField(
        unique=True,
    )
  service = models.CharField(max_length=20, choices=SERVICE_CHOICES)
  job_location = models.CharField(max_length=100)
  skills_needed = models.CharField(max_length=20, choices=SKILLS_NEEDED)
  description = models.TextField(max_length=250)
  referral_source = models.CharField(max_length=100)
  created_at = models.DateTimeField(auto_now_add=True)
  
  

def __str__(self):
    return " | ".join(
        f"{field.name}: {getattr(self, field.name)}"
        for field in self._meta.fields
    )

class ApplicantsInquiries(models.Model):
  JOBS_CHOICES = [
        ('clerical', 'Clerical'),
        ('factory', 'Factory'),
        ('forklift_operator', 'Forklift Operator'),
        ('mover', 'Mover'),
        ('warehouse', 'Warehouse'),
        ('other', 'Other'),
 
    ]

  first_name = models.CharField(max_length=100)
  last_name = models.CharField(max_length=100)
  email = models.EmailField(_("Email"), max_length=254)
  phone = PhoneNumberField(
          unique=True,
      )
  interest= models.CharField(max_length=20,choices=JOBS_CHOICES)
  message = models.TextField(max_length=250)
  created_at = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return " | ".join(
        f"{field.name}: {getattr(self, field.name)}"
        for field in self._meta.fields
    )



class JobPosting(models.Model):
    EMPLOYMENT_TYPES = [
        ('FT', 'Full-Time'),
        ('PT', 'Part-Time'),
        ('TEMP', 'Temporary'),
        ('CONTRACT', 'Contract'),
        ('SEASONAL', 'Seasonal'),
    ]
    STATUS_CHOICES = [
            ('OPEN', 'Open'),
            ('CLOSE', 'Closed'),
            
        ]

    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    salary = models.CharField(max_length=100, blank=True)
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_TYPES,
        default='FT'
    )

    status = models.CharField(
        max_length= 20,
        choices= STATUS_CHOICES,
        default= 'OPEN'

    )
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    


class JobApplication(models.Model):
    YES_NO_CHOICES = [
        ('YES', 'Yes'),
        ('NO', 'No'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('REVIEWING', 'Reviewing'),
        ('INTERVIEW', 'Interview Scheduled'),
        ('HIRED', 'Hired'),
        ('REJECTED', 'Rejected'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    email = models.EmailField()
    phone_number = models.CharField(max_length=20)

    resume = models.FileField(
        upload_to='resumes/'
    )

    cover_letter = models.TextField(
        blank=True,
        null=True
    )

    years_of_experience = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    drivers_license = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Do you have a valid driver’s license?"
    )

    reliable_transportation = models.CharField(
        max_length=3,
        choices=YES_NO_CHOICES,
        verbose_name="Do you have reliable transportation?"
    )


    available_start_date = models.DateField(
        blank=True,
        null=True
    )

    
    terms_and_conditions = models.BooleanField(
        default=False,
        verbose_name="I agree to the terms and conditions"
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    position = models.ForeignKey(
        JobPosting,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} "


class TermsAndConditions(models.Model):
    title = models.CharField(
        max_length=200,
        default="Terms and Conditions"
    )

    content = models.TextField()

    active = models.BooleanField(
        default=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title