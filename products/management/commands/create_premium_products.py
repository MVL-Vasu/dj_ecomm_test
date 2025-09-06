from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, Category, ProductImage, ProductReview
from decimal import Decimal
import cloudinary.uploader
import requests
from io import BytesIO


class Command(BaseCommand):
    help = 'Create premium products with high-quality Cloudinary images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--replace',
            action='store_true',
            help='Replace existing products with premium ones',
        )

    def upload_image_to_cloudinary(self, image_url, public_id):
        """Upload an image from URL to Cloudinary"""
        try:
            # Upload image to Cloudinary
            result = cloudinary.uploader.upload(
                image_url,
                public_id=public_id,
                folder="ecommerce/products",
                transformation=[
                    {"width": 800, "height": 800, "crop": "fill"},
                    {"quality": "auto:good"}
                ]
            )
            return result['secure_url']
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(f'Failed to upload image {public_id}: {str(e)}')
            )
            # Return a placeholder image
            return 'https://via.placeholder.com/800x800/cccccc/ffffff?text=Product+Image'

    def handle(self, *args, **options):
        self.stdout.write('Creating premium products with Cloudinary images...')
        
        if options['replace']:
            with transaction.atomic():
                # Clear existing data
                ProductReview.objects.all().delete()
                ProductImage.objects.all().delete()
                Product.objects.all().delete()
                Category.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('✓ Cleared existing data'))

        with transaction.atomic():
            # Create categories with better descriptions
            categories_data = [
                {
                    'name': 'Electronics',
                    'description': 'Cut the latest electronic gadgets and smart devices',
                    'image_url': 'https://images.unsplash.com/photo-1498049794561-7780e7231661?w=400'
                },
                {
                    'name': 'Smartphones',
                    'description': 'Premium smartphones and mobile accessories',
                    'image_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400'
                },
                {
                    'name': 'Laptops',
                    'description': 'High-performance laptops for work, gaming, and creativity',
                    'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400'
                },
                {
                    'name': 'Fashion',
                    'description': 'Trendy clothing, shoes, and fashion accessories',
                    'image_url': 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?w=400'
                },
                {
                    'name': 'Home & Kitchen',
                    'description': 'Essential home appliances and kitchen gadgets',
                    'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400'
                },
                {
                    'name': 'Books',
                    'description': 'Wide collection of books across all genres',
                    'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400'
                }
            ]
            
            categories = {}
            self.stdout.write('Creating categories...')
            for cat_data in categories_data:
                # Upload category image to Cloudinary
                cloudinary_url = self.upload_image_to_cloudinary(
                    cat_data['image_url'],
                    f"category_{cat_data['name'].lower().replace(' ', '_').replace('&', 'and')}"
                )
                
                category = Category.objects.create(
                    name=cat_data['name'],
                    description=cat_data['description'],
                    image=cloudinary_url
                )
                categories[cat_data['name']] = category
                self.stdout.write(f'✓ Created category: {cat_data["name"]}')
            
            # Create products with real product images
            products_data = [
                {
                    'name': 'iPhone 15 Pro',
                    'category': 'Smartphones',
                    'description': 'Latest iPhone with titanium design, advanced camera system, and A17 Pro chip. Features include ProRAW photography, Action Button, and USB-C connectivity.',
                    'price': Decimal('1199.99'),
                    'compare_price': Decimal('1299.99'),
                    'stock_quantity': 50,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800',
                    'weight': Decimal('2.78'),
                    'dimensions': '6.1 x 2.8 x 0.32 inches'
                },
                {
                    'name': 'Samsung Galaxy S24 Ultra',
                    'category': 'Smartphones',
                    'description': 'Premium Android flagship with S Pen, 200MP camera, and advanced AI features. Includes 5G connectivity and all-day battery life.',
                    'price': Decimal('1299.99'),
                    'compare_price': Decimal('1399.99'),
                    'stock_quantity': 75,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1610945265064-0e34e5519bbf?w=800',
                    'weight': Decimal('2.32'),
                    'dimensions': '6.4 x 3.1 x 0.35 inches'
                },
                {
                    'name': 'MacBook Pro 14" M3',
                    'category': 'Laptops',
                    'description': 'Powerful laptop with M3 chip featuring 8-core CPU and 10-core GPU. Perfect for professional video editing, coding, and creative work.',
                    'price': Decimal('1999.99'),
                    'compare_price': Decimal('2199.99'),
                    'stock_quantity': 25,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1517336714731-489689fd1ca4?w=800',
                    'weight': Decimal('3.5'),
                    'dimensions': '12.31 x 8.71 x 0.61 inches'
                },
                {
                    'name': 'Dell XPS 13 Plus',
                    'category': 'Laptops',
                    'description': 'Ultra-portable laptop with stunning 13.4" OLED display, 12th Gen Intel Core processor, and premium build quality.',
                    'price': Decimal('1299.99'),
                    'compare_price': Decimal('1499.99'),
                    'stock_quantity': 40,
                    'is_featured': False,
                    'image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=800',
                    'weight': Decimal('2.73'),
                    'dimensions': '11.63 x 7.84 x 0.55 inches'
                },
                {
                    'name': 'Sony WH-1000XM5 Headphones',
                    'category': 'Electronics',
                    'description': 'Industry-leading noise canceling wireless headphones with 30-hour battery life, crystal clear hands-free calling, and adaptive sound control.',
                    'price': Decimal('399.99'),
                    'compare_price': Decimal('449.99'),
                    'stock_quantity': 60,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=800',
                    'weight': Decimal('0.55'),
                    'dimensions': '7.3 x 3.03 x 10.73 inches'
                },
                {
                    'name': 'Apple Watch Series 9',
                    'category': 'Electronics',
                    'description': 'Advanced smartwatch with S9 chip, Double Tap gesture, health monitoring, and seamless iPhone integration.',
                    'price': Decimal('399.99'),
                    'compare_price': Decimal('449.99'),
                    'stock_quantity': 80,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1551816230-ef5deaed4a26?w=800',
                    'weight': Decimal('0.07'),
                    'dimensions': '1.69 x 1.42 x 0.41 inches'
                },
                {
                    'name': 'Nike Air Jordan 1 Retro',
                    'category': 'Fashion',
                    'description': 'Iconic basketball shoes that revolutionized sneaker culture. Premium leather construction with classic colorway and legendary comfort.',
                    'price': Decimal('170.00'),
                    'compare_price': Decimal('200.00'),
                    'stock_quantity': 120,
                    'is_featured': False,
                    'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800',
                    'weight': Decimal('1.5'),
                    'dimensions': 'Various sizes available'
                },
                {
                    'name': 'Levi\'s 501 Original Fit Jeans',
                    'category': 'Fashion',
                    'description': 'The original blue jean since 1873. Classic straight fit made from 100% cotton denim with button fly and signature arcuate stitching.',
                    'price': Decimal('89.50'),
                    'compare_price': Decimal('98.00'),
                    'stock_quantity': 200,
                    'is_featured': False,
                    'image_url': 'https://images.unsplash.com/photo-1541099649105-f69ad21f3246?w=800',
                    'weight': Decimal('1.2'),
                    'dimensions': 'Various sizes available'
                },
                {
                    'name': 'Instant Pot Duo 7-in-1',
                    'category': 'Home & Kitchen',
                    'description': 'Multi-use programmable pressure cooker that replaces 7 kitchen appliances. Cook faster, healthier, and more convenient meals.',
                    'price': Decimal('99.99'),
                    'compare_price': Decimal('129.99'),
                    'stock_quantity': 85,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800',
                    'weight': Decimal('12.9'),
                    'dimensions': '13.43 x 12.4 x 12.99 inches'
                },
                {
                    'name': 'KitchenAid Artisan Stand Mixer',
                    'category': 'Home & Kitchen',
                    'description': 'Professional-grade 5-quart tilt-head stand mixer with 10 speeds and multiple attachment options for all your baking needs.',
                    'price': Decimal('379.99'),
                    'compare_price': Decimal('429.99'),
                    'stock_quantity': 30,
                    'is_featured': False,
                    'image_url': 'https://images.unsplash.com/photo-1586217831500-a5c5c9e4c01a?w=800',
                    'weight': Decimal('22'),
                    'dimensions': '14.13 x 8.75 x 14 inches'
                },
                {
                    'name': 'Atomic Habits by James Clear',
                    'category': 'Books',
                    'description': '#1 New York Times bestseller. Transform your life with tiny changes in behavior that compound into remarkable results.',
                    'price': Decimal('18.99'),
                    'compare_price': Decimal('26.99'),
                    'stock_quantity': 180,
                    'is_featured': True,
                    'image_url': 'https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=800',
                    'weight': Decimal('0.7'),
                    'dimensions': '6.12 x 1.06 x 9.25 inches'
                },
                {
                    'name': 'The Psychology of Money',
                    'category': 'Books',
                    'description': 'Timeless lessons on wealth, greed, and happiness from one of the foremost financial thinkers of our time.',
                    'price': Decimal('16.99'),
                    'compare_price': Decimal('24.99'),
                    'stock_quantity': 150,
                    'is_featured': False,
                    'image_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800',
                    'weight': Decimal('0.65'),
                    'dimensions': '6.12 x 0.94 x 9.25 inches'
                }
            ]
            
            self.stdout.write('Creating premium products...')
            created_products = []
            
            for i, product_data in enumerate(products_data, 1):
                self.stdout.write(f'Creating product {i}/{len(products_data)}: {product_data["name"]}')
                
                # Upload product image to Cloudinary
                cloudinary_url = self.upload_image_to_cloudinary(
                    product_data['image_url'],
                    f"product_{product_data['name'].lower().replace(' ', '_').replace('\"', '').replace('\'', '')}"
                )
                
                product = Product.objects.create(
                    name=product_data['name'],
                    category=categories[product_data['category']],
                    description=product_data['description'],
                    price=product_data['price'],
                    compare_price=product_data['compare_price'],
                    stock_quantity=product_data['stock_quantity'],
                    is_featured=product_data['is_featured'],
                    weight=product_data.get('weight'),
                    dimensions=product_data.get('dimensions', ''),
                    image=cloudinary_url
                )
                
                # Create primary ProductImage
                ProductImage.objects.create(
                    product=product,
                    image=cloudinary_url,
                    alt_text=f"{product.name} - Premium Quality",
                    is_primary=True,
                    order=1
                )
                
                created_products.append(product)
                self.stdout.write(f'✓ Created: {product.name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\\n🎉 Successfully created {len(categories)} categories and {len(created_products)} premium products!'
                )
            )
            
            # Display summary
            self.stdout.write('\\n📊 Final Summary:')
            self.stdout.write(f'Categories: {Category.objects.count()}')
            self.stdout.write(f'Total Products: {Product.objects.count()}')
            self.stdout.write(f'Featured Products: {Product.objects.filter(is_featured=True).count()}')
            self.stdout.write(f'Product Images: {ProductImage.objects.count()}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\\n✅ All products now have premium Cloudinary images with optimized transformations!'
                )
            )
            
            # Show featured products
            featured_products = Product.objects.filter(is_featured=True)
            if featured_products:
                self.stdout.write('\\n🌟 Featured Products:')
                for product in featured_products:
                    self.stdout.write(f'  • {product.name} - ${product.price}')
