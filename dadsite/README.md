# Anvil Fitness Website

A production-ready Django website for Anvil Fitness personal training business with Docker deployment.

## Features

- Django 5.0 backend
- SQLite database with persistent volumes
- Tailwind CSS for modern, responsive design
- Caddy reverse proxy with health checks
- Editable content blocks through admin panel
- Contact form with email notifications
- Announcements/updates section
- Health check endpoint for monitoring
- Structured logging with rotation

## Project Structure

```
dadsite/
├── dadsite/              # Django project settings
├── pages/                # Main application
│   ├── models.py         # ContentBlock and Announcement models
│   ├── views.py          # Page views and health check
│   ├── forms.py          # Contact form
│   ├── admin.py          # Admin configuration
│   └── templates/        # HTML templates
├── static/               # Static files
├── media/                # User-uploaded media
├── logs/                 # Application logs
├── db/                   # SQLite database (created on first run)
├── Dockerfile            # Django container
├── docker-compose.yml    # Docker orchestration
├── Caddyfile             # Caddy configuration
└── entrypoint.sh         # Container startup script
```

## Quick Start

### 1. Clone and Setup

```bash
cd dadsite
cp .env.example .env
```

### 2. Configure Environment

Edit `.env` with your settings:

```bash
# Generate a secure secret key
DJANGO_SECRET_KEY=your-random-secret-key-here

# Production settings
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Email configuration (example: Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
CONTACT_EMAIL=contact@yourdomain.com
```

### 3. Build and Run

```bash
# Build and start all containers
docker-compose up -d --build

# Check logs
docker-compose logs -f
```

### 4. Create Admin User

```bash
docker-compose exec web python manage.py createsuperuser
```

### 5. Access the Site

- Website: http://localhost
- Admin Panel: http://localhost/admin
- Health Check: http://localhost/health/

## Managing Content

### Content Blocks

1. Log into admin panel at `/admin`
2. Navigate to "Content Blocks"
3. Add new blocks with:
   - Page selection (Home, About, Services)
   - Unique identifier
   - Title and content
   - Optional image
   - Display order

### Announcements

1. Navigate to "Announcements" in admin
2. Create updates with title, content, and publish date
3. Toggle visibility with "is_active" checkbox

## Production Deployment

### VPS Setup (Ubuntu)

```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin
```

### Deploy Application

```bash
# Clone repository
git clone <your-repo-url>
cd dadsite

# Setup environment
cp .env.example .env
nano .env  # Edit with production values

# Build and run
docker-compose up -d --build

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

### Enable HTTPS

Edit `Caddyfile` and replace `:80` with your domain:

```
yourdomain.com {
    # Caddy automatically provisions SSL certificates

    handle /static/* {
        root * /app
        file_server
    }

    handle /media/* {
        root * /app
        file_server
    }

    reverse_proxy web:8000 {
        health_uri /health/
        health_interval 30s
        health_timeout 10s
    }
}
```

Then restart:

```bash
docker-compose restart caddy
```

## Common Commands

```bash
# View logs
docker-compose logs -f web
docker-compose logs -f caddy

# Restart services
docker-compose restart web
docker-compose restart caddy

# Run migrations
docker-compose exec web python manage.py migrate

# Collect static files
docker-compose exec web python manage.py collectstatic --noinput

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Access Django shell
docker-compose exec web python manage.py shell

# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes database)
docker-compose down -v
```

## Backup Database

```bash
# Backup SQLite database
docker-compose exec web cp /app/db/db.sqlite3 /app/db/backup-$(date +%Y%m%d).sqlite3

# Copy to host
docker cp anvilfitness_web:/app/db/backup-$(date +%Y%m%d).sqlite3 ./
```

## Monitoring

- Health check endpoint: `/health/`
- Application logs: `./logs/django.log`
- Container logs: `docker-compose logs`

## Troubleshooting

### Site not loading

```bash
# Check container status
docker-compose ps

# Check logs
docker-compose logs web
docker-compose logs caddy

# Verify health check
curl http://localhost/health/
```

### Static files not showing

```bash
# Recollect static files
docker-compose exec web python manage.py collectstatic --noinput
docker-compose restart caddy
```

### Email not sending

1. Verify SMTP credentials in `.env`
2. For Gmail, use App Passwords (not regular password)
3. Check logs: `docker-compose logs web | grep -i email`

## Tech Stack

- **Backend**: Django 5.0, Python 3.12
- **Database**: SQLite with persistent volume
- **Server**: Gunicorn (3 workers)
- **Reverse Proxy**: Caddy 2
- **Frontend**: Django templates + Tailwind CSS
- **Deployment**: Docker + Docker Compose

## License

Private use.
