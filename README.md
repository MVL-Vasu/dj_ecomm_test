# Django Ecommerce Website

A beautiful and modern ecommerce website built with Django and Tailwind CSS.

## Features

- **Product Management**: Categories, products, reviews, and ratings
- **Shopping Cart**: Add, remove, and update cart items
- **Order Management**: Complete checkout process and order tracking
- **User Accounts**: Registration, login, and profile management
- **Responsive Design**: Built with Tailwind CSS for modern, mobile-first design
- **Admin Interface**: Django admin for easy content management

## Project Structure

```
ecommerce-django/
├── accounts/          # User authentication and profiles
├── cart/              # Shopping cart functionality
├── ecommerce/         # Main project settings
├── orders/            # Order processing and management
├── products/          # Product catalog and reviews
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates (to be created)
├── media/             # User-uploaded files
├── manage.py          # Django management script
└── requirements.txt   # Python dependencies
```

## Models

### Products App
- **Category**: Product categories with slugs and images
- **Product**: Full product details with pricing, inventory, and images
- **ProductReview**: Customer reviews and ratings

### Cart App
- **Cart**: User shopping carts (supports both authenticated and anonymous users)
- **CartItem**: Individual items in the cart

### Orders App
- **Order**: Complete order information with billing/shipping details
- **OrderItem**: Individual items in an order (with historical pricing)

### Accounts App
- **UserProfile**: Extended user information and preferences

## Getting Started

1. **Install Dependencies**: Install Django and Pillow globally or in a virtual environment
2. **Run Migrations**: `python manage.py migrate`
3. **Create Superuser**: `python manage.py createsuperuser`
4. **Run Development Server**: `python manage.py runserver`
5. **Build Tailwind CSS**: `npm run build-css-prod` (for production) or `npm run build-css` (for development with watch mode)

## Admin Access

Access the Django admin at `http://localhost:8000/admin/` with your superuser credentials.

## Tech Stack

- **Backend**: Django 5.2+
- **Frontend**: HTML, CSS (Tailwind CSS), JavaScript
- **Database**: SQLite (development)
- **Image Processing**: Pillow
- **Package Management**: npm (for Tailwind CSS)

## Next Steps

- Create beautiful HTML templates with Tailwind CSS
- Implement product catalog views
- Add shopping cart functionality
- Create checkout and payment processing
- Add user authentication views
- Implement search and filtering
- Add email notifications
- Set up production deployment

## License

This project is open source and available under the MIT License.
