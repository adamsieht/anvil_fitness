# Anvil Fitness - Django Website

A professional fitness website built with Django, specifically designed for fitness trainers serving adults 40+. The website focuses on promoting positive engagement with exercise and provides an informational platform to attract and retain clients.

## Features

- **Modern, Responsive Design**: Built with Bootstrap 5 and custom CSS
- **Optimized for 40+ Demographics**: Content and design tailored for mature adults
- **Professional Frontend Focus**: Emphasis on visual appeal and user experience
- **Content Management**: Django admin interface for easy content updates
- **Service Showcase**: Detailed service pages highlighting fitness offerings
- **Client Testimonials**: Social proof section with client success stories
- **Fitness Tips Blog**: Engaging content to drive traffic and establish expertise
- **Contact System**: Multiple ways for potential clients to get in touch
- **SEO Friendly**: Proper meta tags, semantic HTML structure
- **Mobile Responsive**: Optimized for all device sizes

## Project Structure

```
anvil_fitness/
├── anvil_fitness/          # Main project settings
├── fitness/                # Main fitness app
│   ├── models.py          # Service, Testimonial, FitnessTip models
│   ├── views.py           # View functions for all pages
│   ├── admin.py           # Admin configuration
│   └── urls.py            # URL routing
├── templates/             # HTML templates
│   ├── base.html          # Base template
│   └── fitness/           # App-specific templates
├── static/               # Static files
│   ├── css/              # Custom stylesheets
│   ├── js/               # JavaScript files
│   └── images/           # Image assets
└── manage_data.py        # Sample data creation script
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Django 5.1+
- Basic knowledge of Django and web development

### Installation

1. **Navigate to the project directory:**
   ```bash
   cd anvil_fitness
   ```

2. **Install Django (if not already installed):**
   ```bash
   pip install django
   ```

3. **Run migrations to set up the database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser for admin access:**
   ```bash
   python manage.py createsuperuser
   ```

5. **Load sample data (optional):**
   ```bash
   python manage_data.py
   ```

6. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

7. **Access the website:**
   - Frontend: http://localhost:8000
   - Admin Panel: http://localhost:8000/admin

## Models

### Service
- **Fields**: name, description, icon, is_featured, created_at
- **Purpose**: Showcase different fitness services offered

### Testimonial
- **Fields**: name, age, content, is_featured, created_at
- **Purpose**: Display client success stories for social proof

### FitnessTip
- **Fields**: title, content, category, created_at, is_featured
- **Purpose**: Blog-style content to engage visitors and demonstrate expertise

## Key Pages

1. **Homepage** (`/`)
   - Hero section with compelling call-to-action
   - Featured services overview
   - Client testimonials
   - Latest fitness tips

2. **About** (`/about/`)
   - Personal story and expertise
   - Certifications and experience
   - Why 40+ fitness is different
   - Core values and philosophy

3. **Services** (`/services/`)
   - Detailed service descriptions
   - Training packages and pricing
   - What's included information
   - Clear calls-to-action

4. **Fitness Tips** (`/tips/`)
   - Paginated blog-style layout
   - Category filtering
   - Individual tip detail pages
   - Newsletter signup

5. **Contact** (`/contact/`)
   - Multiple contact methods
   - Contact form with fitness-specific fields
   - FAQ section
   - Strong call-to-action

## Customization

### Branding
- Update colors in `static/css/style.css` (CSS variables at top)
- Replace placeholder images with actual photos
- Modify contact information in templates
- Update business information in footer

### Content
- Use Django admin to manage services, testimonials, and tips
- Customize page content in template files
- Add or modify service offerings as needed

### Styling
- Bootstrap 5 classes for responsive layout
- Custom CSS in `static/css/style.css`
- Font Awesome icons throughout
- Google Fonts integration (Inter)

## Deployment Considerations

1. **Static Files**: Configure `STATIC_ROOT` for production
2. **Database**: Switch from SQLite to PostgreSQL for production
3. **Environment Variables**: Use for sensitive settings
4. **Security**: Update `SECRET_KEY`, set `DEBUG = False`
5. **Media Files**: Configure media handling for user uploads

## Design Philosophy

The website is designed with the following principles:

- **Trust-Building**: Professional design that instills confidence
- **Age-Appropriate**: Content and imagery relevant to 40+ demographics  
- **Accessibility**: Easy navigation and readable fonts
- **Conversion-Focused**: Clear paths to contact and engagement
- **Content-Rich**: Valuable information that establishes expertise

## Sample Data

The `manage_data.py` script creates:
- 6 fitness services (3 featured)
- 5 client testimonials (3 featured)
- 6 fitness tips across different categories

This provides a fully populated website for demonstration and testing.

## Technical Notes

- **Framework**: Django 5.1.6
- **Frontend**: Bootstrap 5.3, Font Awesome 6.0, Google Fonts
- **Database**: SQLite (development), PostgreSQL recommended for production
- **Responsive Design**: Mobile-first approach
- **SEO**: Semantic HTML, proper meta tags, clean URLs

## Future Enhancements

Potential features to add:
- Email newsletter integration
- Contact form email handling
- Blog commenting system
- Client portal/dashboard
- Online booking system
- Payment integration
- Advanced SEO features
- Analytics integration

---

**Anvil Fitness** - *Forging Strength. Building Confidence.*