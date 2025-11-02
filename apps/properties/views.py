from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings

from .models import Property, Inquiry
from .forms import PropertyForm, PropertySearchFilterForm, InquiryForm


class PropertyListView(ListView):
	model = Property
	template_name = 'properties/property_list.html'
	context_object_name = 'properties'
	paginate_by = 10

	def get_queryset(self):
		queryset = Property.objects.filter(status=Property.AVAILABLE)

		# bind filter form to GET params
		data = self.request.GET
		search = data.get('search')
		property_type = data.get('property_type')
		min_price = data.get('min_price')
		max_price = data.get('max_price')
		bedrooms = data.get('bedrooms')
		bathrooms = data.get('bathrooms')
		sort = data.get('sort')

		if search:
			queryset = queryset.filter(Q(city__icontains=search) | Q(state__icontains=search))

		if property_type:
			queryset = queryset.filter(property_type=property_type)

		try:
			if min_price:
				queryset = queryset.filter(price__gte=min_price)
		except Exception:
			pass

		try:
			if max_price:
				queryset = queryset.filter(price__lte=max_price)
		except Exception:
			pass

		try:
			if bedrooms:
				queryset = queryset.filter(bedrooms__gte=int(bedrooms))
		except Exception:
			pass

		try:
			if bathrooms:
				queryset = queryset.filter(bathrooms__gte=float(bathrooms))
		except Exception:
			pass

		# Sorting options
		if sort == 'price_asc':
			queryset = queryset.order_by('price')
		elif sort == 'price_desc':
			queryset = queryset.order_by('-price')
		elif sort == 'area_asc':
			queryset = queryset.order_by('area')
		elif sort == 'area_desc':
			queryset = queryset.order_by('-area')
		elif sort == 'oldest':
			queryset = queryset.order_by('created_at')
		else:
			queryset = queryset.order_by('-created_at')

		return queryset

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		qs = self.get_queryset()
		context['total_properties'] = qs.count()
		# filter form bound to GET params
		context['filter_form'] = PropertySearchFilterForm(self.request.GET)
		# indicate if any filters are active
		context['has_filters'] = any(self.request.GET.get(k) for k in ['search', 'property_type', 'min_price', 'max_price', 'bedrooms', 'bathrooms'])
		# copy GET params for pagination links
		params = self.request.GET.copy()
		context['query_params'] = params
		return context


class PropertyDetailView(DetailView):
	model = Property
	template_name = 'properties/property_detail.html'
	context_object_name = 'property'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['images'] = self.object.images.all() # type: ignore
		context['is_owner'] = self.request.user == self.object.owner # type: ignore
		# Inquiry form and context for detail page
		if self.request.user.is_authenticated:
			if context['is_owner']:
				# show unread inquiry count for owner
				context['inquiry_count'] = self.object.inquiries.filter(is_read=False).count() # type: ignore
			else:
				context['inquiry_form'] = InquiryForm(user=self.request.user)
		else:
			context['show_login_prompt'] = True
		return context


@login_required
def inquiry_create_view(request, pk):
	property_obj = get_object_or_404(Property, pk=pk)
	# owners cannot inquire on their own property
	if property_obj.owner == request.user:
		messages.error(request, 'You cannot send an inquiry to your own listing.')
		return redirect('properties:property_detail', pk=property_obj.pk)

	if request.method == 'POST':
		form = InquiryForm(request.POST, user=request.user)
		if form.is_valid():
			inquiry = form.save(commit=False)
			inquiry.related_property = property_obj
			inquiry.user = request.user
			inquiry.save()
			# send notification email to property owner (console backend in dev)
			subject = f"New Inquiry for {property_obj.title}"
			message = (
				f"You have received a new inquiry for your property '{property_obj.title}'.\n\n"
				f"From: {inquiry.name} ({inquiry.email})\n"
				f"Phone: {inquiry.phone or 'N/A'}\n\n"
				f"Message:\n{inquiry.message}\n\n"
				f"View property: {request.build_absolute_uri(property_obj.get_absolute_url())}\n"
			)
			from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@realestate.com')
			recipient_list = [property_obj.owner.email] if property_obj.owner.email else []
			try:
				if recipient_list:
					send_mail(subject, message, from_email, recipient_list, fail_silently=False)
			except Exception:
				# don't block inquiry saving on email failure
				messages.warning(request, 'Inquiry saved, but failed to send notification email.')
			else:
				messages.success(request, 'Your inquiry has been sent successfully!')
			return redirect('properties:property_detail', pk=property_obj.pk)
		else:
			# keep the user on the property detail page and show errors
			for field, errors in form.errors.items():
				messages.error(request, f"{field}: {'; '.join(errors)}") # type: ignore
			return redirect('properties:property_detail', pk=property_obj.pk)
	# fallback: redirect to property page
	return redirect('properties:property_detail', pk=property_obj.pk)


