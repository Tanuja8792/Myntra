# Myntra – Fashion & Lifestyle Shopping App

A Myntra-inspired educational e-commerce project. The original static HTML/CSS/JavaScript storefront is retained on the `main` branch. The Django + MySQL upgrade is being developed on the `django-upgrade` branch.

## Current Django features

- Separate homepage and collections page.
- Category-specific product listings and product detail pages.
- Django signup and login.
- Session-based shopping bag.
- Checkout with Cash on Delivery demo orders.
- Saved order history and Django admin management.
- Order confirmation email support (SMTP configuration required).
- MySQL configuration through environment variables; SQLite is used by default for the first local run.

## Technology

- Python and Django
- MySQL (configurable; SQLite default for initial setup)
- HTML, CSS
- Django authentication and email framework

## Project setup (Windows)

1. Install Python 3.11 or newer and MySQL Server 8.
2. Clone this repository and switch to the `django-upgrade` branch:
   ```bash
   git clone https://github.com/Tanuja8792/Myntra.git
   cd Myntra
   git checkout django-upgrade
   ```
3. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Copy `.env.example` to `.env`. For the first run, keep `DB_ENGINE=sqlite`.
6. Create database tables and sample products:
   ```bash
   python manage.py makemigrations shop
   python manage.py migrate
   python manage.py seed_demo_data
   python manage.py createsuperuser
   python manage.py runserver
   ```
7. Open http://127.0.0.1:8000/ . Admin is at http://127.0.0.1:8000/admin/.

## Enable MySQL

Create a database named `myntra_db` in MySQL, update `.env` with `DB_ENGINE=mysql`, your database username/password, host and port, then run `python manage.py migrate`.

## Enable Gmail order emails

For local testing, the default console email backend prints the email in the terminal. To send real emails, configure Gmail SMTP in your private `.env` using a Google App Password (not your normal Gmail password), set `EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend`, and never commit `.env` to GitHub.

## Important

This is an educational demo. COD orders are recorded in the database; no real payment is processed. Email delivery depends on correct SMTP configuration. Product catalogue entries and prices are sample data. AI tools, real payment gateway, courier integration, stock reservation under high traffic, and production deployment/security hardening are future work.

## Author

Tanuja Achari
