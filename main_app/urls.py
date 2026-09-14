from django.urls import path, include 
from . import views
from django.contrib.auth import views as auth_views

urlpatterns =[
path('',views.home, name='home'),
path('services/', views.services, name='services'),
path('employers/', views.partners_inquiries, name='employers'),
path('careers/', views.applicant_inquiries, name='careers'),
path('about/', views.about, name='about'),
path('jobs/', views.job_board, name='job_board'),
path('apply/<int:job_id>/', views.job_applications, name='apply'),
path('contact-us/', views.contact, name='contact-us'),
path('login/', views.login.as_view(), name='login'),
path('logout/', views.logout.as_view(), name='logout'),
path(
        'forgot-password/',
        auth_views.PasswordResetView.as_view(
            template_name='registration/forgot_password.html'
        ),
        name='forgot_password'
    ),
path('profile/',views.profile,name='profile'),
path('edit-profile/',views.edit_profile,name='edit-profile'),
path('dashboard/', views.dashboard, name='dashboard'),
path('partners/', views.admin_partners, name='partners'),
path('applicants/', views.admin_applicants, name='applicants'),
path('job-applications/', views.admin_job_applications, name='job-applications'),
path('add-jobs/', views.create_job_post, name='add-jobs'),
path('message/<str:source>/', views.message_page, name='message_page'),
path(
    "partners/<int:pk>/",
    views.partner_detail,
    name="partner_detail",
),

path(
    "applicants/<int:pk>/",
    views.applicant_detail,
    name="applicant_detail",
),

path('jobs/<int:job_id>/', views.job_detail, name='job_detail'),

path('job-applications/<int:pk>/', views.job_application_detail, name='job_application_detail'),

path('job-listing/', views.admin_job_listing, name='job_listing'),
]