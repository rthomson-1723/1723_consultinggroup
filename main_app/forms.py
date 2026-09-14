from django import forms
from .models import PartnersInquiries,ApplicantsInquiries,JobPosting,JobApplication
from django.contrib.auth.models import User


class PartnersInquiriesForm(forms.ModelForm):
    class Meta:
        model = PartnersInquiries
        fields = ['first_name', 'last_name', 'company_name', 'email','phone', 'service','job_location','skills_needed','description','referral_source']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'company_name': 'Company',
            'email': 'Email',
            'phone': 'Phone',
            'service': 'Service',
            'job_location':"Job Location",
            'skills_needed':"Skills needed",
            'description': 'Description',
            'referral_source':"How did you hear about us?"
        }
        
        widgets={
            'service': forms.Select(attrs={'style': 'width: 100%; padding: 5px;'}),

        }
class ApplicantInquiriesForm(forms.ModelForm):
    other_interest = forms.CharField(
        required=False,
        label="Please specify"
    )
    class Meta:
        model = ApplicantsInquiries
        fields = ['first_name', 'last_name', 'email','phone','interest','other_interest','message']
        labels = {
            'first_name': 'First name',
            'last_name': 'Last name',
            'email': 'Email',
            'phone': 'Phone',
            'interest': 'Interest',
            'message': 'Message',
        }
        
        widgets={
          'interest': forms.Select(attrs={'style': 'width: 100%; padding: 5px;'}),
    }
        
    def clean(self):
        cleaned_data = super().clean()

        interest = cleaned_data.get('interest')
        other_interest = cleaned_data.get('other_interest')

        if interest == 'other' and not other_interest:
            self.add_error(
                'other_interest',
                'Please specify your interest.'
            )

        return cleaned_data
        


class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting
        fields = [
            'title',
            'company',
            'location',
            'description',
            'requirements',
            'salary',
            'employment_type',
            'status',
        ]
        labels = {
            'title': 'Title',
            'company': 'Company',
            'location': 'Location',
            'description': 'Description',
            'requirements': 'Requirement',
            'salary': 'Salary',
            'employment_type':'Type of Employment',
            'status':'Status',
        }
        
class JobApplicationForm(forms.ModelForm):

    class Meta:
        model = JobApplication
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'resume',
            'cover_letter',
            'years_of_experience',
            'available_start_date',
            'drivers_license',
            'reliable_transportation',
            'terms_and_conditions',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),

            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),

            'cover_letter': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4
            }),

            'years_of_experience': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'available_start_date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),

            'drivers_license': forms.Select(attrs={'style': 'width: 100%; padding: 5px;'}),
            'reliable_transportation': forms.Select(attrs={'style': 'width: 100%; padding: 5px;'}),

            'terms_and_conditions': forms.CheckboxInput(),
        }

    
def clean_terms_and_conditions(self):
    agreed = self.cleaned_data.get('terms_and_conditions')

    if not agreed:
        raise forms.ValidationError(
            'You must agree to the Terms and Conditions.'
        )

    return agreed



class EditProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'email': forms.EmailInput(attrs={
                'class': 'form-control'
            }),

            'username': forms.TextInput(attrs={
                'class': 'form-control'
            }),
        }