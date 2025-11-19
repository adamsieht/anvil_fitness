"""
Management command to auto-discover URLs and populate URLPermission table
"""
from django.core.management.base import BaseCommand
from django.urls import get_resolver
from pages.models import URLPermission
import re


class Command(BaseCommand):
    help = 'Auto-discover all URLs in the project and create URLPermission entries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--update',
            action='store_true',
            help='Update descriptions for existing permissions',
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Discovering URLs in project...'))

        # Get all URL patterns
        url_patterns = self.get_all_urls()

        created_count = 0
        updated_count = 0
        skipped_count = 0

        for url_info in url_patterns:
            url_pattern = url_info['pattern']
            description = url_info['description']

            # Check if permission already exists
            permission, created = URLPermission.objects.get_or_create(
                url_pattern=url_pattern,
                defaults={
                    'visibility': 'public',
                    'description': description,
                    'is_active': True,
                    'order': 100,  # Default to low priority
                }
            )

            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'  ✅ Created: {url_pattern} - {description}')
                )
            elif options['update'] and permission.description != description:
                permission.description = description
                permission.save()
                updated_count += 1
                self.stdout.write(
                    self.style.WARNING(f'  📝 Updated: {url_pattern} - {description}')
                )
            else:
                skipped_count += 1
                self.stdout.write(
                    self.style.HTTP_INFO(f'  ⏭️  Skipped: {url_pattern} (already exists)')
                )

        # Summary
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'📊 Summary:'))
        self.stdout.write(self.style.SUCCESS(f'  ✅ Created: {created_count}'))
        if options['update']:
            self.stdout.write(self.style.SUCCESS(f'  📝 Updated: {updated_count}'))
        self.stdout.write(self.style.SUCCESS(f'  ⏭️  Skipped: {skipped_count}'))
        self.stdout.write(self.style.SUCCESS(f'  📋 Total URLs: {len(url_patterns)}'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        self.stdout.write(
            self.style.SUCCESS('✨ All URLs populated! Go to Django Admin → URL Permissions to set visibility.')
        )

    def get_all_urls(self):
        """
        Get all URL patterns from the URLconf, excluding parameter-based URLs
        """
        url_patterns = []
        resolver = get_resolver()

        # Get patterns from the resolver
        patterns = self.extract_patterns(resolver.url_patterns, prefix='')

        # Process patterns to create URLPermission entries
        for pattern, name in patterns:
            # Skip if pattern has URL parameters
            if self.has_url_parameters(pattern):
                # Create base pattern without parameters
                base_pattern = self.get_base_pattern(pattern)
                if base_pattern and base_pattern not in [p['pattern'] for p in url_patterns]:
                    url_patterns.append({
                        'pattern': base_pattern,
                        'description': f'Base URL for {name or "unnamed"}',
                    })
            else:
                # Add clean pattern
                if pattern not in [p['pattern'] for p in url_patterns]:
                    url_patterns.append({
                        'pattern': pattern,
                        'description': self.get_description(name, pattern),
                    })

        return url_patterns

    def extract_patterns(self, urlpatterns, prefix=''):
        """
        Recursively extract URL patterns from URLconf
        """
        patterns = []

        for pattern in urlpatterns:
            # Get the pattern string
            pattern_str = str(pattern.pattern)

            # Build full pattern
            full_pattern = prefix + pattern_str

            # Handle included URLconfs
            if hasattr(pattern, 'url_patterns'):
                # Recursively get patterns from included URLconf
                patterns.extend(
                    self.extract_patterns(pattern.url_patterns, prefix=full_pattern)
                )
            else:
                # Add this pattern
                # Clean up pattern (remove regex characters)
                clean_pattern = self.clean_pattern(full_pattern)
                if clean_pattern:
                    patterns.append((clean_pattern, getattr(pattern, 'name', None)))

        return patterns

    def clean_pattern(self, pattern):
        """
        Clean URL pattern by removing regex anchors and converting to path format
        """
        # Remove ^ and $ anchors
        pattern = pattern.replace('^', '').replace('$', '')

        # Ensure starts with /
        if not pattern.startswith('/'):
            pattern = '/' + pattern

        # Remove trailing / for consistency (except root)
        if pattern != '/' and pattern.endswith('/'):
            pattern = pattern.rstrip('/')

        # Add trailing / back for directory-like paths
        if '.' not in pattern.split('/')[-1]:  # Not a file
            pattern = pattern + '/'

        return pattern

    def has_url_parameters(self, pattern):
        """
        Check if URL pattern contains parameters like <int:pk>, <slug:slug>, etc.
        """
        return bool(re.search(r'<[^>]+>', pattern))

    def get_base_pattern(self, pattern):
        """
        Extract base pattern from parameterized URL
        e.g., /tips/<int:pk>/ -> /tips/
        """
        # Remove everything from first < onwards
        base = re.sub(r'<[^>]+>.*$', '', pattern)

        # Ensure it ends with /
        if not base.endswith('/'):
            base += '/'

        return base if len(base) > 1 else None

    def get_description(self, name, pattern):
        """
        Generate a friendly description based on URL name or pattern
        """
        if name:
            # Convert underscores to spaces and title case
            return name.replace('_', ' ').title()

        # Generate from pattern
        parts = [p for p in pattern.split('/') if p]
        if parts:
            return ' '.join(parts).title() + ' Page'

        return 'Root Page' if pattern == '/' else 'Page'
