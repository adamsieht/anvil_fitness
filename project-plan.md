Claude-Optimized Project Plan (Machine Format)

project_name: anvil_fitness
framework: django
database_local: sqlite
database_prod: sqlite
frontend: django_templates + tailwind
deployment_target: render_or_railway

apps:

main

blog

calendar_app

onboarding

app_definitions:

main:
pages:
- home
- about
- contact
requirements:
- base template layout
- header + footer
- navigation partial
- responsive design

blog:
model: Post
fields:
- title:str
- slug:str(unique)
- content:text
- image:file(optional)
- category:str (values: workout,nutrition,recipe)
- created_at:datetime(auto)
views:
- list_posts
- view_post
- category_filter
- search
templates:
- post_list
- post_detail
admin: full_crud

calendar_app:
model: WorkoutEvent
fields:
- date:date
- title:str
- description:text(optional)
- client_name:str(optional)
views:
- monthly_calendar
- daily_event_list
templates:
- calendar_month
- events_for_day
admin: full_crud

onboarding:
model: ClientIntake
fields:
- name:str
- email:str
- goals:text
- injuries:text(optional)
- schedule:str
- experience:str
- notes:text(optional)
views:
- intake_form
- intake_success
templates:
- intake_form
- intake_success
admin: read_only or full_crud (either acceptable)
email_optional: send_email_to_trainer

pages:
home:
components:
- hero_section
- trainer_intro
- links_to_blog
- link_to_onboarding
- testimonials_static
about:
components:
- trainer_photo
- training_philosophy
- services_list
- pricing_blocks
- cta_button
blog:
components:
- paginated_list
- category_filters
- search_bar
- detail_page_with_images
calendar:
components:
- full_month_grid
- clickable_days
- events_display
onboarding:
components:
- multi_field_form
- success_screen

ui_requirements:

mobile_first

consistent_spacing

simple_color_theme

template_inheritance (base.html → page templates)

readable typography

recipes visually distinct

auth:

only_admin_login

no_user_accounts_for_clients_initially

deployment_requirements:

production_settings_file

environment_variable_support

whitenoise_or_staticfiles_all_set

postgres_config

instructions_for_render_or_railway

deliverables:

full_django_project_with_all_apps

complete_models_views_urls_admin_templates

working_tailwind_or_bootstrap_setup

ready_for_local_run

ready_for_production_deploy

filetree_output

explicit_file_contents

no_stub_placeholders

generation_instructions_for_claude:

generate full code files

include migrations if able

ensure imports resolve

ensure folder structure is consistent

do not output snippets; output full file contents

assume user will paste final output directly into VS Code

always include settings.py, urls.py, wsgi/asgi files, templates, and static config

avoid commentary unless needed for clarity