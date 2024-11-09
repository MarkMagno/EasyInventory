from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from .models import Equipment, UserProfile, CheckoutRequest
from .forms import EquipmentForm, CheckoutRequestForm, UserForm
from django.db.models import Q
from datetime import date

# Utility function to check if the user is an admin
def is_admin(user):
    return UserProfile.objects.filter(user=user, role='admin').exists()

### Admin Views ###

## Login functionality not working commented out for now

# Admin view to list all equipment and handle search functionality
##@login_required
##@user_passes_test(is_admin)
def inventory_list(request):
    search_query = request.GET.get('search', '')
    equipment = Equipment.objects.all()
    
    # Handle different search filters
    if search_query:
        equipment = equipment.filter(
            Q(asset_number__icontains=search_query) |
            Q(model_number__icontains=search_query) |
            Q(checked_out_to__username__icontains=search_query) |
            Q(due_date__icontains=search_query)
        )

    return render(request, 'inventory/admin_inventory.html', {'equipment': equipment})

# Admin view to list and manage users
##@login_required
##@user_passes_test(is_admin)
def user_list(request):
    users = UserProfile.objects.select_related('user').all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save User without committing
            user.save()  # Save the user (hashes password)
            role = form.cleaned_data['role']
            UserProfile.objects.create(user=user, role=role)  # Create UserProfile
            return redirect('admin_users')  # Refresh the page to show the new user
    else:
        form = UserForm()
    
    return render(request, 'inventory/admin_users.html', {'users': users, 'form': form})

# Admin view to create new equipment entries
##@login_required
##@user_passes_test(is_admin)
def new_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_inventory')
    else:
        form = EquipmentForm()
    return render(request, 'inventory/new_equipment.html', {'form': form})

# Admin view to approve or deny checkout requests
##@login_required
##@user_passes_test(is_admin)
from django.shortcuts import render, redirect, get_object_or_404
from .models import CheckoutRequest

##@login_required
##@user_passes_test(is_admin)  # Assuming is_admin is a function that checks admin privileges
def checkout_requests(request):
    requests = CheckoutRequest.objects.filter(status='pending')
    
    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')
        checkout_request = get_object_or_404(CheckoutRequest, id=request_id)
        
        if action == 'approve':
            checkout_request.approve()
        elif action == 'deny':
            checkout_request.deny()

        # Redirect to the inventory page after processing the request
        return redirect('/administrator/inventory')

    return render(request, 'inventory/admin_checkout_requests.html', {'requests': requests})


# Admin view to check in equipment
##@login_required
##@user_passes_test(is_admin)
def check_in(request):
    equipment = Equipment.objects.filter(due_date__isnull=False, checked_out_to__isnull=False)

    if request.method == 'POST':
        equipment_id = request.POST.get('equipment_id')
        equipment_item = get_object_or_404(Equipment, id=equipment_id)
        equipment_item.due_date = None
        equipment_item.checked_out_to = None
        equipment_item.save()
        return redirect('check_in')

    return render(request, 'inventory/admin_check_in.html', {'equipment': equipment})

### User Views ###

# User view to see their checked-out equipment
##@login_required
def user_equipment(request):
    user = request.user
    checked_out_equipment = Equipment.objects.filter(checked_out_to=user)
    return render(request, 'inventory/user_equipment.html', {'equipment': checked_out_equipment})

# User view to submit a checkout request
##@login_required
def user_checkout(request):
    if request.method == 'POST':
        form = CheckoutRequestForm(request.POST)
        if form.is_valid():
            checkout_request = form.save(commit=False)
            checkout_request.user = request.user
            checkout_request.save()
            return redirect('user_equipment')
    else:
        form = CheckoutRequestForm()
    return render(request, 'inventory/user_checkout.html', {'form': form})


##@login_required
##@user_passes_test(is_admin)
def user_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    action = request.POST.get('action')

    if action == 'enable':
        user.is_active = True
    elif action == 'disable':
        user.is_active = False
    elif action == 'unlock':
        profile = UserProfile.objects.get(user=user)
        profile.is_locked = False
        profile.save()
    elif action == 'delete':
        user.delete()
        return redirect('admin_users')  # Redirect to user list after deletion

    user.save()
    return redirect('admin_users')
