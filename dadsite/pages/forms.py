from django import forms
from .models import ClientInquiry


class ClientInquiryForm(forms.ModelForm):
    """Client onboarding form for capturing fitness goals and information"""

    fitness_goals = forms.MultipleChoiceField(
        choices=ClientInquiry.GOAL_CHOICES,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'space-y-2',
        }),
        required=True,
        label='Fitness Goals'
    )

    class Meta:
        model = ClientInquiry
        fields = [
            'name', 'email', 'phone', 'age',
            'fitness_level', 'fitness_goals', 'additional_goals', 'current_frequency',
            'injuries_limitations', 'message', 'referral_source'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'Your Full Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'your.email@example.com',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': '(555) 123-4567',
                'id': 'id_phone',
                'maxlength': '14',
            }),
            'age': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'Your age',
                'min': '13',
                'max': '120',
            }),
            'fitness_level': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange cursor-pointer',
            }),
            'additional_goals': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'Any other specific fitness goals or details...',
                'rows': 3,
            }),
            'current_frequency': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange cursor-pointer',
            }),
            'injuries_limitations': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'List any injuries, health conditions, or physical limitations we should know about...',
                'rows': 3,
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'Tell us more about what you want to achieve and why you want to work with Anvil Fitness...',
                'rows': 4,
            }),
            'referral_source': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-white border-2 border-gray-300 text-black rounded-lg focus:outline-none focus:ring-2 focus:ring-brand-orange focus:border-brand-orange transition hover:border-brand-orange',
                'placeholder': 'Google, Instagram, Friend referral, etc.',
            }),
        }
        labels = {
            'name': 'Full Name *',
            'email': 'Email Address *',
            'phone': 'Phone Number',
            'age': 'Age',
            'fitness_level': 'Current Fitness Level *',
            'additional_goals': 'Additional Goals or Details',
            'current_frequency': 'How Often Do You Currently Exercise? *',
            'injuries_limitations': 'Injuries or Limitations',
            'message': 'Tell Us About Your Goals',
            'referral_source': 'How Did You Hear About Us?',
        }

    def clean_fitness_goals(self):
        """Convert list of goals to comma-separated string"""
        goals = self.cleaned_data.get('fitness_goals', [])
        return ','.join(goals)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields explicitly
        # Required fields (marked with * in labels)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['fitness_level'].required = True
        self.fields['current_frequency'].required = True
        self.fields['fitness_goals'].required = True

        # Optional fields (no *)
        self.fields['phone'].required = False
        self.fields['age'].required = False
        self.fields['additional_goals'].required = False
        self.fields['injuries_limitations'].required = False
        self.fields['message'].required = False
        self.fields['referral_source'].required = False

        # If editing existing instance, pre-populate checkboxes
        if self.instance and self.instance.pk and self.instance.fitness_goals:
            self.initial['fitness_goals'] = self.instance.fitness_goals.split(',')

    def save(self, commit=True):
        """Override save to clean empty optional fields"""
        instance = super().save(commit=False)

        # Clean optional fields - set to empty string or None if blank
        if not instance.phone or instance.phone.strip() == '':
            instance.phone = ''
        if not instance.age:
            instance.age = None
        if not instance.additional_goals or instance.additional_goals.strip() == '':
            instance.additional_goals = ''
        if not instance.injuries_limitations or instance.injuries_limitations.strip() == '':
            instance.injuries_limitations = ''
        if not instance.message or instance.message.strip() == '':
            instance.message = ''
        if not instance.referral_source or instance.referral_source.strip() == '':
            instance.referral_source = ''

        if commit:
            instance.save()
        return instance
