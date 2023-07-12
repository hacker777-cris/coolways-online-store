from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', through='CartItem', related_name='carts')

    def get_total_price(self):
        total_price = 0
        for item in self.cartitem_set.all():
            total_price += item.product.price * item.quantity
        return total_price

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)
    # Add other fields as needed


class Category(models.Model):
    name = models.CharField(max_length=100, default='hello')

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(default='example@example.com')
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()

class Order(models.Model):
    PAYMENT_CHOICES = (
        ('online', 'Online Payment'),
        ('delivery', 'Pay on Delivery'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    products = models.ManyToManyField(Product)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='online')
    delivery_location = models.CharField(max_length=50)

    def __str__(self):
        return f"Order #{self.id} - Total: {self.total_price}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Order #{self.order.id} - {self.product.name} - Quantity: {self.quantity}"