from datetime import timedelta, timezone
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.views import View
from .forms import PartnersInquiriesForm, ApplicantInquiriesForm, JobPostingForm,JobApplicationForm, EditProfileForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import JobPosting,PartnersInquiries,ApplicantsInquiries,JobApplication, TermsAndConditions


class login(LoginView):
    template_name = 'registration/login.html'

class logout(LogoutView):
    next_page = reverse_lazy('login')
    
def home(request):
    return  render(request, 'home.html')

def services(request):
    return  render(request, 'services.html')

def about(request):
    return  render(request, 'about.html')

def contact(request):
    return  render(request, 'contact.html')


def message_page(request, source):
    if source == "employers":
        back_url = "employers"
        back_text = "Back to employers page"

    elif source == "careers":
        back_url = "careers"
        back_text = "Back to general inquiry page"

    elif source == "jobs":
            back_url = "jobs"
            back_text = "Back to careers page"

    else:
        back_url = "home"
        back_text = "Back to Home"

    return render(
        request,
        "message.html",
        {
            "back_url": back_url,
            "back_text": back_text,
        },
    )


def job_board(request):
    keyword = request.GET.get('keyword', '').strip()
    location = request.GET.get('location', '').strip()

    job_list = JobPosting.objects.all().order_by('-created_at')

    if keyword:
        job_list = job_list.filter(
            title__icontains=keyword
        )

    if location:
        job_list = job_list.filter(
            location__icontains=location
        )
    paginator = Paginator(job_list, 10)  # 10 jobs per 
    page_number = request.GET.get("page")
    jobs = paginator.get_page(page_number)

    return render(request, 'job_board.html', {
        'jobs': jobs,
        'keyword': keyword,
        'location': location,
    })

