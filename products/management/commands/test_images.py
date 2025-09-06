from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, ProductImage, Category
from PIL import Image
import io
import requests
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Test product image functionality and populate sample data'

    def add_arguments(self, parser):
        parser.add_argument('--create-sample', action='store_true', help='Create sample products with images')
        parser.add_argument('--test-existing', action='store_true', help='Test existing products')

    def handle(self, *args, **options):
        if options['create_sample']:
            self.create_sample_products()
        elif options['test_existing']:
            self.test_existing_products()
        else:
            self.stdout.write(self.style.SUCCESS('Use --create-sample or --test-existing'))

    def create_sample_products(self):
        """Create sample products with placeholder images"""
        try:
            # Create a sample category if it doesn't exist
            category, created = Category.objects.get_or_create(
                name="Electronics",
                defaults={
                    'description': 'Electronic devices and gadgets',
                    'slug': 'electronics'
                }
            )
            
            if created:
                self.stdout.write(f'Created category: {category.name}')

            # Create sample products
            sample_products = [
                {
                    'name': 'Sample Smartphone',
                    'description': 'A high-quality smartphone with amazing features',
                    'price': 599.99,
                    'stock_quantity': 10,
                    'is_featured': True
                },
                {
                    'name': 'Sample Laptop',
                    'description': 'Powerful laptop for work and gaming',
                    'price': 1299.99,
                    'stock_quantity': 5,
                    'is_featured': True
                }
            ]

            for product_data in sample_products:
                product, created = Product.objects.get_or_create(
                    name=product_data['name'],
                    defaults={
                        **product_data,
                        'category': category
                    }
                )
                
                if created:
                    self.stdout.write(f'Created product: {product.name}')
                    
                    # Create sample images for this product
                    self.create_sample_images_for_product(product)

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating sample data: {e}'))

    def create_sample_images_for_product(self, product):
        """Create placeholder images for a product"""
        try:
            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
            
            for i, color in enumerate(colors[:3]):  # Create 3 images per product
                # Create a simple colored placeholder image
                img = Image.new('RGB', (800, 800), color)
                
                # Add some text to make it identifiable
                try:
                    from PIL import ImageDraw, ImageFont
                    draw = ImageDraw.Draw(img)
                    # Try to use a default font, fallback to basic if not available
                    try:
                        font = ImageFont.truetype("arial.ttf", 60)
                    except:
                        font = ImageFont.load_default()
                    
                    text = f"{product.name}\nImage {i+1}"
                    bbox = draw.textbbox((0, 0), text, font=font)
                    text_width = bbox[2] - bbox[0]
                    text_height = bbox[3] - bbox[1]
                    x = (800 - text_width) // 2
                    y = (800 - text_height) // 2
                    draw.text((x, y), text, fill='white', font=font, align='center')
                except:
                    # If text rendering fails, just use colored rectangle
                    pass
                
                # Save to BytesIO
                buffer = io.BytesIO()
                img.save(buffer, format='JPEG', quality=90)
                buffer.seek(0)
                
                # Create ProductImage instance
                product_image = ProductImage(
                    product=product,
                    is_primary=(i == 0),  # First image is primary
                    order=i,
                    alt_text=f"{product.name} - Image {i+1}"
                )
                
                # Save the image file
                filename = f"{product.slug}_{i+1}.jpg"
                product_image.image.save(filename, ContentFile(buffer.getvalue()))
                
                self.stdout.write(f'  Created image {i+1} for {product.name}')
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating images for {product.name}: {e}'))

    def test_existing_products(self):
        """Test existing products and their images"""
        products = Product.objects.all()
        
        if not products.exists():
            self.stdout.write(self.style.WARNING('No products found. Use --create-sample to create some.'))
            return
        
        for product in products:
            self.stdout.write(f'\nProduct: {product.name}')
            self.stdout.write(f'  Slug: {product.slug}')
            
            # Test primary image
            primary_image = product.get_primary_image()
            if primary_image:
                self.stdout.write(f'  Primary image: {primary_image.url}')
            else:
                self.stdout.write('  No primary image found')
            
            # Test all images
            all_images = product.get_all_images()
            self.stdout.write(f'  Total images: {len(all_images)}')
            
            # List ProductImage instances
            product_images = product.images.all()
            for img in product_images:
                self.stdout.write(f'    - {img.image.url} (Primary: {img.is_primary}, Order: {img.order})')
