"""
Middleware to enforce URL-based permissions
"""
from django.http import Http404
from django.core.cache import cache
from django.shortcuts import redirect
from .models import URLPermission


class URLPermissionMiddleware:
    """
    Middleware to control access to URLs based on URLPermission settings

    - Checks URL permissions before processing the view
    - Supports parent URL patterns (e.g., /tips/ controls /tips/1/)
    - Caches permissions for performance
    - Respects admin exemptions for /admin/ URLs
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip permission check for admin URLs (Django admin should handle its own auth)
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Skip permission check for static/media files
        if request.path.startswith('/static/') or request.path.startswith('/media/'):
            return self.get_response(request)

        # Skip permission check for health check
        if request.path == '/health/':
            return self.get_response(request)

        # Check URL permissions
        permission_result = self.check_url_permission(request.path, request.user)

        if permission_result == 'hidden':
            # Return 404 for hidden URLs
            raise Http404("Page not found")
        elif permission_result == 'admin_required':
            # Redirect to login if not authenticated
            if not request.user.is_authenticated:
                from django.conf import settings
                from django.contrib.auth.views import redirect_to_login
                return redirect_to_login(request.get_full_path(), settings.LOGIN_URL)
            # Return 404 if authenticated but not staff (hide existence from non-admins)
            raise Http404("Page not found")

        # Permission granted, continue to view
        return self.get_response(request)

    def check_url_permission(self, path, user):
        """
        Check if user has permission to access the given URL path

        Returns:
            None: No permission rule found, allow access (default behavior)
            'hidden': URL should return 404 for everyone
            'admin_required': URL requires admin access, deny for non-admins
        """
        # Get cached permissions or fetch from database
        permissions = cache.get('url_permissions_cache')
        if permissions is None:
            permissions = list(
                URLPermission.objects.filter(is_active=True)
                .values('url_pattern', 'visibility', 'order')
                .order_by('order', 'url_pattern')
            )
            cache.set('url_permissions_cache', permissions, 60 * 15)  # Cache for 15 minutes

        # Check each permission rule in order
        for perm in permissions:
            pattern = perm['url_pattern']

            # Check if the current path matches or starts with this pattern
            # This allows parent URLs to control child URLs
            # e.g., /tips/ controls /tips/1/, /tips/2/, etc.
            if path == pattern or path.startswith(pattern):
                visibility = perm['visibility']

                if visibility == 'hidden':
                    # URL should be hidden from everyone (404)
                    return 'hidden'

                elif visibility == 'admin_only':
                    # URL requires admin access
                    if user.is_authenticated and (user.is_staff or user.is_superuser):
                        # User is admin, allow access
                        return None
                    else:
                        # User is not admin, deny access
                        return 'admin_required'

                elif visibility == 'public':
                    # URL is public, allow access
                    return None

                # If we matched a pattern, don't check further
                # (this is why order matters)
                break

        # No matching permission rule found, allow access by default
        return None
