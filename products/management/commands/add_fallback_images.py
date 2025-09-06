from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from products.models import Product, ProductImage
import requests
from PIL import Image
import io

class Command(BaseCommand):
    help = 'Add fallback images for products that failed to get images'

    def handle(self, *args, **options):
        # Fallback images for products that failed
        fallback_images = {
            'Dyson V15 Detect Vacuum': [
                'https://images.unsplash.com/photo-1558618047-3c8c76ca7d13?w=800&h=800&fit=crop',
                'https://images.unsplash.com/photo-1574781330855-d0db8cc6a79c?w=800&h=800&fit=crop',
                'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=800&h=800&fit=crop'
            ],
            'Patagonia Down Jacket': [
                'https://images.unsplash.com/photo-1539533018447-63fcce2678e3?w=800&h=800&fit=crop',
                'https://images.unsplash.com/photo-1544966503-7cc5ac882d5c?w=800&h=800&fit=crop',
                'https://images.unsplash.com/photo-1445205170444-d2991bc821d2?w=800&h=800&fit=crop'
            ]
        }

        self.stdout.write(self.style.SUCCESS('Adding fallback images for failed products...'))
        
        for product_name, image_urls in fallback_images.items():
            try:
                # Find the product
                products = Product.objects.filter(name__icontains=product_name)
                if not products.exists():
                    self.stdout.write(self.style.WARNING(f'Product not found: {product_name}'))
                    continue
                
                product = products.first()
                
                # Check if product already has images
                if product.images.exists():
                    self.stdout.write(f'Product "{product.name}" already has images, skipping...')
                    continue
                
                self.stdout.write(f'Adding fallback images for: {product.name}')
                
                # Add images for this product
                for i, url in enumerate(image_urls):
                    try:
                        # Download the image
                        response = requests.get(url, timeout=15, headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
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
                            is_primary=(i == 0),
                            order=i,
                            alt_text=f"{product.name} - Image {i+1}"
                        )
                        
                        # Save the image file
                        filename = f"{product.slug}_fallback_{i+1}.jpg"
                        product_image.image.save(filename, ContentFile(buffer.getvalue()))
                        
                        self.stdout.write(f'  ✓ Added fallback image {i+1}')
                        
                    except Exception as e:
                        self.stdout.write(f'  ✗ Failed to add fallback image {i+1}: {str(e)}')
                        # If all else fails, create a simple colored placeholder
                        if i == 0:  # At least create one image
                            self.create_placeholder_image(product)
                        continue
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error processing {product_name}: {str(e)}'))
                continue
        
        self.stdout.write(self.style.SUCCESS('✓ Finished adding fallback images!'))
    
    def create_placeholder_image(self, product):
        """Create a simple colored placeholder image"""
        try:
            from PIL import ImageDraw, ImageFont
            
            # Create a simple colored image
            colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
            color = colors[hash(product.name) % len(colors)]
            
            img = Image.new('RGB', (800, 800), color)
            draw = ImageDraw.Draw(img)
            
            # Add product name as text
            try:
                font = ImageFont.truetype("arial.ttf", 48)
            except:
                font = ImageFont.load_default()
            
            text = product.name
            if len(text) > 20:
                text = text[:20] + "..."
            
            bbox = draw.textbbox((0, 0), text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (800 - text_width) // 2
            y = (800 - text_height) // 2
            draw.text((x, y), text, fill='white', font=font)
            
            # Save to buffer
            buffer = io.BytesIO()
            img.save(buffer, format='JPEG', quality=90)
            buffer.seek(0)
            
            # Create ProductImage instance
            product_image = ProductImage(
                product=product,
                is_primary=True,
                order=0,
                alt_text=f"{product.name} - Placeholder"
            )
            
            filename = f"{product.slug}_placeholder.jpg"
            product_image.image.save(filename, ContentFile(buffer.getvalue()))
            
            self.stdout.write(f'  ✓ Created placeholder image for {product.name}')
            
        except Exception as e:
            self.stdout.write(f'  ✗ Failed to create placeholder: {str(e)}')