class InquiryListView(LoginRequiredMixin, ListView):
	model = Inquiry
	template_name = 'properties/inquiry_list.html'
	context_object_name = 'inquiries'
	paginate_by = 20

	def get_queryset(self):
		filter_type = self.request.GET.get('filter', 'received')
		qs = Inquiry.objects.select_related('property', 'user')
		if filter_type == 'received':
			# inquiries for properties owned by the user
			return qs.filter(property__owner=self.request.user).order_by('-created_at')
		elif filter_type == 'sent':
			return qs.filter(user=self.request.user).order_by('-created_at')
		# default
		return qs.filter(property__owner=self.request.user).order_by('-created_at')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		filter_type = self.request.GET.get('filter', 'received')
		context['filter_type'] = filter_type
		context['received_count'] = Inquiry.objects.filter(property__owner=self.request.user).count()
		context['sent_count'] = Inquiry.objects.filter(user=self.request.user).count()
		return context


class InquiryDetailView(LoginRequiredMixin, DetailView):
	model = Inquiry
	template_name = 'properties/inquiry_detail.html'
	context_object_name = 'inquiry'

	def get_queryset(self):
		# only allow owners or inquirers to view
		return Inquiry.objects.filter(Q(property__owner=self.request.user) | Q(user=self.request.user)).select_related('property', 'user')

	def get_object(self, queryset=None):
		obj = super().get_object(queryset=queryset)
		# if owner views and inquiry unread mark as read
		if self.request.user == obj.property.owner and not obj.is_read: # type: ignore
			obj.is_read = True # type: ignore
			obj.save()
		return obj


class PropertyCreateView(LoginRequiredMixin, CreateView):
	model = Property
	form_class = PropertyForm
	template_name = 'properties/property_form.html'
	success_url = reverse_lazy('properties:property_list')

	def form_valid(self, form):
		# assign owner and save
		self.object = form.save(commit=False)
		self.object.owner = self.request.user
		self.object.save()
		messages.success(self.request, 'Property created successfully!')
		return redirect(self.get_success_url())

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form_title'] = 'Add Property'
		return context


class PropertyUpdateView(LoginRequiredMixin, UpdateView):
	model = Property
	form_class = PropertyForm
	template_name = 'properties/property_form.html'
	success_url = reverse_lazy('properties:property_list')

	def get_queryset(self):
		# only allow owners to update their properties
		return Property.objects.filter(owner=self.request.user)

	def form_valid(self, form):
		response = super().form_valid(form)
		messages.success(self.request, 'Property updated successfully!')
		return response

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form_title'] = 'Edit Property'
		return context


class PropertyDeleteView(LoginRequiredMixin, DeleteView):
	model = Property
	template_name = 'properties/property_confirm_delete.html'
	success_url = reverse_lazy('properties:property_list')
	context_object_name = 'property'

	def get_queryset(self):
		return Property.objects.filter(owner=self.request.user)

	def delete(self, request, *args, **kwargs):
		messages.success(self.request, 'Property deleted successfully!')
		return super().delete(request, *args, **kwargs)

