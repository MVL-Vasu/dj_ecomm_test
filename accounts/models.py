from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    # Default addresses
    default_shipping_address_line_1 = models.CharField(max_length=255, blank=True)
    default_shipping_address_line_2 = models.CharField(max_length=255, blank=True)
    default_shipping_city = models.CharField(max_length=100, blank=True)
    default_shipping_state = models.CharField(max_length=100, blank=True)
    default_shipping_postal_code = models.CharField(max_length=20, blank=True)
    default_shipping_country = models.CharField(max_length=100, blank=True)
    
    default_billing_address_line_1 = models.CharField(max_length=255, blank=True)
    default_billing_address_line_2 = models.CharField(max_length=255, blank=True)
    default_billing_city = models.CharField(max_length=100, blank=True)
    default_billing_state = models.CharField(max_length=100, blank=True)
    default_billing_postal_code = models.CharField(max_length=20, blank=True)
    default_billing_country = models.CharField(max_length=100, blank=True)
    
    # Preferences
    newsletter_subscription = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Profile for {self.user.username}"
    
    @property
    def full_name(self):
        return f"{self.user.first_name} {self.user.last_name}".strip()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
