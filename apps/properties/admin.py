from django.contrib import admin
from .models import Property, PropertyImage, Inquiry


class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 3
    fields = ['image', 'caption']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price', 'city', 'bedrooms', 'bathrooms', 'status', 'created_at']
    list_filter = ['status', 'property_type', 'city', 'bedrooms', 'bathrooms']
    search_fields = ['title', 'description', 'address', 'city']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [PropertyImageInline]
    fieldsets = (
        ('Basic Information', {'fields': ('title', 'description', 'owner')}),
        ('Property Details', {'fields': ('property_type', 'status', 'featured_image')}),
        ('Specifications', {'fields': ('bedrooms', 'bathrooms', 'area')}),
        ('Location', {'fields': ('address', 'city', 'state', 'zipcode')}),
        ('Pricing', {'fields': ('price',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['property__title', 'caption']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['related_property', 'user', 'name', 'email', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at', 'related_property__property_type']
    search_fields = ['property__title', 'user__username', 'name', 'email', 'message']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    list_editable = ['is_read']
    list_per_page = 25
    fieldsets = (
        ('Property & User', {'fields': ('property', 'user')}),
        ('Contact Information', {'fields': ('name', 'email', 'phone')}),
        ('Message', {'fields': ('message',)}),
        ('Status', {'fields': ('is_read', 'created_at')}),
    )
    actions = ['mark_as_read', 'mark_as_unread']

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('property', 'user')

    def mark_as_read(self, request, queryset):
        updated = queryset.update(is_read=True)
        self.message_user(request, f"{updated} inquiries marked as read.")
    mark_as_read.short_description = 'Mark selected inquiries as read' # type: ignore

    def mark_as_unread(self, request, queryset):
        updated = queryset.update(is_read=False)
        self.message_user(request, f"{updated} inquiries marked as unread.")
    mark_as_unread.short_description = 'Mark selected inquiries as unread' # type: ignore
