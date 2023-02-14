from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView
from composter.forms import InputEntryForm, InputFormSet, TempEntryForm, OutputForm
from composter.forms import RestaurantForm, UserForm, InputTypeForm, ChangePasswordForm
from composter.models import InputType, Input, TemperatureEntry
import datetime


def index(request):
    typeNames = [x.name for x in InputType.objects.all()]
    typeCounts = [float(sum(y.inputAmount for y in Input.objects.filter(inputType=x))) for x in typeNames]
    # remove counts of 0
    n = len(typeNames) - 1
    for i in range(n + 1):
        if typeCounts[n-i] == 0:
            del typeCounts[n-i]
            del typeNames[n-i]

    tempEntries = TemperatureEntry.objects.all().order_by('entryTime').values()
    if len(tempEntries) > 30:
        tempEntries = tempEntries[-30:]

    tempTimes = [x.get('entryTime').strftime("%d/%m/%Y") for x in tempEntries]

    context = {'typeNames': typeNames, 'typeCounts': typeCounts, 'tempEntries': tempEntries, 'tempTimes': tempTimes}
    return render(request, "composter/index.html", context)


def about(request):
    return render(request, "composter/about.html")


def composter(request):
    return render(request, "composter/composter.html")


@csrf_protect
def user_login(request):
    if request.user.is_authenticated:
        messages.error(request, "You are already logged in.")
        return redirect(reverse('index'))
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


@login_required(login_url='/composter/login/')
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


class InputFormView(TemplateView):
    template_name = "composter/compost_form.html"

    @method_decorator(login_required(login_url='/composter/login/'))
    def get(self, *args, **kwargs):
        context = {'input_formset': InputFormSet, 'entry_form': InputEntryForm()}
        return self.render_to_response(context)

    @method_decorator(login_required(login_url='/composter/login/'))
    def post(self, request, *args, **kwargs):
        user = User.objects.get(username=self.request.user.username)

        entry_form = InputEntryForm(self.request.POST)
        input_formset = InputFormSet(self.request.POST)

        if entry_form.is_valid() and input_formset.is_valid():
            entry = entry_form.save(commit=False)
            entry.user = user
            entry.save()
            for inputs in input_formset:
                input = inputs.save(commit=False)
                input.inputEntry = entry
                input.save()
            return redirect(reverse('composter:composter'))
        else:
            print(entry_form.errors)
            for inputs in input_formset:
                print(inputs.errors)
        context = {'input_formset': input_formset, 'entry_form': entry_form}
        return render(request, self.template_name, context)


@login_required(login_url='/composter/login/')
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


@login_required(login_url='/composter/login/')
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
            restaurant_req.dateRequested = datetime.datetime.now()
            restaurant_req.save()
            return redirect(reverse('composter:index'))
        else:
            print(restaurant_form.errors)

    else:
        restaurant_form = RestaurantForm()
    return render(request, 'composter/restaurant_form.html', {'restaurant_form': restaurant_form})


# admin only views
@login_required(login_url='/composter/')
def simple_admin(request):
    user = User.objects.get(username=request.user.username)
    context = {'user_form': UserForm(), 'input_type_form': InputTypeForm(), 'change_password_form': ChangePasswordForm()}
    if not user.is_staff:
        messages.error(request, "You are not authorised to access this.")
        return redirect('composter:index')
    if request.method == 'POST':
        # deal with each form and add success message if successful
        if 'add_user' in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                context['success_message'] = f"New user {user_form.data['username']} added."
            else:
                context['user_form'] = user_form
        elif 'change_password' in request.POST:
            change_password_form = ChangePasswordForm(request.POST)
            if change_password_form.data['username'] is not None and change_password_form.data['password'] is not None:
                changed_user = User.objects.get(username=change_password_form.data['username'])
                changed_user.set_password(change_password_form.data['password'])
                changed_user.save()
                context['success_message'] = f"Password for user {change_password_form.data['username']} changed."
            else:
                context['change_password_form'] = change_password_form
        elif 'add_input_type' in request.POST:
            input_type_form = InputTypeForm(request.POST)
            if input_type_form.is_valid():
                input_type_form.save()
                context['success_message'] = f"Input type {input_type_form.data['name']} added successfully"
            else:
                context['input_type_form'] = input_type_form
    return render(request, 'composter/simple_admin.html', context)
