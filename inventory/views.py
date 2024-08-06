from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm
from .models import InventoryItem, Category, Department
from django.http import HttpResponse
from openpyxl import Workbook
from io import BytesIO

def ExportData(request):
    # Create a workbook and a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = 'Inventory Data'

    # Define the header
    headers = [
        'No Inventaris', 'Item', 'Kode Asset', 'Photo', 'Specifications', 'Department', 
        'Category', 'Location', 'PIC', 'Condition', 'Date Created', 'History', 
        'Tipe Unit', 'User'
    ]
    ws.append(headers)

    # Fetch the data and write to the worksheet
    items = InventoryItem.objects.filter(user=request.user)
    for item in items:
        # Remove timezone information from datetime objects
        date_created = item.date_created.replace(tzinfo=None) if item.date_created else ''
        
        ws.append([
            item.no,
            item.name,
            item.kode_asset,
            item.photo.url if item.photo else '',  # Include the photo URL if it exists
            item.specifications,
            item.department.name if item.department else '',
            item.category.name if item.category else '',
            item.location,
            item.user.get_full_name() if item.user else '',
            item.condition,
            date_created,  # Use the naive datetime without timezone
            item.history,
            item.tipe_unit,
            item.user.username if item.user else '',
        ])

    # Save the workbook to a BytesIO object
    output = BytesIO()
    wb.save(output)
    output.seek(0)

    # Create the response with the Excel file
    response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=inventory_data.xlsx'

    return response

def upload_image(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('upload_image')
    else:
        form = InventoryItemForm()
    return render(request, 'upload_image.html', {'form': form})

def image_gallery(request):
    items = InventoryItem.objects.all()
    return render(request, 'image_gallery.html', {'items': items})

class Index(TemplateView):
    template_name = 'inventory/index.html'

class Dashboard(LoginRequiredMixin, View):
    def get(self, request):
        items = InventoryItem.objects.filter(user=request.user).order_by('id')
        items_data = serializers.serialize('json', items)

        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'items_data': items_data
        })

class SignUpView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'inventory/signup.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1']
            )
            if user is not None:
                login(request, user)
                return redirect('index')

        return render(request, 'inventory/signup.html', {'form': form})

class AddItem(LoginRequiredMixin, CreateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['departments'] = Department.objects.all()
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class EditItem(LoginRequiredMixin, UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

class DeleteItem(LoginRequiredMixin, DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    context_object_name = 'item'
