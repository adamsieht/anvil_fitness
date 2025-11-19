from django.contrib import admin
from .models import ContentBlock, Announcement, ClientInquiry, EmailRecipient, AlertType, AlertSubscription, URLPermission


@admin.register(ContentBlock)
class ContentBlockAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'page', 'title', 'order', 'is_active', 'updated_at']
    list_filter = ['page', 'is_active']
    search_fields = ['identifier', 'title', 'content']
    list_editable = ['order', 'is_active']
    ordering = ['page', 'order']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('Content Information', {
            'fields': ('page', 'identifier', 'title', 'content')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Display Settings', {
            'fields': ('order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['title', 'published_date', 'is_active', 'updated_at']
    list_filter = ['is_active', 'published_date']
    search_fields = ['title', 'content']
    list_editable = ['is_active']
    ordering = ['-published_date']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'published_date'

    fieldsets = (
        ('Announcement Information', {
            'fields': ('title', 'content', 'published_date')
        }),
        ('Display Settings', {
            'fields': ('is_active',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ClientInquiry)
class ClientInquiryAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'age', 'get_goals_display', 'fitness_level', 'group', 'get_status_display', 'submitted_at']
    list_filter = ['group', 'lead_status', 'client_status', 'fitness_level', 'current_frequency', 'submitted_at']
    search_fields = ['name', 'email', 'phone', 'fitness_goals']
    list_editable = ['group']
    ordering = ['-submitted_at']
    readonly_fields = ['submitted_at', 'updated_at', 'reviewed_at', 'approved_at']
    date_hierarchy = 'submitted_at'

    def get_goals_display(self, obj):
        """Display fitness goals in a readable format"""
        goals = obj.get_fitness_goals_list()
        if not goals:
            return 'No goals'
        # Get display names for goals
        goal_dict = dict(ClientInquiry.GOAL_CHOICES)
        display_goals = [goal_dict.get(g, g) for g in goals]
        return ', '.join(display_goals[:2]) + ('...' if len(display_goals) > 2 else '')
    get_goals_display.short_description = 'Fitness Goals'

    def get_status_display(self, obj):
        """Display current status based on group"""
        if obj.group == 'lead':
            return f"Lead: {obj.get_lead_status_display()}"
        else:
            return f"Client: {obj.get_client_status_display() if obj.client_status else 'Unknown'}"
    get_status_display.short_description = 'Status'

    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'age')
        }),
        ('Fitness Assessment', {
            'fields': ('fitness_level', 'fitness_goals', 'additional_goals', 'current_frequency')
        }),
        ('Health Information', {
            'fields': ('injuries_limitations',)
        }),
        ('Additional Information', {
            'fields': ('message', 'referral_source')
        }),
        ('Lead/Client Status', {
            'fields': ('group', 'lead_status', 'client_status', 'notes'),
            'description': 'Manage lead qualification and client activation status.'
        }),
        ('Review Tracking', {
            'fields': ('reviewed_by', 'reviewed_at', 'approved_at'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('submitted_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EmailRecipient)
class EmailRecipientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_active', 'alert_count', 'updated_at']
    list_filter = ['is_active']
    search_fields = ['name', 'email']
    list_editable = ['is_active']
    ordering = ['name']
    readonly_fields = ['created_at', 'updated_at']

    def alert_count(self, obj):
        """Show how many alerts this recipient is subscribed to"""
        count = obj.alertsubscription_set.filter(is_subscribed=True).count()
        return f"{count} alerts"
    alert_count.short_description = 'Subscriptions'

    fieldsets = (
        ('Recipient Information', {
            'fields': ('name', 'email', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


class AlertSubscriptionInline(admin.TabularInline):
    model = AlertSubscription
    extra = 1
    fields = ['recipient', 'is_subscribed']
    autocomplete_fields = ['recipient']


@admin.register(AlertType)
class AlertTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'alert_type', 'is_active', 'recipient_count', 'updated_at']
    list_filter = ['is_active', 'alert_type']
    search_fields = ['name', 'description']
    list_editable = ['is_active']
    ordering = ['name']
    readonly_fields = ['alert_type', 'created_at', 'updated_at']
    inlines = [AlertSubscriptionInline]

    def recipient_count(self, obj):
        """Show how many recipients are subscribed to this alert"""
        count = obj.alertsubscription_set.filter(is_subscribed=True, recipient__is_active=True).count()
        return f"{count} recipients"
    recipient_count.short_description = 'Active Recipients'

    fieldsets = (
        ('Alert Configuration', {
            'fields': ('alert_type', 'name', 'description', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(AlertSubscription)
class AlertSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'alert_type', 'is_subscribed', 'created_at']
    list_filter = ['is_subscribed', 'alert_type']
    search_fields = ['recipient__name', 'recipient__email', 'alert_type__name']
    list_editable = ['is_subscribed']
    ordering = ['alert_type', 'recipient']
    autocomplete_fields = ['recipient']

    fieldsets = (
        ('Subscription', {
            'fields': ('alert_type', 'recipient', 'is_subscribed')
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(URLPermission)
class URLPermissionAdmin(admin.ModelAdmin):
    list_display = ['url_pattern', 'visibility', 'description', 'is_active', 'order', 'updated_at']
    list_filter = ['visibility', 'is_active']
    search_fields = ['url_pattern', 'description']
    list_editable = ['visibility', 'is_active', 'order']
    ordering = ['order', 'url_pattern']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        ('URL Pattern', {
            'fields': ('url_pattern', 'description'),
            'description': 'Define the URL path to control. Parent URLs control child URLs (e.g., /tips/ controls /tips/1/, /tips/2/, etc.)'
        }),
        ('Permission Settings', {
            'fields': ('visibility', 'is_active', 'order'),
            'description': 'Set visibility and processing order. Lower order numbers are checked first (more specific patterns should have lower order).'
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Display message about cache clearing"""
        super().save_model(request, obj, form, change)
        self.message_user(request, f"URL permission updated. Cache cleared for immediate effect.", level='SUCCESS')
