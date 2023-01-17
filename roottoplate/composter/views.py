from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from composter.forms import InputEntryForm, InputForm, TempEntryForm, OutputForm
from composter.forms import RestaurantForm, UserForm, InputTypeForm, ChangePasswordForm
import datetime


def index(request):
    return render(request, "composter/index.html")


def about(request):
    return render(request, "composter/about.html")


def composter(request):
    return render(request, "composter/composter.html")


@csrf_protect
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return HttpResponse("Your account is disabled")
        else:
            return HttpResponse("Invalid login details")
    else:
        return render(request, 'composter/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


@login_required
def input_entry(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        entry_form = InputEntryForm(request.POST)
        input_form1 = InputForm(request.POST)
        input_form2 = InputForm(request.POST)
        input_form3 = InputForm(request.POST)
        input_forms = [input_form1, input_form2, input_form3]

        # only the first input form needs to be valid
        if entry_form.is_valid() and input_form1.is_valid():
            entry = entry_form.save(commit=False)
            entry.user = user
            entry.save()
            for input_instance in input_forms:
                if input_instance.data['inputType'] is not None and int(input_instance.data['inputAmount']) > 0:
                    input_instance = input_instance.save(commit=False)
                    input_instance.inputEntry = entry
                    input_instance.save()

            return redirect(reverse('composter:composter'))
        else:
            print(entry_form.errors)
            for input_instance in input_forms:
                print(input_instance.errors)
    else:
        entry_form = InputEntryForm()
        input_form1 = InputForm()
        input_form2 = InputForm()
        input_form3 = InputForm()
    context = {'entry_form': entry_form, 'input_form1': input_form1, 'input_form2': input_form2, 'input_form3': input_form3}
    return render(request, 'composter/compost_form.html', context)


@login_required
def temp_entry(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        temp_form = TempEntryForm(request.POST)
        if temp_form.is_valid():
            temperature = temp_form.save(commit=False)
            temperature.user = user
            temperature.save()
            return redirect(reverse('composter:composter'))
        else:
            print(temp_form.errors)

    else:
        temp_form = TempEntryForm()
    return render(request, 'composter/temperature_form.html', {'temperature_form': temp_form})


@login_required
def output_entry(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        output_form = OutputForm(request.POST)
        if output_form.is_valid():
            output = output_form.save(commit=False)
            output.user = user
            output.save()
            return redirect(reverse('composter:composter'))
        else:
            print(output_form.errors)
    else:
        output_form = OutputForm()
    return render(request, 'composter/compost_output_form.html', {'output_form': output_form})


def restaurant_request_form(request):
    if request.method == "POST":
        restaurant_form = RestaurantForm(request.POST)
        if restaurant_form.is_valid():
            restaurant_req = restaurant_form.save(commit=False)
            restaurant_req.dateRequested = datetime.date.today()
            restaurant_req.save()
            return redirect(reverse('composter:home'))
        else:
            print(restaurant_form.errors)

    else:
        restaurant_form = RestaurantForm()
    return render(request, 'composter/restaurant_form.html', {'restaurant_form': restaurant_form})


# admin only views
@login_required
def add_user(request):
    user = User.objects.get(username=request.user.username)
    if not user.is_staff:
        messages.error(request, "You are not authorised to access this.")
        return redirect('composter:home')
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            new_user = form.cleaned_data.get('uesrname')
            messages.success(request, 'Account was created for ' + new_user)
            return redirect('composter:add_user')
    else:
        form = UserForm()
    return render(request, 'composter/admin_add_user.html', {'form': form})


@login_required
def add_input_type(request):
    user = User.objects.get(username=request.user.username)
    if not user.is_staff:
        messages.error(request, "You are not authorised to access this.")
        return redirect('composter:home')
    if request.method == 'POST':
        form = InputTypeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('composter:add_imput_type')
        else:
            print(form.errors)
    else:
        form = InputTypeForm()
    return render(request, 'composter/admin_add_input_type.html', {'form': form})


@login_required
def change_password(request):
    user = User.objects.get(username=request.user.username)
    if not user.is_staff:
        messages.error(request, "You are not authorised to access this.")
        return redirect('composter:home')
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('composter:manage_users')
        else:
            print(form.errors)
    else:
        form = ChangePasswordForm()
    return render(request, 'composter/admin_change_password.html', {'form': form})