import logging
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.utils import timezone
from .models import ContentBlock, Announcement, ClientInquiry
from .forms import ClientInquiryForm
from .email_alerts import send_alert_email

logger = logging.getLogger(__name__)


def is_staff_user(user):
    """Check if user is staff/admin"""
    return user.is_staff or user.is_superuser


def home(request):
    """Home page view"""
    content_blocks = ContentBlock.objects.filter(page='home', is_active=True)
    announcements = Announcement.objects.filter(is_active=True)[:3]

    context = {
        'content_blocks': content_blocks,
        'announcements': announcements,
    }
    return render(request, 'home.html', context)


def about(request):
    """About page view"""
    content_blocks = ContentBlock.objects.filter(page='about', is_active=True)

    context = {
        'content_blocks': content_blocks,
    }
    return render(request, 'about.html', context)


def services(request):
    """Services page view"""
    content_blocks = ContentBlock.objects.filter(page='services', is_active=True)

    context = {
        'content_blocks': content_blocks,
    }
    return render(request, 'services.html', context)


def client_portal(request):
    """Client portal page with PT Distinction integration"""
    return render(request, 'client_portal.html')


def contact(request):
    """Contact page view with client onboarding form"""
    if request.method == 'POST':
        form = ClientInquiryForm(request.POST)
        if form.is_valid():
            # Save the client inquiry to database
            inquiry = form.save()

            # Construct email notification
            email_subject = f"New Client Inquiry: {inquiry.name}"
            email_message = f"""
New client onboarding inquiry received:

CONTACT INFORMATION:
Name: {inquiry.name}
Email: {inquiry.email}
Phone: {inquiry.phone or 'Not provided'}
Age: {inquiry.age or 'Not provided'}

FITNESS INFORMATION:
Current Fitness Level: {inquiry.get_fitness_level_display()}
Fitness Goals: {', '.join([dict(inquiry.GOAL_CHOICES).get(goal, goal) for goal in inquiry.get_fitness_goals_list()])}
Additional Goals: {inquiry.additional_goals or 'None specified'}
Current Exercise Frequency: {inquiry.get_current_frequency_display()}

HEALTH INFORMATION:
Injuries/Limitations: {inquiry.injuries_limitations or 'None reported'}

ADDITIONAL INFORMATION:
Message: {inquiry.message or 'No additional message'}
Referral Source: {inquiry.referral_source or 'Not specified'}

---
Submitted: {inquiry.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}
View in admin panel to update status and add notes.
"""

            # Send email alert to distribution list
            success, recipients, error = send_alert_email(
                'new_inquiry',
                email_subject,
                email_message,
                fail_silently=True
            )

            if success:
                messages.success(request, 'Thank you for your interest! We will contact you within 24 hours to begin your transformation.')
                logger.info(f"Client inquiry submitted by {inquiry.email} (ID: {inquiry.id}) - Email sent to {len(recipients)} recipients")
            else:
                messages.success(request, 'Thank you for your interest! We will contact you within 24 hours to begin your transformation.')
                logger.warning(f"Client inquiry submitted by {inquiry.email} (ID: {inquiry.id}) - Email not sent: {error}")

            return redirect('contact')
    else:
        form = ClientInquiryForm()

    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


@require_http_methods(["GET"])
def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Check database connectivity
        ContentBlock.objects.count()

        return JsonResponse({
            'status': 'healthy',
            'database': 'ok',
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
        }, status=503)


# Admin Views

@login_required
@user_passes_test(is_staff_user)
def manage_dashboard(request):
    """Main management dashboard with links to all admin pages"""
    # Get summary statistics
    total_pending_leads = ClientInquiry.objects.filter(group='lead', lead_status='pending').count()
    total_approved_leads = ClientInquiry.objects.filter(group='lead', lead_status='approved').count()
    total_denied_leads = ClientInquiry.objects.filter(group='lead', lead_status='denied').count()

    all_clients = ClientInquiry.objects.filter(group='client')
    total_clients = all_clients.count()
    total_active = all_clients.filter(client_status='active').count()
    total_contacted = all_clients.filter(client_status='contacted').count()
    total_inactive = all_clients.filter(client_status='inactive').count()

    context = {
        'total_pending_leads': total_pending_leads,
        'total_approved_leads': total_approved_leads,
        'total_denied_leads': total_denied_leads,
        'total_clients': total_clients,
        'total_active': total_active,
        'total_contacted': total_contacted,
        'total_inactive': total_inactive,
    }
    return render(request, 'admin/dashboard.html', context)


@login_required
@user_passes_test(is_staff_user)
def admin_pending_inquiries(request):
    """Admin page to review pending lead inquiries"""
    pending_leads = ClientInquiry.objects.filter(group='lead', lead_status='pending').order_by('-submitted_at')

    context = {
        'inquiries': pending_leads,
        'total_pending': pending_leads.count(),
    }
    return render(request, 'admin/pending_inquiries.html', context)


