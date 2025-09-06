from django.core.management.base import BaseCommand
from django.db import transaction
from products.models import Product, Category, ProductImage, ProductReview
from decimal import Decimal
import cloudinary.uploader


class Command(BaseCommand):
    help = 'Reset product data and add new products with Cloudinary images'

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm that you want to delete all existing products',
        )

    def handle(self, *args, **options):
        if not options['confirm']:
            self.stdout.write(
                self.style.WARNING(
                    'This will delete ALL existing products, categories, and related data. '
                    'Use --confirm flag if you really want to proceed.'
                )
            )
            return

        self.stdout.write('Starting product data reset...')
        
        with transaction.atomic():
            # Delete all existing data
            self.stdout.write('Deleting existing data...')
            ProductReview.objects.all().delete()
            ProductImage.objects.all().delete()
            Product.objects.all().delete()
            Category.objects.all().delete()
            
            self.stdout.write(self.style.SUCCESS('✓ Deleted all existing data'))
            
            # Create new categories
            self.stdout.write('Creating categories...')
            categories_data = [
                {
                    'name': 'Electronics',
                    'description': 'Latest electronic gadgets and devices',
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Smartphones',
                    'description': 'Premium smartphones and accessories',
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Laptops',
                    'description': 'High-performance laptops for work and gaming',
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Fashion',
                    'description': 'Trendy clothing and fashion accessories',
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Home & Kitchen',
                    'description': 'Essential home and kitchen appliances',
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Books',
                    'description': 'Wide collection of books across genres',
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                }
            ]
            
            categories = {}
            for cat_data in categories_data:
                category = Category.objects.create(
                    name=cat_data['name'],
                    description=cat_data['description'],
                    image=cat_data['image_url']  # Cloudinary URL
                )
                categories[cat_data['name']] = category
                self.stdout.write(f'✓ Created category: {cat_data["name"]}')
            
            # Create new products with Cloudinary images
            self.stdout.write('Creating products...')
            products_data = [
                {
                    'name': 'iPhone 15 Pro',
                    'category': 'Smartphones',
                    'description': 'Latest iPhone with titanium design and advanced camera system.',
                    'price': Decimal('1199.99'),
                    'compare_price': Decimal('1299.99'),
                    'stock_quantity': 50,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Samsung Galaxy S24 Ultra',
                    'category': 'Smartphones',
                    'description': 'Premium Android smartphone with S Pen and advanced AI features.',
                    'price': Decimal('1099.99'),
                    'compare_price': Decimal('1199.99'),
                    'stock_quantity': 75,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'MacBook Pro 14" M3',
                    'category': 'Laptops',
                    'description': 'Powerful laptop with M3 chip for professional work.',
                    'price': Decimal('1999.99'),
                    'compare_price': Decimal('2199.99'),
                    'stock_quantity': 25,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Dell XPS 13',
                    'category': 'Laptops',
                    'description': 'Ultra-portable laptop with stunning display.',
                    'price': Decimal('899.99'),
                    'compare_price': Decimal('999.99'),
                    'stock_quantity': 40,
                    'is_featured': False,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Sony WH-1000XM5',
                    'category': 'Electronics',
                    'description': 'Premium noise-canceling wireless headphones.',
                    'price': Decimal('399.99'),
                    'compare_price': Decimal('449.99'),
                    'stock_quantity': 60,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Apple Watch Series 9',
                    'category': 'Electronics',
                    'description': 'Advanced smartwatch with health monitoring features.',
                    'price': Decimal('329.99'),
                    'compare_price': Decimal('399.99'),
                    'stock_quantity': 80,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Nike Air Max 270',
                    'category': 'Fashion',
                    'description': 'Comfortable and stylish running shoes.',
                    'price': Decimal('129.99'),
                    'compare_price': Decimal('149.99'),
                    'stock_quantity': 120,
                    'is_featured': False,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Levi\'s 501 Jeans',
                    'category': 'Fashion',
                    'description': 'Classic straight-fit jeans in premium denim.',
                    'price': Decimal('79.99'),
                    'compare_price': Decimal('89.99'),
                    'stock_quantity': 200,
                    'is_featured': False,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Instant Pot Duo 7-in-1',
                    'category': 'Home & Kitchen',
                    'description': 'Multi-functional electric pressure cooker.',
                    'price': Decimal('99.99'),
                    'compare_price': Decimal('119.99'),
                    'stock_quantity': 85,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'KitchenAid Stand Mixer',
                    'category': 'Home & Kitchen',
                    'description': 'Professional-grade stand mixer for baking.',
                    'price': Decimal('349.99'),
                    'compare_price': Decimal('399.99'),
                    'stock_quantity': 30,
                    'is_featured': False,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'The Psychology of Money',
                    'category': 'Books',
                    'description': 'Bestselling book about personal finance and investing.',
                    'price': Decimal('16.99'),
                    'compare_price': Decimal('19.99'),
                    'stock_quantity': 150,
                    'is_featured': False,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                },
                {
                    'name': 'Atomic Habits',
                    'category': 'Books',
                    'description': 'Transform your life with tiny changes in behavior.',
                    'price': Decimal('18.99'),
                    'compare_price': Decimal('21.99'),
                    'stock_quantity': 180,
                    'is_featured': True,
                    'image_url': 'https://res.cloudinary.com/demo/image/upload/v1312461204/sample.jpg'
                }
            ]
            
            created_products = []
            for product_data in products_data:
                product = Product.objects.create(
                    name=product_data['name'],
                    category=categories[product_data['category']],
                    description=product_data['description'],
                    price=product_data['price'],
                    compare_price=product_data['compare_price'],
                    stock_quantity=product_data['stock_quantity'],
                    is_featured=product_data['is_featured'],
                    image=product_data['image_url']  # Direct Cloudinary URL
                )
                
                # Create a ProductImage as the primary image
                ProductImage.objects.create(
                    product=product,
                    image=product_data['image_url'],
                    alt_text=f"{product.name} - Main Image",
                    is_primary=True,
                    order=1
                )
                
                created_products.append(product)
                self.stdout.write(f'✓ Created product: {product.name}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n🎉 Successfully created {len(categories)} categories and {len(created_products)} products with Cloudinary images!'
                )
            )
            
            # Display summary
            self.stdout.write('\n📊 Summary:')
            self.stdout.write(f'Categories: {Category.objects.count()}')
            self.stdout.write(f'Products: {Product.objects.count()}')
            self.stdout.write(f'Featured Products: {Product.objects.filter(is_featured=True).count()}')
            self.stdout.write(f'Product Images: {ProductImage.objects.count()}')
            
            self.stdout.write(
                self.style.SUCCESS(
                    '\n✅ All products now use Cloudinary for image storage!'
                )
            )
