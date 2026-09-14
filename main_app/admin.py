from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.models import User
from .models import ApplicantsInquiries, PartnersInquiries, JobPosting,JobApplication,Profile, TermsAndConditions


admin.site.register(PartnersInquiries)
admin.site.register(ApplicantsInquiries)
admin.site.register(JobPosting)
admin.site.register(JobApplication)
admin.site.register(Profile)
admin.site.register(TermsAndConditions)
