from django.urls import path
from .views import (
    PropertyListView,
    PropertyDetailView,
    PropertyCreateView,
    PropertyUpdateView,
    PropertyDeleteView,
    inquiry_create_view,
    InquiryListView,
    InquiryDetailView,
)

app_name = 'properties'

urlpatterns = [
    path('', PropertyListView.as_view(), name='property_list'),
    path('property/<int:pk>/', PropertyDetailView.as_view(), name='property_detail'),
    path('property/<int:pk>/inquiry/', inquiry_create_view, name='inquiry_create'),
    path('property/new/', PropertyCreateView.as_view(), name='property_create'),
    path('property/<int:pk>/edit/', PropertyUpdateView.as_view(), name='property_update'),
    path('property/<int:pk>/delete/', PropertyDeleteView.as_view(), name='property_delete'),
    path('inquiries/', InquiryListView.as_view(), name='inquiry_list'),
    path('inquiry/<int:pk>/', InquiryDetailView.as_view(), name='inquiry_detail'),
]
