# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

This is a Django-based ecommerce website with Tailwind CSS for styling. The project uses a modular app structure with separate apps for products, cart, orders, and user accounts.

## Architecture

The project follows Django's MVT (Model-View-Template) pattern with these core apps:

- **products**: Product catalog, categories, and reviews
- **cart**: Shopping cart functionality for authenticated and anonymous users
- **orders**: Order processing and management with complete billing/shipping details
- **accounts**: User authentication and profile management with default addresses
- **ecommerce**: Main project configuration and URL routing

### Key Model Relationships

- Products belong to Categories (ForeignKey)
- Products can have multiple Reviews (One-to-Many)
- Cart supports both authenticated users (OneToOne with User) and anonymous users (session-based)
- Orders store historical product data to maintain pricing integrity
- UserProfile extends Django's User model with address defaults and preferences

## Development Commands

### Initial Setup
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node.js dependencies for Tailwind
npm install

# Run database migrations
python manage.py migrate

# Create superuser for admin access
python manage.py createsuperuser
```

### Development Server
```bash
# Start Django development server
python manage.py runserver

# Build Tailwind CSS (development with watch mode)
npm run build-css

# Build Tailwind CSS (production - minified)
npm run build-css-prod
```

### Database Operations
```bash
# Create new migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset specific app migrations (if needed)
python manage.py migrate <app_name> zero
python manage.py migrate <app_name>
```

### Testing
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test <app_name>

# Run specific test case
python manage.py test <app_name>.tests.<TestClassName>

# Run with verbose output
python manage.py test --verbosity=2
```

### Admin and Data Management
```bash
# Access Django shell
python manage.py shell

# Load fixture data (if available)
python manage.py loaddata <fixture_name>

# Create fixture from existing data
python manage.py dumpdata <app_name> > fixtures/<fixture_name>.json
```

### Static Files and Media
```bash
# Collect static files for production
python manage.py collectstatic

# Clear collected static files
python manage.py collectstatic --clear
```

## Key Features

### Product Management
- Categories with slugs and images
- Products with inventory tracking, pricing, and multiple images
- Customer reviews with verified purchase status
- Automatic slug generation and SKU assignment

### Shopping Cart
- Supports both authenticated and anonymous users
- Session-based cart for guests
- Automatic cart merging on user login
- Real-time price calculations

### Order Processing
- Complete billing and shipping address capture
- Historical product data preservation
- Order status and payment status tracking
- UUID-based order numbers for security

### User Accounts
- Extended user profiles with default addresses
- Newsletter and notification preferences
- Avatar uploads and personal information

## Database Configuration

- Development: SQLite (db.sqlite3)
- Models use proper indexing for performance
- Automatic timestamp tracking on all major models

## Static Files Structure

- **Input CSS**: `static/css/input.css`
- **Output CSS**: `static/css/output.css`
- **Media uploads**: `media/` directory
- **Static files**: `static/` directory

## URL Structure

- Root (`/`): Products app (product catalog)
- `/admin/`: Django admin interface
- `/cart/`: Shopping cart operations
- `/orders/`: Order management
- `/accounts/`: User authentication and profiles

## Tailwind CSS Configuration

The project uses Tailwind CSS v4+ with custom primary color scheme (blue variants). The configuration scans all Python and HTML files across all apps for Tailwind classes.

## Development Notes

- All models include created_at/updated_at timestamps
- Products and Categories auto-generate slugs from names
- Cart items automatically delete when quantity reaches zero
- Order items preserve product data at time of purchase
- User profiles are automatically created via Django signals
