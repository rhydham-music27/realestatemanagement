from django import forms
from .models import Property, PropertyImage, Inquiry


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title',
            'description',
            'price',
            'address',
            'city',
            'state',
            'zipcode',
            'bedrooms',
            'bathrooms',
            'area',
            'property_type',
            'status',
            'featured_image',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
            'bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'bathrooms': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.5'}),
            'area': forms.NumberInput(attrs={'class': 'form-control'}),
            'property_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
        labels = {
            'area': 'Area (sq ft)',
            'property_type': 'Property Type',
            'featured_image': 'Main Property Image',
        }
        help_texts = {
            'featured_image': 'Upload the main image for this property',
            'price': 'Enter price in USD',
        }


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image', 'caption']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'caption': forms.TextInput(attrs={'class': 'form-control'}),
        }


class PropertySearchFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search by city or state...'}),
        label='Location Search',
    )
    property_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Types')] + Property.PROPERTY_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Property Type',
    )
    min_price = forms.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Min', 'step': '1000'}),
        label='Min Price',
    )
    max_price = forms.DecimalField(
        required=False,
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max', 'step': '1000'}),
        label='Max Price',
    )
    bedrooms = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Any', 'min': '0'}),
        label='Min Bedrooms',
    )
    bathrooms = forms.DecimalField(
        required=False,
        max_digits=3,
        decimal_places=1,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Any', 'min': '0', 'step': '0.5'}),
        label='Min Bathrooms',
    )
    SORT_CHOICES = [
        ('', 'Newest First'),
        ('price_asc', 'Price: Low to High'),
        ('price_desc', 'Price: High to Low'),
        ('area_asc', 'Area: Small to Large'),
        ('area_desc', 'Area: Large to Small'),
        ('oldest', 'Oldest First'),
    ]
    sort = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Sort By',
    )


class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Phone (optional)'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'I am interested in this property...'}),
        }
        labels = {
            'name': 'Your Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'message': 'Your Message',
        }
        help_texts = {
            'message': 'Tell the property owner why you are interested',
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if user and user.is_authenticated:
                full_name = user.get_full_name() or user.username
                if not self.initial.get('name'):
                    self.initial['name'] = full_name
                if not self.initial.get('email'):
                    self.initial['email'] = user.email
                # try to prefill phone from profile if available
                profile = getattr(user, 'userprofile', None)
                if profile and getattr(profile, 'phone', None) and not self.initial.get('phone'):
                    self.initial['phone'] = profile.phone
        except Exception:
            pass
