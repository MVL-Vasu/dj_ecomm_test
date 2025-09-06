from PIL import Image, ImageOps
import os
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import io

def optimize_image(image_field, max_width=1200, max_height=1200, quality=85):
    """
    Optimize an uploaded image by resizing and compressing it
    """
    if not image_field:
        return None
    
    try:
        # Open the image
        img = Image.open(image_field)
        
        # Convert to RGB if necessary (handles RGBA, P mode, etc.)
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Auto-orient the image based on EXIF data
        img = ImageOps.exif_transpose(img)
        
        # Calculate new dimensions maintaining aspect ratio
        img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
        
        # Save the optimized image to a BytesIO buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        # Create a new ContentFile with the optimized image
        return ContentFile(buffer.getvalue())
        
    except Exception as e:
        # If optimization fails, return the original image
        print(f"Image optimization failed: {e}")
        return image_field

def create_thumbnail(image_field, size=(300, 300), quality=80):
    """
    Create a thumbnail version of an image
    """
    if not image_field:
        return None
    
    try:
        # Open the image
        img = Image.open(image_field)
        
        # Convert to RGB if necessary
        if img.mode not in ('RGB', 'L'):
            img = img.convert('RGB')
        
        # Auto-orient the image
        img = ImageOps.exif_transpose(img)
        
        # Create thumbnail
        img.thumbnail(size, Image.Resampling.LANCZOS)
        
        # Save to buffer
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG', quality=quality, optimize=True)
        buffer.seek(0)
        
        return ContentFile(buffer.getvalue())
        
    except Exception as e:
        print(f"Thumbnail creation failed: {e}")
        return None

def generate_image_variants(image_field, base_name):
    """
    Generate different variants of an image (thumbnail, medium, large)
    Returns a dictionary with the variants
    """
    variants = {}
    
    if not image_field:
        return variants
    
    try:
        # Thumbnail (300x300)
        thumbnail = create_thumbnail(image_field, (300, 300), 80)
        if thumbnail:
            variants['thumbnail'] = thumbnail
        
        # Medium size (600x600)
        medium = create_thumbnail(image_field, (600, 600), 85)
        if medium:
            variants['medium'] = medium
        
        # Large/optimized version (1200x1200)
        large = optimize_image(image_field, 1200, 1200, 90)
        if large:
            variants['large'] = large
            
    except Exception as e:
        print(f"Image variant generation failed: {e}")
    
    return variants

def get_upload_path(instance, filename):
    """
    Generate upload path for product images
    """
    # Get file extension
    name, ext = os.path.splitext(filename)
    
    # Create path: products/product_id/filename
    return f'products/{instance.product.id}/{instance.product.slug}_{instance.order}{ext}'
