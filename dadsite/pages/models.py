from django.db import models
from django.utils import timezone


class ContentBlock(models.Model):
    """Editable content blocks for pages"""

    PAGE_CHOICES = [
        ('home', 'Home'),
        ('about', 'About'),
        ('services', 'Services'),
    ]

    page = models.CharField(max_length=50, choices=PAGE_CHOICES)
    identifier = models.SlugField(max_length=100, help_text="Unique identifier for this content block")
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='content/', blank=True, null=True)
    order = models.IntegerField(default=0, help_text="Display order on the page")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page', 'order']
        unique_together = ['page', 'identifier']
        verbose_name = 'Content Block'
        verbose_name_plural = 'Content Blocks'

    def __str__(self):
        return f"{self.get_page_display()} - {self.identifier}"


class Announcement(models.Model):
    """News/updates/announcements section"""

    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text="Show on website")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-published_date']
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'

    def __str__(self):
        return self.title


class ClientInquiry(models.Model):
    """Client onboarding inquiries and information"""

    FITNESS_LEVEL_CHOICES = [
        ('beginner', 'Beginner - New to fitness'),
        ('intermediate', 'Intermediate - Regular exercise'),
        ('advanced', 'Advanced - Experienced athlete'),
    ]

    GOAL_CHOICES = [
        ('weight_loss', 'Weight Loss'),
        ('muscle_gain', 'Muscle Gain'),
        ('strength', 'Strength Training'),
        ('endurance', 'Endurance/Cardio'),
        ('flexibility', 'Flexibility/Mobility'),
        ('general_fitness', 'General Fitness'),
        ('sports_performance', 'Sports Performance'),
    ]

    FREQUENCY_CHOICES = [
        ('none', 'Not currently exercising'),
        ('1-2', '1-2 times per week'),
        ('3-4', '3-4 times per week'),
        ('5+', '5+ times per week'),
    ]

    # Basic Info
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    age = models.IntegerField(null=True, blank=True, help_text="Age in years")

    # Fitness Info
    fitness_level = models.CharField(max_length=20, choices=FITNESS_LEVEL_CHOICES)
    fitness_goals = models.TextField(help_text="Selected fitness goals (comma-separated)")
    additional_goals = models.TextField(blank=True, help_text="Any other fitness goals or details")
    current_frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)

    # Health & Limitations
    injuries_limitations = models.TextField(blank=True, help_text="Any injuries, health conditions, or physical limitations")

    # Additional Info
    message = models.TextField(blank=True, help_text="Tell us more about your goals and what you're looking for")
    referral_source = models.CharField(max_length=200, blank=True, help_text="How did you hear about us?")

    # Lead/Client Group
    GROUP_CHOICES = [
        ('lead', 'Lead'),
        ('client', 'Client'),
    ]
    group = models.CharField(max_length=10, choices=GROUP_CHOICES, default='lead', help_text="Lead or Client status")

    # Lead Status (for group='lead')
    LEAD_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('denied', 'Denied/Spam'),
    ]
    lead_status = models.CharField(max_length=20, choices=LEAD_STATUS_CHOICES, default='pending', help_text="Status when in lead group")

    # Client Status (for group='client')
    CLIENT_STATUS_CHOICES = [
        ('contacted', 'Contacted - Agreed but Not Paid'),
        ('active', 'Active - Currently Paying'),
        ('inactive', 'Inactive - Previously Paid'),
    ]
    client_status = models.CharField(max_length=20, choices=CLIENT_STATUS_CHOICES, blank=True, null=True, help_text="Status when in client group")

    notes = models.TextField(blank=True, help_text="Internal notes for trainer")

    # Approval tracking
    reviewed_at = models.DateTimeField(null=True, blank=True, help_text="When lead was reviewed")
    reviewed_by = models.CharField(max_length=100, blank=True, help_text="Admin who reviewed")
    approved_at = models.DateTimeField(null=True, blank=True, help_text="When lead was approved to become client")

    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = 'Client Inquiry'
        verbose_name_plural = 'Client Inquiries'

    def __str__(self):
        goals = self.fitness_goals.split(',')[0] if self.fitness_goals else 'No goals specified'
        return f"{self.name} - {goals}"

    def get_fitness_goals_list(self):
        """Return fitness goals as a list"""
        return [goal.strip() for goal in self.fitness_goals.split(',') if goal.strip()]


class EmailRecipient(models.Model):
    """Email recipient for alert notifications"""

    name = models.CharField(max_length=200, help_text="Recipient name (e.g., John Doe)")
    email = models.EmailField(unique=True, help_text="Email address")
    is_active = models.BooleanField(default=True, help_text="Receive emails?")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Email Recipient'
        verbose_name_plural = 'Email Recipients'

    def __str__(self):
        return f"{self.name} <{self.email}>"


class AlertType(models.Model):
    """Types of email alerts that can be sent"""

    ALERT_TYPE_CHOICES = [
        ('new_inquiry', 'New Client Inquiry Submitted'),
        ('inquiry_approved', 'Lead Approved to Client'),
        ('inquiry_denied', 'Lead Denied/Marked as Spam'),
        ('client_status_changed', 'Client Status Changed'),
        ('client_activated', 'Client Activated (Started Paying)'),
        ('client_deactivated', 'Client Deactivated (Stopped Paying)'),
    ]

    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES, unique=True)
    name = models.CharField(max_length=200, help_text="Display name for this alert")
    description = models.TextField(help_text="What triggers this alert?")
    is_active = models.BooleanField(default=True, help_text="Enable/disable this alert globally")
    recipients = models.ManyToManyField(EmailRecipient, through='AlertSubscription', related_name='alert_types')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Alert Type'
        verbose_name_plural = 'Alert Types'

    def __str__(self):
        status = "✓ Enabled" if self.is_active else "✗ Disabled"
        return f"{self.name} ({status})"

    def get_active_recipients(self):
        """Get list of active email addresses for this alert"""
        return [
            sub.recipient.email
            for sub in self.alertsubscription_set.filter(
                is_subscribed=True,
                recipient__is_active=True
            )
        ]


class AlertSubscription(models.Model):
    """Many-to-many relationship between AlertType and EmailRecipient"""

    alert_type = models.ForeignKey(AlertType, on_delete=models.CASCADE)
    recipient = models.ForeignKey(EmailRecipient, on_delete=models.CASCADE)
    is_subscribed = models.BooleanField(default=True, help_text="Receive this specific alert?")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['alert_type', 'recipient']
        verbose_name = 'Alert Subscription'
        verbose_name_plural = 'Alert Subscriptions'

    def __str__(self):
        status = "✓" if self.is_subscribed else "✗"
        return f"{status} {self.recipient.name} → {self.alert_type.name}"
