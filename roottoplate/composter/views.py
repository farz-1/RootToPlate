from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_protect
from composter.forms import InputForm, InputEntryForm
from composter.models import UserProfile


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
    user = UserProfile.objects.get(username=request.user.username)
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
                if input_instance.inputType is not None and input_instance.inputAmount > 0:
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