def job_detail(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    return render(request, 'job_detail.html', {
        'job': job
    })

def partners_inquiries(request):
    if request.method == "POST":
        partner_inquiry_form = PartnersInquiriesForm(
            request.POST,
            request.FILES
        )
        if partner_inquiry_form.is_valid() and any(partner_inquiry_form.cleaned_data.values()):
            partner_inquiry_form.save()
            messages.success(request, "Your submission was successful!")
            
            applicant_email = partner_inquiry_form.cleaned_data.get("email")
            service = partner_inquiry_form.cleaned_data.get("service")
            partner = partner_inquiry_form.cleaned_data.get("company_name")

            # Email to applicant
            send_mail(
                subject="Thank you for your Application",
                message=f"""
Dear Partner,

Thank you for applying to become a partner with us. We truly value your business and appreciate you choosing us for your {service} needs.
Your application has been received successfully. Our team will review it shortly, and we will get back to you as soon as possible regarding the next steps.
Thank you again for your interest in partnering with us.

Sincerely,
The 1723 Consulting Group Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[applicant_email],
                fail_silently=False,
            )

            # Email to admin
            send_mail(
                subject="New Partner Inquiry",
                message=f"""
Hi team, you have received a new partner inquiry
Company Name: {partner}
Service Requested: {service}
Email: {applicant_email}
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            return redirect("message_page", source="employers")

    else:
        partner_inquiry_form = PartnersInquiriesForm()

    return render(
        request,
        "employers.html",
        {
            "partner_inquiry_form": partner_inquiry_form,
        },
    )

def partner_detail(request, pk):
    partner = get_object_or_404(PartnersInquiries, pk=pk)
    return render(request, "admin/partner_detail.html", {"partner": partner})

def job_application_detail(request, pk):
    job_application = get_object_or_404(JobApplication, pk=pk)
    return render(request, "admin/job_applications_details.html", {"job_application": job_application })

def admin_partners(request):
    keyword = request.GET.get('keyword', '').strip()
    location = request.GET.get('location', '').strip()
    date_range = request.GET.get('date_range', '').strip()
    service = request.GET.get('service', '').strip()
    skills = request.GET.get('skills', '').strip()

    # Start with all inquiries
    inquiries = PartnersInquiries.objects.all().order_by('-created_at')

    # Keyword search
    if keyword:
        inquiries = inquiries.filter(
            Q(first_name__icontains=keyword) |
            Q(last_name__icontains=keyword) |
            Q(company_name__icontains=keyword) |
            Q(description__icontains=keyword)
        )

    # Location search
    if location:
        inquiries = inquiries.filter(
            job_location__icontains=location
        )

    # Date range
    if date_range in ['7', '30']:
        cutoff_date = timezone.now() - timedelta(days=int(date_range))
        inquiries = inquiries.filter(
            created_at__gte=cutoff_date
        )

    # Service filter
    if service:
        inquiries = inquiries.filter(
            service=service
        )

    # Skills filter
    if skills:
        inquiries = inquiries.filter(
            skills_needed=skills
        )

    # Pagination
    partners_paginator = Paginator(inquiries, 10)

    partners_applications = partners_paginator.get_page(
        request.GET.get('partners_page')
    )

    # Context
    context = {
        'partners_applications': partners_applications,
        'keyword': keyword,
        'location': location,
        'date_range': date_range,
        'service': service,
        'skills': skills,
    }

    return render(
        request,
        'admin/partners_inquiries.html',
        context
    )

def applicant_inquiries(request):
    if request.method == "POST":
        applicant_inquiry_form = ApplicantInquiriesForm(request.POST, request.FILES)

        if applicant_inquiry_form.is_valid() and any(applicant_inquiry_form.cleaned_data.values()):
            applicant_inquiry_form.save()

            applicant_email = applicant_inquiry_form.cleaned_data.get('email')
            applicant_name = applicant_inquiry_form.cleaned_data.get('name')
            interest = applicant_inquiry_form.cleaned_data.get('interest')
           

            # Email to applicant
            send_mail(
                subject="Thank you for your Application",
                message=f"""
Hello {applicant_name},
Thank you for submitting for a general application for the {interest} field.
Your application has been received successfully. A member of our team will get back to you as soon as we
open positions that matches your skilss.
Thank you again for your interest in our career opportunities.

Sincerely,The 1723 Consulting Group Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[applicant_email],
                fail_silently=False,
            )

            # Email to admin
            send_mail(
                subject="New Job Inquiry",
                message=f"Hi team, you have received a new general application inquiry from {applicant_name} for {interest}.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            return redirect("message_page", source="careers")
    else:
        applicant_inquiry_form = ApplicantInquiriesForm()

    return render(
        request,
        "job_seekers.html",
        {"applicant_inquiries_form": applicant_inquiry_form},
    )

def applicant_detail(request, pk):
    applicant = get_object_or_404(ApplicantsInquiries, pk=pk)
    return render(request, "admin/applicant_detail.html", {"applicant": applicant})

def job_applications(request, job_id):
    job = get_object_or_404(JobPosting, id=job_id)

    terms = TermsAndConditions.objects.filter(
        active=True
    ).first()

    if request.method == "POST":
        job_application_form = JobApplicationForm(
            request.POST,
            request.FILES
        )

        if job_application_form.is_valid():
            application = job_application_form.save(commit=False)
            application.position = job
            application.save()

            # Get applicant information from the job application form
            applicant_email = job_application_form.cleaned_data.get("email")
            applicant_name = job_application_form.cleaned_data.get("first_name")

            # Email to applicant
            send_mail(
                subject="Thank you for your Application",
                message=f"""
Hello {applicant_name},

Thank you for submitting your application for the {job.title} position.

Your application has been received successfully. A member of our team will
review your application and get back to you as soon as possible.

Thank you again for your interest in joining our team.

Sincerely,
The 1723 Consulting Group Team
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[applicant_email],
                fail_silently=False,
            )

            # Email to admin
            send_mail(
                subject="New Job Application",
                message=f"""
Hi team,

You have received a new job application from {applicant_name}
for the position: {job.title}.

Please log in to the admin panel to review the application.
                """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            return redirect("message_page", source="careers")

    else:
        job_application_form = JobApplicationForm()

    return render(
        request,
        "job_application.html",
        {
            "job_application_form": job_application_form,
            "job": job,
            "terms": terms,
        }
    )

def profile(request):
    return  render(request, 'admin/profile.html')



def admin_applicants(request):
    applicants_applications= ApplicantsInquiries.objects.all().order_by('created_at')
    applicants_paginator = Paginator(applicants_applications, 10)
    applicants_applications = applicants_paginator.get_page(
                request.GET.get('applicants_page')
            )

    return  render(request, 'admin/applicants_inquiries.html',{'applicants_applications': applicants_applications})

def admin_job_applications(request):
    jobs_applications = JobApplication.objects.all().order_by('-created_at')
    jobs_applications_paginator = Paginator(jobs_applications, 10)
    jobs_applications = jobs_applications_paginator.get_page(
                request.GET.get('job_applications_page')
            )
    
    return  render(request, 'admin/jobs_applications.html',{'jobs_applications': jobs_applications})

@login_required
def create_job_post(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save()

            send_mail(
                subject='New Job Posted',
                message=f'''
                A new job has been posted:

                    Title: {job.title}
                    Company: {job.company}
                    Location: {job.location}
                    ''',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.ADMIN_EMAIL],
                fail_silently=False,
            )

            messages.success(request, "Job posted successfully!")
            return redirect('add-jobs')  # redirect back to form
    else:
        form = JobPostingForm()

    return render(request, 'admin/add_jobs.html', {'form': form})

@login_required
def dashboard(request):
    jobs = JobPosting.objects.all().order_by('-created_at')
    partners_applications = PartnersInquiries.objects.all().order_by('-created_at')
    applicants_applications= ApplicantsInquiries.objects.all().order_by('created_at')

    # Last 7 days
    one_week_ago = timezone.now() - timedelta(days=7)

    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Job Applications
    weekly_job_applications = JobApplication.objects.filter(
        created_at__gte=one_week_ago
    ).order_by('-created_at')

    # General Applicant Inquiries
    weekly_general_inquiries = ApplicantsInquiries.objects.filter(
        created_at__gte=one_week_ago
    ).order_by('-created_at')

    # Partner Inquiries
    weekly_partner_inquiries = PartnersInquiries.objects.filter(
        created_at__gte=one_week_ago
    ).order_by('-created_at')

    new_partners_applications =  PartnersInquiries.objects.filter(
        created_at__gte=thirty_days_ago
            ).order_by("-created_at")

    new_general_applications = ApplicantsInquiries.objects.filter(
        created_at__gte=thirty_days_ago
        ).order_by("-created_at")

    new_job_applications = JobApplication.objects.filter(
        created_at__gte=thirty_days_ago
        ).order_by("-created_at") 

    
    jobs_paginator = Paginator(jobs, 10)
    applicants_paginator = Paginator(applicants_applications, 10)


    jobs = jobs_paginator.get_page(
        request.GET.get('jobs_page')
    )

    

    applicants_applications = applicants_paginator.get_page(
        request.GET.get('applicants_page')
    )

    context = {
        'weekly_job_applications': weekly_job_applications,
        'weekly_general_inquiries': weekly_general_inquiries,
        'weekly_partner_inquiries': weekly_partner_inquiries,
        'jobs': jobs,
        'partners_applications': partners_applications,
        'applicants_applications': applicants_applications,
        'new_partners_applications': new_partners_applications,
        'new_general_applications': new_general_applications,
        'new_job_applications': new_job_applications

    }
    return  render(request, 'admin/dashboard.html',context)

@login_required
def edit_profile(request):

    if request.method == 'POST':

        form = EditProfileForm(
            request.POST,
            instance=request.user
        )

        if form.is_valid():
            form.save()

            return redirect('dashboard')

    else:

        form = EditProfileForm(
            instance=request.user
        )

    context = {
        'form': form
    }

    return render(
        request,
        'admin/edit_profile.html',
        context
    )

def admin_job_listing(request):
    job_lists = JobPosting.objects.all().order_by('-created_at')
    return  render(request, 'admin/job_listing.html', {"job_lists": job_lists})

