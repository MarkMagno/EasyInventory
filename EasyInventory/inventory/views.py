from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.html import escape
from django.contrib.auth.models import User
from .models import Equipment, UserProfile, CheckoutRequest
from .forms import EquipmentForm, CheckoutRequestForm, UserForm
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.contrib import messages

# Utility function to check if the user is an admin
def is_admin(user):
    return UserProfile.objects.filter(user=user, role='admin').exists()

### Admin Views ###

@login_required
@user_passes_test(is_admin)
def inventory_list(request):
    search_query = request.GET.get('search', '')
    search_query = escape(search_query)  # Escape search query
    equipment = Equipment.objects.all()

    if search_query:
        equipment = equipment.filter(
            Q(asset_number__icontains=search_query) |
            Q(model_number__icontains=search_query) |
            Q(checked_out_to__username__icontains=search_query) |
            Q(due_date__icontains=search_query)
        )

    return render(request, 'inventory/admin_inventory.html', {'equipment': equipment})


@login_required
@user_passes_test(is_admin)
def user_list(request):
    users = UserProfile.objects.select_related('user').all()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            username = escape(form.cleaned_data['username'])  # Escape username
            user = form.save(commit=False)
            user.username = username
            user.save()
            role = escape(form.cleaned_data['role'])  # Escape role
            UserProfile.objects.create(user=user, role=role)
            return redirect('admin_users')
    else:
        form = UserForm()

    return render(request, 'inventory/admin_users.html', {'users': users, 'form': form})


@login_required
@user_passes_test(is_admin)
def new_equipment(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            form.instance.asset_number = escape(form.cleaned_data['asset_number'])
            form.instance.model_number = escape(form.cleaned_data['model_number'])
            form.save()
            return redirect('admin_inventory')
    else:
        form = EquipmentForm()

    return render(request, 'inventory/new_equipment.html', {'form': form})


@login_required
@user_passes_test(is_admin)
def checkout_requests(request):
    requests = CheckoutRequest.objects.filter(status='pending')

    if request.method == 'POST':
        request_id = escape(request.POST.get('request_id'))
        action = escape(request.POST.get('action'))
        checkout_request = get_object_or_404(CheckoutRequest, id=request_id)

        if action == 'approve':
            checkout_request.approve()
        elif action == 'deny':
            checkout_request.deny()

        return redirect('/administrator/inventory')

    return render(request, 'inventory/admin_checkout_requests.html', {'requests': requests})


@login_required
@user_passes_test(is_admin)
def check_in(request):
    equipment = Equipment.objects.filter(due_date__isnull=False, checked_out_to__isnull=False)

    if request.method == 'POST':
        equipment_id = escape(request.POST.get('equipment_id'))
        equipment_item = get_object_or_404(Equipment, id=equipment_id)
        equipment_item.due_date = None
        equipment_item.checked_out_to = None
        equipment_item.save()
        return redirect('check_in')

    return render(request, 'inventory/admin_check_in.html', {'equipment': equipment})


### User Views ###

def user_page(request):
    user = request.user if request.user.is_authenticated else None

    # Define the filtered form class
    class FilteredCheckoutRequestForm(CheckoutRequestForm):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['equipment'].queryset = Equipment.objects.filter(
                checked_out_to__isnull=True, due_date__isnull=True
            )

    if request.method == 'POST':
        if not user:  # If the user is not logged in, redirect to the login page
            return redirect('login_view')

        form = FilteredCheckoutRequestForm(request.POST)
        if form.is_valid():
            checkout_request = form.save(commit=False)
            checkout_request.user = user
            checkout_request.use_case = escape(form.cleaned_data['use_case'])  # Escape use_case
            checkout_request.save()
            return redirect('user')
    else:
        form = FilteredCheckoutRequestForm()

    checked_out_equipment = Equipment.objects.filter(checked_out_to=user) if user else None

    return render(request, 'inventory/user.html', {
        'form': form,
        'equipment': checked_out_equipment,
    })


@login_required
@user_passes_test(is_admin)
def user_action(request, user_id):
    user = get_object_or_404(User, id=user_id)
    action = escape(request.POST.get('action'))

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
        return redirect('admin_users')

    user.save()
    return redirect('admin_users')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect based on user role
                if hasattr(user, 'userprofile') and user.userprofile.role == 'admin':
                    return redirect('admin_inventory')
                else:
                    return redirect('user')
            else:
                messages.error(request, 'This account is inactive.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

