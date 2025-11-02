from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Property(models.Model):
    HOUSE = 'HOUSE'
    APARTMENT = 'APARTMENT'
    CONDO = 'CONDO'
    TOWNHOUSE = 'TOWNHOUSE'
    LAND = 'LAND'
    COMMERCIAL = 'COMMERCIAL'

    PROPERTY_TYPE_CHOICES = [
        (HOUSE, 'House'),
        (APARTMENT, 'Apartment'),
        (CONDO, 'Condo'),
        (TOWNHOUSE, 'Townhouse'),
        (LAND, 'Land'),
        (COMMERCIAL, 'Commercial'),
    ]

    AVAILABLE = 'AVAILABLE'
    SOLD = 'SOLD'
    PENDING = 'PENDING'
    RENTED = 'RENTED'

    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (SOLD, 'Sold'),
        (PENDING, 'Pending'),
        (RENTED, 'Rented'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=20)
    bedrooms = models.PositiveIntegerField()
    bathrooms = models.DecimalField(max_digits=3, decimal_places=1)
    area = models.PositiveIntegerField(help_text='Area in square feet')
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=AVAILABLE)
    featured_image = models.ImageField(upload_to='properties/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('properties:property_detail', kwargs={'pk': self.pk})


    @property
    def is_available(self):
        return self.status == self.AVAILABLE

    @property
    def formatted_price(self):
        try:
            return f"${self.price:,.2f}"
        except Exception:
            return str(self.price)


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/gallery/')
    caption = models.CharField(max_length=200, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['uploaded_at']
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'

    def __str__(self):
        return f"{self.property.title} - Image {self.id}" # type: ignore


class Inquiry(models.Model):
    related_property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='inquiries')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries_sent')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Inquiry'
        verbose_name_plural = 'Inquiries'
        indexes = [
            models.Index(fields=['related_property', 'created_at']),
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        user_repr = getattr(self.user, 'username', str(self.user))
        return f"Inquiry from {user_repr} about {self.related_property.title}"

    @property
    def property_owner(self):
        return self.related_property.owner
