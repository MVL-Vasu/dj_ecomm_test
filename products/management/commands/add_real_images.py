from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, ProductImage
import requests
from PIL import Image
import io

class Command(BaseCommand):
    help = 'Add real product images from internet URLs for existing products'

    def handle(self, *args, **options):
        # Product image mappings with real product images from the internet
        product_images = {
            'iPhone 15 Pro Max': [
                'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Samsung Galaxy S24 Ultra': [
                'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=800&fit=crop&crop=bottom'
            ],
            'MacBook Air M3': [
                'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Sony WH-1000XM5 Headphones': [
                'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&h=800&fit=crop&crop=bottom'
            ],
            'iPad Pro 12.9"': [
                'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Nike Air Jordan 1 Retro': [
                'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Levi\'s 501 Original Jeans': [
                'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1542272604-787c3835535d?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Patagonia Down Jacket': [
                'https://images.unsplash.com/photo-1544966503-7cc5ac882d5c?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1544966503-7cc5ac882d5c?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1544966503-7cc5ac882d5c?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Ray-Ban Aviator Sunglasses': [
                'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Dyson V15 Detect Vacuum': [
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=800&fit=crop&crop=bottom'
            ],
            'KitchenAid Stand Mixer': [
                'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Ninja Foodi Air Fryer': [
                'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Philips Hue Smart Bulbs (4-Pack)': [
                'https://images.unsplash.com/photo-1558002038-1055907df827?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1558002038-1055907df827?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1558002038-1055907df827?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Peloton Bike+': [
                'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Apple Watch Series 9': [
                'https://images.unsplash.com/photo-1510017098667-27dfc7150acb?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1510017098667-27dfc7150acb?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1510017098667-27dfc7150acb?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Bowflex Adjustable Dumbbells': [
                'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1517963879433-6ad2b056d712?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Yeti Rambler Water Bottle': [
                'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1523362628745-0c100150b504?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Atomic Habits by James Clear': [
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&crop=bottom'
            ],
            'The Psychology of Money': [
                'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Kindle Paperwhite (11th Gen)': [
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Olaplex Hair Treatment Set': [
                'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1571781926291-c477ebfd024b?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Vitamin D3 Supplements (120 Count)': [
                'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Cetaphil Gentle Skin Cleanser': [
                'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&h=800&fit=crop&crop=bottom'
            ],
            'LEGO Creator Expert Set': [
                'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1558060370-d644479cb6f7?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Nintendo Switch OLED': [
                'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Monopoly Classic Board Game': [
                'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1606092195730-5d7b9af1efc5?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Tesla Model 3 Floor Mats': [
                'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1549317661-bd32c8ce0db2?w=800&h=800&fit=crop&crop=bottom'
            ],
            'Garmin DashCam 67W': [
                'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&h=800&fit=crop&crop=center',
                'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&h=800&fit=crop&crop=top',
                'https://images.unsplash.com/photo-1449965408869-eaa3f722e40d?w=800&h=800&fit=crop&crop=bottom'
            ]
        }

        self.stdout.write(self.style.SUCCESS('Starting to add real product images...'))
        
        for product_name, image_urls in product_images.items():
            try:
                # Find the product by name (case insensitive contains search)
                products = Product.objects.filter(name__icontains=product_name.replace("'", ""))
                if not products.exists():
                    # Try exact match
                    products = Product.objects.filter(name=product_name)
                    if not products.exists():
                        self.stdout.write(self.style.WARNING(f'Product not found: {product_name}'))
                        continue
                
                product = products.first()
                
                # Check if product already has images
                if product.images.exists():
                    self.stdout.write(f'Product "{product.name}" already has images, skipping...')
                    continue
                
                self.stdout.write(f'Adding images for: {product.name}')
                
                # Add images for this product
                for i, url in enumerate(image_urls):
                    try:
                        # Download the image
                        response = requests.get(url, timeout=15, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                        })
                        response.raise_for_status()
                        
                        # Open and process the image
                        img = Image.open(io.BytesIO(response.content))
                        
                        # Convert to RGB if necessary
                        if img.mode not in ('RGB', 'L'):
                            img = img.convert('RGB')
                        
                        # Resize to reasonable dimensions
                        img.thumbnail((800, 800), Image.Resampling.LANCZOS)
                        
                        # Save to buffer
                        buffer = io.BytesIO()
                        img.save(buffer, format='JPEG', quality=85)
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
                        
                        self.stdout.write(f'  ✓ Added image {i+1}')
                        
                    except Exception as e:
                        self.stdout.write(f'  ✗ Failed to add image {i+1}: {str(e)}')
                        continue
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {product_name}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS('✓ Finished adding product images!'))
        
        # Show summary
        self.show_summary()
    
    def show_summary(self):
        """Show summary of products with and without images"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SUMMARY:')
        self.stdout.write('='*50)
        
        total_products = Product.objects.count()
        products_with_images = Product.objects.filter(images__isnull=False).distinct().count()
        products_without_images = total_products - products_with_images
        
        self.stdout.write(f'Total products: {total_products}')
        self.stdout.write(f'Products with images: {products_with_images}')
        self.stdout.write(f'Products without images: {products_without_images}')
        
        if products_without_images > 0:
            self.stdout.write('\nProducts without images:')
            for product in Product.objects.filter(images__isnull=True):
                self.stdout.write(f'  - {product.name}')
