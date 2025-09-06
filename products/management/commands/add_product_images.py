from django.core.management.base import BaseCommand
from products.models import Product
import requests
import tempfile
import os
from django.core.files import File

class Command(BaseCommand):
    help = 'Add placeholder images to products'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Adding images to products...'))

        # Image mappings for different products
        image_mappings = {
            # Electronics
            'iPhone 15 Pro Max': 'https://picsum.photos/600/600?random=1',
            'Samsung Galaxy S24 Ultra': 'https://picsum.photos/600/600?random=2', 
            'MacBook Air M3': 'https://picsum.photos/600/600?random=3',
            'Sony WH-1000XM5 Headphones': 'https://picsum.photos/600/600?random=4',
            'iPad Pro 12.9"': 'https://picsum.photos/600/600?random=5',
            
            # Fashion & Clothing
            'Nike Air Jordan 1 Retro': 'https://picsum.photos/600/600?random=6',
            "Levi's 501 Original Jeans": 'https://picsum.photos/600/600?random=7',
            'Patagonia Down Jacket': 'https://picsum.photos/600/600?random=8',
            'Ray-Ban Aviator Sunglasses': 'https://picsum.photos/600/600?random=9',
            
            # Home & Garden
            'Dyson V15 Detect Vacuum': 'https://picsum.photos/600/600?random=10',
            'KitchenAid Stand Mixer': 'https://picsum.photos/600/600?random=11',
            'Ninja Foodi Air Fryer': 'https://picsum.photos/600/600?random=12',
            'Philips Hue Smart Bulbs (4-Pack)': 'https://picsum.photos/600/600?random=13',
            
            # Sports & Fitness
            'Peloton Bike+': 'https://picsum.photos/600/600?random=14',
            'Apple Watch Series 9': 'https://picsum.photos/600/600?random=15',
            'Bowflex Adjustable Dumbbells': 'https://picsum.photos/600/600?random=16',
            'Yeti Rambler Water Bottle': 'https://picsum.photos/600/600?random=17',
            
            # Books & Media
            'Atomic Habits by James Clear': 'https://picsum.photos/600/600?random=18',
            'The Psychology of Money': 'https://picsum.photos/600/600?random=19',
            'Kindle Paperwhite (11th Gen)': 'https://picsum.photos/600/600?random=20',
            
            # Health & Beauty
            'Olaplex Hair Treatment Set': 'https://picsum.photos/600/600?random=21',
            'Vitamin D3 Supplements (120 Count)': 'https://picsum.photos/600/600?random=22',
            'Cetaphil Gentle Skin Cleanser': 'https://picsum.photos/600/600?random=23',
            
            # Toys & Games
            'LEGO Creator Expert Set': 'https://picsum.photos/600/600?random=24',
            'Nintendo Switch OLED': 'https://picsum.photos/600/600?random=25',
            'Monopoly Classic Board Game': 'https://picsum.photos/600/600?random=26',
            
            # Automotive
            'Tesla Model 3 Floor Mats': 'https://picsum.photos/600/600?random=27',
            'Garmin DashCam 67W': 'https://picsum.photos/600/600?random=28',
        }

        def download_image(url, product_name):
            """Download image from URL and return a Django File object"""
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    # Create a temporary file
                    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                    temp_file.write(response.content)
                    temp_file.flush()
                    
                    # Create Django File object
                    with open(temp_file.name, 'rb') as f:
                        django_file = File(f)
                        django_file.name = f"{product_name.lower().replace(' ', '-')}.jpg"
                        return django_file, temp_file.name
                    
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error downloading image for {product_name}: {e}'))
                return None, None

        # Update products with images
        products = Product.objects.all()
        for product in products:
            if not product.image and product.name in image_mappings:
                url = image_mappings[product.name]
                
                try:
                    response = requests.get(url, timeout=10)
                    if response.status_code == 200:
                        # Create a temporary file
                        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
                        temp_file.write(response.content)
                        temp_file.close()
                        
                        # Save image to product
                        filename = f"{product.name.lower().replace(' ', '-').replace('/', '-')}.jpg"
                        with open(temp_file.name, 'rb') as f:
                            product.image.save(filename, File(f), save=True)
                        
                        # Clean up temp file
                        os.unlink(temp_file.name)
                        
                        self.stdout.write(f'Added image to: {product.name}')
                    
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error adding image to {product.name}: {e}'))

        self.stdout.write(self.style.SUCCESS('Finished adding images to products!'))
