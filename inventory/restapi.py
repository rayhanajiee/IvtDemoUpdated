# mobile apps API
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import secrets
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import secrets
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Category
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.contrib.auth import authenticate, login
from django.utils import timezone
from .models import InventoryItem, Category, Condition


def token_required(f):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print(f'Authorization header: {auth_header}')
        
        if not auth_header:
            return JsonResponse({'error': 'Missing token'}, status=401)
        
        token = auth_header.split(' ')[1] if ' ' in auth_header else None
        session_token = request.session.get('token')
        user_id = request.session.get('user_id')

        print(f"Received Token: {token}")
        print(f"Session Token: {session_token}")
        print(f"User ID from Session: {user_id}")
        
        if not token or not session_token or not user_id or token != session_token:
            return JsonResponse({'error': 'Invalid or missing token'}, status=401)

        try:
            request.user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid user'}, status=401)

        return f(request, *args, **kwargs)
    return wrapper


@csrf_exempt
def api_register(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create(username=username, email=email, password=make_password(password))
        return JsonResponse({'message': 'User created successfully'}, status=201)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def api_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        
        user = authenticate(username=username, password=password)
        if user is not None:
            token = secrets.token_urlsafe(32)
            request.session['token'] = token
            request.session['user_id'] = user.id
            print("authenticated")
            session_token = request.session.get('token')
            user_id = request.session.get('user_id')
            print(f'token: {session_token}')
            print(f'user_id: {user_id}')
            return JsonResponse({'message': 'Login successful', 'token': token, 'user_id': user_id }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@token_required
def api_check_inventory(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        inventory_no = data.get('inventory_no')
        try:
            item = InventoryItem.objects.get(no=inventory_no, user=request.user)
            item_data = {
                'name': item.name,
                'category': item.category.name if item.category else None,
                'no': item.no,
                'department': item.department.name if item.department else None,
                'history': item.history,
                'location': item.location,
                'no': item.no,
                'pic': item.pic,
                'bpb_ppat': item.bpb_ppat,
                'bulan': item.bulan,
                'condition': item.condition,
                'digit_1': item.digit_1,
                'digit_23': item.digit_23,
                'digit_45': item.digit_45,
                'kode_asset': item.kode_asset,
                'kode_golongan': item.kode_golongan,
                'kode_jenisunit': item.kode_jenisunit,
                'photo': item.photo.url if item.photo else '',
                'po': item.po,
                'specifications': item.specifications,
                'tahun': item.tahun,
                'tipe_unit': item.tipe_unit,
                'urutan': item.urutan,
                'user': item.user.id,
                'user_id': item.user_id,
            }
            return JsonResponse({'item': item_data}, status=200)
        except InventoryItem.DoesNotExist:
            return JsonResponse({'error': 'Inventory item not found'}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

def category_list(request):
    categories = Category.objects.all().values('id', 'name')  # Mengambil data kategori
    categories_list = list(categories)
    return JsonResponse(categories_list, safe=False)


from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os

@csrf_exempt
@token_required
def api_add_inventory(request):
    if request.method == 'POST':
        # Check if the request contains files (for photo upload)
        if 'photo' in request.FILES:
            print("image file received")
            photo = request.FILES['photo']
        else:
            photo = None

        # Extract other data from the POST request
        no = request.POST.get('no')
        name = request.POST.get('name')
        specifications = request.POST.get('specifications')
        location = request.POST.get('location')
        condition_id = request.POST.get('condition')  # changed from condition to condition_id
        user = request.POST.get('user')
        user_id = request.session.get('user_id')

        if not user_id:
            return JsonResponse({'error': 'User not authenticated'}, status=401)
        
        try:
            user_object = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        try:
            # Fetch the Condition instance using the ID
            condition_instance = Condition.objects.get(id=condition_id)

            # Save the inventory item
            inventory_item = InventoryItem.objects.create(
                no=no,
                name=name,
                specifications=specifications,
                location=location,
                condition=condition_instance,  # Assign the instance here
                pic=user,
                user=user_object
            )

            # If there's an uploaded photo, save it
            if photo:
                print("saving images..")
                file_path = default_storage.save(f'images/{photo.name}', ContentFile(photo.read()))
                inventory_item.photo = file_path
                inventory_item.save()

            return JsonResponse({'message': 'Inventory item created successfully'}, status=201)

        except Condition.DoesNotExist:
            return JsonResponse({'error': 'Condition not found'}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

# @csrf_exempt
# @token_required
# def api_add_inventory(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
        
#         no = data.get('no')
#         name = data.get('name')
#         specifications = data.get('specifications')
#         location = data.get('location')
#         condition = data.get('condition')
#         user = data.get('user')
        
#         user_id = request.session.get('user_id')
#         if not user_id:
#             return JsonResponse({'error': 'User not authenticated'}, status=401)
        
#         try:
#             user = User.objects.get(id=user_id)
#         except User.DoesNotExist:
#             return JsonResponse({'error': 'User not found'}, status=404)
        
#         # Save the inventory item
#         try:
#             InventoryItem.objects.create(
#                 no=no,
#                 name=name,
#                 specifications=specifications,
#                 location=location,
#                 condition=condition,
#                 pic=user,
#                 user=user
#             )
#             return JsonResponse({'message': 'Inventory item created successfully'}, status=201)
#         except Category.DoesNotExist:
#             return JsonResponse({'error': 'Category not found'}, status=400)
    
#     return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@token_required
def api_moving(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            no_inventaris = data.get('no_inventaris')
            move_to = data.get('move_to')
            move_by = data.get('move_by')

            if not no_inventaris or not move_to or not move_by:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                item = InventoryItem.objects.get(no=no_inventaris)
            except InventoryItem.DoesNotExist:
                return JsonResponse({'error': 'Inventory item not found'}, status=404)

            current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            new_history_entry = f'move_by: "{move_by}", move_to: "{move_to}", at: "{current_time}"'
            if item.history:
                item.history = f'{item.history}\n{new_history_entry}'
            else:
                item.history = new_history_entry

            item.location = move_to
            item.save()

            return JsonResponse({'message': 'Inventory moving history updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    

@csrf_exempt
@token_required
def api_service(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            no_inventaris = data.get('no_inventaris')
            service_by = data.get('service_by')
            service_details = data.get('service_details')

            if not no_inventaris or not service_by or not service_details:
                return JsonResponse({'error': 'Missing required fields'}, status=400)

            try:
                item = InventoryItem.objects.get(no=no_inventaris)
            except InventoryItem.DoesNotExist:
                return JsonResponse({'error': 'Inventory item not found'}, status=404)                                      

            current_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
            new_history_entry = f'service_by: "{service_by}", service_details: "{service_details}", at: "{current_time}"'
            if item.history:
                item.history = f'{item.history}\n{new_history_entry}'
            else:
                item.history = new_history_entry

            item.save()

            return JsonResponse({'message': 'Inventory service history updated successfully'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
