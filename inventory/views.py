from django.core import serializers
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserRegisterForm, InventoryItemForm, DescriptionForm
from .models import InventoryItem, Category, Department, Condition, DescriptionModel
from django.http import HttpResponse, JsonResponse
from openpyxl import Workbook
from io import BytesIO


def save_code_description(request):
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Retrieve the user inputs
        first_digit = request.POST.get('first_digit')
        second_digit = request.POST.get('second_digit')
        third_digit = request.POST.get('third_digit')
        day = request.POST.get('day')
        month = request.POST.get('month')
        year = request.POST.get('year')

        # Save the inputs to the database
        description = DescriptionModel.objects.create(
            first_digit=first_digit,
            second_digit=second_digit,
            third_digit=third_digit,
            day=day,
            month=month,
            year=year
        )

        # Retrieve all saved descriptions to update the table
        descriptions = DescriptionModel.objects.all().values()

        # Return a JSON response for AJAX requests
        return JsonResponse({'descriptions': list(descriptions)})
    
    # For non-AJAX requests (initial page load), render the page normally
    descriptions = DescriptionModel.objects.all()  # Retrieve all descriptions

    return render(request, 'inventory/item_form.html', {
        'descriptions': descriptions,
    })
    
    # For GET requests or non-AJAX POST requests, render the page normally
    form = DescriptionForm()
    descriptions = DescriptionModel.objects.all()

    return render(request, 'inventory/item_form.html', {
        'form': form,
        'descriptions': descriptions,
    })

def ExportData(request):
    # Create a workbook and a worksheet
    wb = Workbook()
    ws = wb.active
    ws.title = 'Inventory Data'

    # Define the header
    headers = [
        'Date Created','No Inventaris', 'Item', 'Photo', 'Specifications', 'Department', 
        'Category', 'Location', 'PIC', 'Condition', 'History', 
        'Tipe Unit', 'Input by', 'digit_1', 'kode_asset','digit_23', 'kode_golongan',
        'digit_45', 'kdoe_jenisunit', 'urutan', 'bulan', 'tahun', 'bpb_ppat',
        'po',
    ]
    ws.append(headers)

    # Fetch the data and write to the worksheet
    items = InventoryItem.objects.all() if request.user.is_superuser else InventoryItem.objects.filter(user=request.user)
    for item in items:
        # Remove timezone information from datetime objects
        date_created = item.date_created.replace(tzinfo=None) if item.date_created else ''
        
        ws.append([
            date_created,
            item.no,
            item.name,
            item.photo.url if item.photo else '',  # Include the photo URL if it exists
            item.specifications,
            item.department.name if item.department else '',
            item.category.name if item.category else '',
            item.location,
            item.pic if item.pic else '',
            item.condition.name,
            item.history,
            item.tipe_unit,
            item.user.username if item.user else '',
            item.digit_1,
            item.kode_asset,
            item.digit_23,
            item.kode_golongan,
            item.digit_45,
            item.kode_jenisunit,
            item.urutan,
            item.bulan,
            item.tahun,
            item.bpb_ppat,
            item.po
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
        conditions = Condition.objects.all()
        selected_condition = request.GET.get('condition_name', '')

        if selected_condition:
            items = InventoryItem.objects.filter(condition__name=selected_condition)
        else:
            items = InventoryItem.objects.all() if request.user.is_superuser else InventoryItem.objects.filter(user=request.user).order_by('id')

        items_data = serializers.serialize('json', items)

        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'items_data': items_data,
            'conditions': conditions,
            'selected_condition': selected_condition,
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
        context['conditions'] = Condition.objects.all()
        context['descriptions'] = DescriptionModel.objects.all()  # Pulling data from DescriptionModel
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

class CustomLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('inventory/logout.html')
