# Generated migration for URLPermission model

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='URLPermission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_pattern', models.CharField(help_text="URL pattern (e.g., '/about/', '/manage/', '/tips/'). Child URLs inherit permissions (e.g., '/tips/' controls '/tips/1/', '/tips/2/')", max_length=200, unique=True)),
                ('visibility', models.CharField(choices=[('public', 'Visible to Everyone'), ('admin_only', 'Visible to Admin Only'), ('hidden', 'Visible to Nobody (404)')], default='public', help_text='Control who can access this URL', max_length=20)),
                ('description', models.CharField(blank=True, help_text='Description of what this URL is for', max_length=200)),
                ('is_active', models.BooleanField(default=True, help_text='Enable/disable this permission rule')),
                ('order', models.IntegerField(default=0, help_text='Processing order (lower numbers processed first). More specific patterns should have lower order.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'URL Permission',
                'verbose_name_plural': 'URL Permissions',
                'ordering': ['order', 'url_pattern'],
            },
        ),
    ]
