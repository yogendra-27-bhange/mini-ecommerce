# Mini E-commerce Website

A simple Mini E-commerce Website built using Python Flask and MySQL with HTML, CSS, and JavaScript frontend.

## Features
- Product listing with details
- Add to cart functionality
- Cart view and checkout process
- Admin panel to add, edit, delete products
- Simple order history tracking

## Tech Stack
- Backend: Flask (Python)
- Database: MySQL
- Frontend: HTML, CSS, JavaScript

## Setup Instructions

1. Install Python packages:

2. Setup MySQL database:
- Run the `schema.sql` script to create `ecommerce` database and tables.

3. Run the Flask app:
python app.py

4. Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- Visit `/` to see products
- Add products to cart and checkout
- Admin page at `/admin` to manage products

## Deployment Notes
- Set environment variables for security:
  - `SECRET_KEY` (Flask secret key)
  - `DB_HOST`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` (MySQL config)
- Never use debug mode in production.
- Use a production server (e.g., Gunicorn/Waitress + Nginx/Apache).
- Install dependencies from `requirements.txt` (see below).

## Creating requirements.txt
Run this command to generate requirements:
```
pip freeze > requirements.txt
```

---

Feel free to customize and extend this project!