@login_required
@user_passes_test(is_staff_user)
def admin_active_clients(request):
    """Admin page to view all clients"""
    all_clients = ClientInquiry.objects.filter(group='client').order_by('-submitted_at')

    # Get counts for dashboard
    total_clients = all_clients.count()
    total_active = all_clients.filter(client_status='active').count()
    total_inactive = all_clients.filter(client_status='inactive').count()
    total_contacted = all_clients.filter(client_status='contacted').count()
    total_pending_leads = ClientInquiry.objects.filter(group='lead', lead_status='pending').count()

    context = {
        'clients': all_clients,
        'total_clients': total_clients,
        'total_active': total_active,
        'total_inactive': total_inactive,
        'total_contacted': total_contacted,
        'total_pending_leads': total_pending_leads,
    }
    return render(request, 'admin/active_clients.html', context)


@login_required
@user_passes_test(is_staff_user)
@require_POST
def approve_inquiry(request, inquiry_id):
    """Approve a lead and convert to client"""
    inquiry = get_object_or_404(ClientInquiry, id=inquiry_id)

    # Move from lead to client group
    inquiry.group = 'client'
    inquiry.lead_status = 'approved'
    inquiry.client_status = 'contacted'  # Default to contacted when approved
    inquiry.reviewed_at = timezone.now()
    inquiry.approved_at = timezone.now()
    inquiry.reviewed_by = request.user.username if request.user.is_authenticated else 'admin'
    inquiry.save()

    # Send email alert
    send_alert_email(
        'inquiry_approved',
        f"Lead Approved: {inquiry.name}",
        f"{inquiry.name} ({inquiry.email}) has been approved and converted to a client.\n\nApproved by: {inquiry.reviewed_by}\nStatus: Contacted (awaiting payment)",
        fail_silently=True
    )

    messages.success(request, f'Approved {inquiry.name} and moved to Clients group with status "Contacted".')
    logger.info(f"Lead {inquiry.id} approved and converted to client by {request.user.username}")

    return redirect('admin_pending_inquiries')


@login_required
@user_passes_test(is_staff_user)
@require_POST
def deny_inquiry(request, inquiry_id):
    """Deny a lead inquiry (mark as spam)"""
    inquiry = get_object_or_404(ClientInquiry, id=inquiry_id)

    inquiry.lead_status = 'denied'
    inquiry.reviewed_at = timezone.now()
    inquiry.reviewed_by = request.user.username if request.user.is_authenticated else 'admin'
    inquiry.save()

    # Send email alert
    send_alert_email(
        'inquiry_denied',
        f"Lead Denied: {inquiry.name}",
        f"{inquiry.name} ({inquiry.email}) has been marked as spam/denied.\n\nDenied by: {inquiry.reviewed_by}",
        fail_silently=True
    )

    messages.warning(request, f'Denied lead from {inquiry.name}. Marked as spam.')
    logger.info(f"Lead {inquiry.id} denied by {request.user.username}")

    return redirect('admin_pending_inquiries')


@login_required
@user_passes_test(is_staff_user)
@require_POST
def update_client_status(request, inquiry_id):
    """Update client activation status"""
    inquiry = get_object_or_404(ClientInquiry, id=inquiry_id)
    old_status = inquiry.client_status
    new_status = request.POST.get('client_status')

    if inquiry.group != 'client':
        messages.error(request, 'This person is not a client yet.')
        return redirect('admin_pending_inquiries')

    if new_status in ['contacted', 'active', 'inactive']:
        inquiry.client_status = new_status
        inquiry.save()

        # Send different alerts based on status change
        if new_status == 'active' and old_status != 'active':
            # Client activated (started paying)
            send_alert_email(
                'client_activated',
                f"Client Activated: {inquiry.name}",
                f"{inquiry.name} ({inquiry.email}) is now an active paying client.\n\nUpdated by: {request.user.username}",
                fail_silently=True
            )
        elif new_status == 'inactive' and old_status == 'active':
            # Client deactivated (stopped paying)
            send_alert_email(
                'client_deactivated',
                f"Client Deactivated: {inquiry.name}",
                f"{inquiry.name} ({inquiry.email}) has been deactivated (no longer paying).\n\nUpdated by: {request.user.username}",
                fail_silently=True
            )
        else:
            # General status change
            send_alert_email(
                'client_status_changed',
                f"Client Status Changed: {inquiry.name}",
                f"{inquiry.name} ({inquiry.email}) status changed from {old_status or 'None'} to {new_status}.\n\nUpdated by: {request.user.username}",
                fail_silently=True
            )

        messages.success(request, f'Updated {inquiry.name} status to {inquiry.get_client_status_display()}.')
        logger.info(f"Client {inquiry.id} status updated to {new_status} by {request.user.username}")
    else:
        messages.error(request, 'Invalid status.')

    return redirect('admin_active_clients')


# Keep for backward compatibility but redirect to update_client_status
@login_required
@user_passes_test(is_staff_user)
@require_POST
def onboard_client(request, inquiry_id):
    """Legacy endpoint - redirects to update client status"""
    return update_client_status(request, inquiry_id)
