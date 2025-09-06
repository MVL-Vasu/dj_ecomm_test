from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from products.models import Category, Product, ProductReview
from decimal import Decimal
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate database with sample data...'))

        # Create categories
        categories_data = [
            {
                'name': 'Electronics',
                'description': 'Latest gadgets, smartphones, laptops, and electronic accessories for modern living.',
            },
            {
                'name': 'Fashion & Clothing',
                'description': 'Trendy clothing, shoes, and accessories for men, women, and kids.',
            },
            {
                'name': 'Home & Garden',
                'description': 'Everything for your home, garden, furniture, and home improvement.',
            },
            {
                'name': 'Sports & Fitness',
                'description': 'Sports equipment, fitness gear, and outdoor recreation products.',
            },
            {
                'name': 'Books & Media',
                'description': 'Books, audiobooks, movies, music, and educational materials.',
            },
            {
                'name': 'Health & Beauty',
                'description': 'Skincare, cosmetics, health supplements, and wellness products.',
            },
            {
                'name': 'Toys & Games',
                'description': 'Toys, board games, video games, and entertainment for all ages.',
            },
            {
                'name': 'Automotive',
                'description': 'Car accessories, tools, and automotive maintenance products.',
            }
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create products for each category
        # Using placeholder images from picsum.photos for demonstration
        products_data = {
            'Electronics': [
                {
                    'name': 'iPhone 15 Pro Max',
                    'description': 'The latest iPhone with titanium design, A17 Pro chip, and advanced camera system. Features USB-C connectivity and action button.',
                    'price': Decimal('1199.99'),
                    'compare_price': Decimal('1299.99'),
                    'stock_quantity': 25,
                    'is_featured': True,
                    'weight': Decimal('0.5'),
                    'dimensions': '6.3 x 3.0 x 0.3 inches'
                },
                {
                    'name': 'Samsung Galaxy S24 Ultra',
                    'description': 'Premium Android smartphone with S Pen, 200MP camera, and AI-powered features. Perfect for productivity and creativity.',
                    'price': Decimal('1099.99'),
                    'compare_price': Decimal('1199.99'),
                    'stock_quantity': 18,
                    'is_featured': True,
                    'weight': Decimal('0.6'),
                    'dimensions': '6.4 x 3.1 x 0.3 inches'
                },
                {
                    'name': 'MacBook Air M3',
                    'description': 'Ultra-thin laptop with Apple M3 chip, 13.6-inch Liquid Retina display, and all-day battery life. Perfect for students and professionals.',
                    'price': Decimal('1299.99'),
                    'stock_quantity': 12,
                    'is_featured': True,
                    'weight': Decimal('2.7'),
                    'dimensions': '11.97 x 8.46 x 0.44 inches'
                },
                {
                    'name': 'Sony WH-1000XM5 Headphones',
                    'description': 'Industry-leading noise canceling wireless headphones with 30-hour battery life and premium sound quality.',
                    'price': Decimal('399.99'),
                    'compare_price': Decimal('449.99'),
                    'stock_quantity': 35,
                    'weight': Decimal('0.5'),
                    'dimensions': '10.2 x 8.9 x 3.1 inches'
                },
                {
                    'name': 'iPad Pro 12.9"',
                    'description': 'The ultimate iPad experience with M2 chip, Liquid Retina XDR display, and support for Apple Pencil.',
                    'price': Decimal('1099.99'),
                    'stock_quantity': 22,
                    'weight': Decimal('1.5'),
                    'dimensions': '11.04 x 8.46 x 0.25 inches'
                }
            ],
            'Fashion & Clothing': [
                {
                    'name': 'Nike Air Jordan 1 Retro',
                    'description': 'Iconic basketball shoes with premium leather construction and classic colorway. A timeless sneaker for style and comfort.',
                    'price': Decimal('170.00'),
                    'stock_quantity': 45,
                    'is_featured': True,
                    'weight': Decimal('2.0'),
                    'dimensions': '13 x 5 x 5 inches'
                },
                {
                    'name': 'Levi\'s 501 Original Jeans',
                    'description': 'The original straight fit jeans. Made with premium denim and classic five-pocket styling.',
                    'price': Decimal('59.99'),
                    'compare_price': Decimal('89.99'),
                    'stock_quantity': 60,
                    'weight': Decimal('1.2'),
                    'dimensions': '12 x 10 x 2 inches'
                },
                {
                    'name': 'Patagonia Down Jacket',
                    'description': 'Lightweight, packable down jacket perfect for outdoor adventures. Water-resistant and ethically sourced.',
                    'price': Decimal('229.99'),
                    'stock_quantity': 28,
                    'is_featured': True,
                    'weight': Decimal('0.8'),
                    'dimensions': '14 x 12 x 4 inches'
                },
                {
                    'name': 'Ray-Ban Aviator Sunglasses',
                    'description': 'Classic aviator sunglasses with UV protection and iconic teardrop shape. A timeless accessory.',
                    'price': Decimal('154.99'),
                    'stock_quantity': 40,
                    'weight': Decimal('0.1'),
                    'dimensions': '6 x 2 x 6 inches'
                }
            ],
            'Home & Garden': [
                {
                    'name': 'Dyson V15 Detect Vacuum',
                    'description': 'Advanced cordless vacuum with laser dust detection and powerful suction. Perfect for deep cleaning.',
                    'price': Decimal('749.99'),
                    'stock_quantity': 15,
                    'is_featured': True,
                    'weight': Decimal('6.8'),
                    'dimensions': '49.6 x 9.8 x 10.5 inches'
                },
                {
                    'name': 'KitchenAid Stand Mixer',
                    'description': 'Professional-grade stand mixer with multiple attachments. Perfect for baking and cooking enthusiasts.',
                    'price': Decimal('379.99'),
                    'compare_price': Decimal('429.99'),
                    'stock_quantity': 20,
                    'weight': Decimal('22.0'),
                    'dimensions': '14.1 x 8.7 x 14 inches'
                },
                {
                    'name': 'Ninja Foodi Air Fryer',
                    'description': '8-in-1 countertop appliance with air frying, roasting, and dehydrating capabilities.',
                    'price': Decimal('199.99'),
                    'stock_quantity': 32,
                    'weight': Decimal('18.5'),
                    'dimensions': '15.75 x 13.5 x 12.25 inches'
                },
                {
                    'name': 'Philips Hue Smart Bulbs (4-Pack)',
                    'description': 'Color-changing smart LED bulbs that sync with your home automation system.',
                    'price': Decimal('179.99'),
                    'stock_quantity': 50,
                    'weight': Decimal('0.8'),
                    'dimensions': '8 x 6 x 4 inches'
                }
            ],
            'Sports & Fitness': [
                {
                    'name': 'Peloton Bike+',
                    'description': 'Premium indoor cycling bike with rotating HD touchscreen and access to thousands of classes.',
                    'price': Decimal('2495.00'),
                    'stock_quantity': 8,
                    'is_featured': True,
                    'weight': Decimal('135.0'),
                    'dimensions': '59 x 23 x 53 inches'
                },
                {
                    'name': 'Apple Watch Series 9',
                    'description': 'Advanced health and fitness tracking with ECG, blood oxygen monitoring, and GPS.',
                    'price': Decimal('399.99'),
                    'stock_quantity': 30,
                    'is_featured': True,
                    'weight': Decimal('0.1'),
                    'dimensions': '1.7 x 1.5 x 0.4 inches'
                },
                {
                    'name': 'Bowflex Adjustable Dumbbells',
                    'description': 'Space-saving adjustable dumbbells that replace 15 sets of weights. Perfect for home workouts.',
                    'price': Decimal('549.99'),
                    'stock_quantity': 12,
                    'weight': Decimal('52.5'),
                    'dimensions': '16.9 x 8.3 x 9 inches'
                },
                {
                    'name': 'Yeti Rambler Water Bottle',
                    'description': 'Insulated stainless steel water bottle that keeps drinks cold for 24 hours or hot for 12 hours.',
                    'price': Decimal('44.99'),
                    'stock_quantity': 85,
                    'weight': Decimal('1.1'),
                    'dimensions': '11.1 x 3.5 x 3.5 inches'
                }
            ],
            'Books & Media': [
                {
                    'name': 'Atomic Habits by James Clear',
                    'description': 'A proven framework for improving every day. Learn how to build good habits and break bad ones.',
                    'price': Decimal('18.99'),
                    'stock_quantity': 75,
                    'is_featured': True,
                    'weight': Decimal('0.8'),
                    'dimensions': '8.4 x 5.5 x 1.2 inches'
                },
                {
                    'name': 'The Psychology of Money',
                    'description': 'Timeless lessons on wealth, greed, and happiness by Morgan Housel.',
                    'price': Decimal('16.99'),
                    'stock_quantity': 60,
                    'weight': Decimal('0.7'),
                    'dimensions': '8.3 x 5.5 x 0.9 inches'
                },
                {
                    'name': 'Kindle Paperwhite (11th Gen)',
                    'description': '6.8" display, adjustable warm light, waterproof design, and weeks of battery life.',
                    'price': Decimal('139.99'),
                    'stock_quantity': 25,
                    'weight': Decimal('0.5'),
                    'dimensions': '6.9 x 4.9 x 0.32 inches'
                }
            ],
            'Health & Beauty': [
                {
                    'name': 'Olaplex Hair Treatment Set',
                    'description': 'Professional-grade hair repair treatment that strengthens and restores damaged hair.',
                    'price': Decimal('89.99'),
                    'stock_quantity': 40,
                    'is_featured': True,
                    'weight': Decimal('1.2'),
                    'dimensions': '8 x 6 x 3 inches'
                },
                {
                    'name': 'Vitamin D3 Supplements (120 Count)',
                    'description': 'High-potency vitamin D3 for immune system support and bone health.',
                    'price': Decimal('24.99'),
                    'stock_quantity': 120,
                    'weight': Decimal('0.3'),
                    'dimensions': '4 x 2 x 2 inches'
                },
                {
                    'name': 'Cetaphil Gentle Skin Cleanser',
                    'description': 'Dermatologist-recommended gentle cleanser for sensitive skin. Fragrance-free and non-comedogenic.',
                    'price': Decimal('13.99'),
                    'stock_quantity': 95,
                    'weight': Decimal('1.1'),
                    'dimensions': '7.5 x 3 x 3 inches'
                }
            ],
            'Toys & Games': [
                {
                    'name': 'LEGO Creator Expert Set',
                    'description': 'Advanced building set for adult LEGO enthusiasts. Features intricate details and premium pieces.',
                    'price': Decimal('279.99'),
                    'stock_quantity': 18,
                    'is_featured': True,
                    'weight': Decimal('4.2'),
                    'dimensions': '15.04 x 20.47 x 3.58 inches'
                },
                {
                    'name': 'Nintendo Switch OLED',
                    'description': 'Gaming console with vibrant OLED screen, enhanced audio, and versatile play modes.',
                    'price': Decimal('349.99'),
                    'stock_quantity': 22,
                    'is_featured': True,
                    'weight': Decimal('0.93'),
                    'dimensions': '9.53 x 4.02 x 0.55 inches'
                },
                {
                    'name': 'Monopoly Classic Board Game',
                    'description': 'The classic property trading game that brings families together for hours of fun.',
                    'price': Decimal('19.99'),
                    'stock_quantity': 55,
                    'weight': Decimal('2.4'),
                    'dimensions': '15.75 x 10.5 x 2 inches'
                }
            ],
            'Automotive': [
                {
                    'name': 'Tesla Model 3 Floor Mats',
                    'description': 'Custom-fit all-weather floor mats designed specifically for Tesla Model 3. Durable and easy to clean.',
                    'price': Decimal('149.99'),
                    'stock_quantity': 35,
                    'weight': Decimal('8.5'),
                    'dimensions': '24 x 18 x 2 inches'
                },
                {
                    'name': 'Garmin DashCam 67W',
                    'description': 'Wide-angle dash camera with GPS, voice control, and automatic incident detection.',
                    'price': Decimal('199.99'),
                    'stock_quantity': 28,
                    'weight': Decimal('0.5'),
                    'dimensions': '4.1 x 2.3 x 1.6 inches'
                }
            ]
        }

        # Create products
        products = []
        for category in categories:
            if category.name in products_data:
                for prod_data in products_data[category.name]:
                    product, created = Product.objects.get_or_create(
                        name=prod_data['name'],
                        category=category,
                        defaults={
                            'description': prod_data['description'],
                            'price': prod_data['price'],
                            'compare_price': prod_data.get('compare_price'),
                            'stock_quantity': prod_data['stock_quantity'],
                            'is_featured': prod_data.get('is_featured', False),
                            'weight': prod_data.get('weight'),
                            'dimensions': prod_data.get('dimensions'),
                            'is_active': True
                        }
                    )
                    products.append(product)
                    if created:
                        self.stdout.write(f'Created product: {product.name}')

        # Create sample user if not exists
        sample_user, created = User.objects.get_or_create(
            username='sampleuser',
            defaults={
                'email': 'sample@example.com',
                'first_name': 'Sample',
                'last_name': 'User'
            }
        )
        if created:
            sample_user.set_password('password123')
            sample_user.save()
            self.stdout.write('Created sample user: sampleuser')

        # Create sample reviews
        review_texts = [
            {
                'title': 'Excellent Product!',
                'comment': 'This product exceeded my expectations. Great quality and fast shipping!',
                'rating': 5
            },
            {
                'title': 'Very Good',
                'comment': 'Good value for money. Would recommend to others.',
                'rating': 4
            },
            {
                'title': 'Amazing Quality',
                'comment': 'Outstanding build quality and performance. Worth every penny!',
                'rating': 5
            },
            {
                'title': 'Good Purchase',
                'comment': 'Solid product, works as expected. Happy with my purchase.',
                'rating': 4
            },
            {
                'title': 'Highly Recommended',
                'comment': 'This is exactly what I was looking for. Perfect for my needs!',
                'rating': 5
            }
        ]

        # Add reviews to featured products
        featured_products = [p for p in products if p.is_featured]
        for product in featured_products[:10]:  # Add reviews to first 10 featured products
            for i, review_data in enumerate(review_texts[:3]):  # Add 3 reviews per product
                review, created = ProductReview.objects.get_or_create(
                    product=product,
                    user=sample_user,
                    defaults={
                        'title': review_data['title'],
                        'comment': review_data['comment'],
                        'rating': review_data['rating'],
                        'is_verified_purchase': True
                    }
                )
                if created:
                    self.stdout.write(f'Created review for: {product.name}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with:\n'
                f'- {len(categories)} categories\n'
                f'- {len(products)} products\n'
                f'- Sample user and reviews\n'
                f'Your ecommerce site is now ready with sample data!'
            )
        )
