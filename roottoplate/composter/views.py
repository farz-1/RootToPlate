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
from composter.forms import InputEntryForm, InputFormSet, TempEntryForm, OutputForm, EnergyForm
from composter.forms import RestaurantForm, UserForm, InputTypeForm, ChangePasswordForm
from composter.models import InputType, Input, InputEntry, TemperatureEntry, RestaurantRequest
from django.utils import timezone
from composter.signals import GraphState


def index(request):
    state = GraphState()
    context = {'typeNames': state.typeNames, 'typePercentages': state.typePercentages,
               'tempEntries': state.tempEntries, 'tempTimes': state.tempTimes, 'tempTimesInt': state.tempTimesInt,
               'cMonth': state.cMonth, 'cYear': state.cYear, 'notEnoughEnergyInfo': state.notEnoughEnergyInfo}
    return render(request, "composter/index.html", context)


def about(request):
    return render(request, "composter/about.html")


def composter(request):
    context = {}
    last_five_entries = InputEntry.objects.all().order_by('-entryTime').values()[:5]

    # get time the composter was last fed
    if last_five_entries:
        compost_last_fed = last_five_entries[0].get('entryTime')
        compost_last_fed_js = compost_last_fed.strftime("%Y-%m-%dT%H:%M:%SZ")
        context = {'compost_last_fed': compost_last_fed, 'compost_last_fed_js': compost_last_fed_js}

        if request.user.is_staff:
            for entry in last_five_entries:
                entry['username'] = User.objects.get(id=entry['user_id']).username
                inputs = Input.objects.filter(inputEntry=entry['entryID']).values()
                entry['inputs'] = [{'type': i.get('inputType_id'), 'amount': i.get('inputAmount')} for i in inputs]
            context['last_five_entries'] = last_five_entries

    return render(request, "composter/composter.html", context)


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
            messages.error(request, "Invalid login details.")

    return render(request, 'composter/login.html')


@login_required(login_url='/composter/login/')
def user_logout(request):
    logout(request)
    return redirect(reverse('index'))


def calculate_mixture_sums(cur_inputs):
    sumN = sum([i['amount'] * i['nitrogen'] * i['moisture'] for i in cur_inputs])
    for i in cur_inputs:
        i['carbon'] = i['nitrogen'] * i['CNRatio']
    sumC = sum([i['amount'] * i['carbon'] * i['moisture'] for i in cur_inputs])
    return sumC, sumN


def calculate_recommended_addition(rec_input, sumC, sumN):
    cn = 27  # ideal carbon nitrogen ratio
    nitrogen, moisture = float(rec_input.nitrogenPercent), 100 - float(rec_input.moisturePercent)
    carbon = float(rec_input.nitrogenPercent * rec_input.CNRatio)
    return (cn * sumN - sumC) / (carbon * moisture - nitrogen * moisture * cn)


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
        context = {}

        if 'get_advice' in self.request.POST and input_formset.is_valid():
            cur_inputs = []
            # get the inputs without saving the form
            for input in input_formset:
                input = input.save(commit=False)
                cur_inputs.append({'amount': float(input.inputAmount),
                                   'nitrogen': float(input.inputType.nitrogenPercent),
                                   'moisture': 100 - float(input.inputType.moisturePercent),
                                   'CNRatio': float(input.inputType.CNRatio)})
            # get the total carbon and nitrogen in the mixture
            sumC, sumN = calculate_mixture_sums(cur_inputs)

            # if the ratio is too big then add more green
            if sumC / sumN > 35:
                rec_input = InputType.objects.get(name='Food waste')
                rec_input_amount = round(calculate_recommended_addition(rec_input, sumC, sumN), 1)
                advice = f"The carbon-nitrogen ratio of this mixture is too high. Recommended addition: roughly {rec_input_amount} of green material. "  # noqa:E501
            # if the ratio is too small then add more brown
            elif sumC / sumN < 20:
                rec_input = InputType.objects.get(name='Wood')
                rec_input_amount = round(calculate_recommended_addition(rec_input, sumC, sumN), 1)
                advice = f"The carbon-nitrogen ratio of this mixture is too low. Recommended addition: roughly {rec_input_amount} of brown material. "  # noqa:E501
            # the ratio is ready to submit
            else:
                advice = "The carbon-nitrogen ratio is within the recommended range. "

            tempEntries = TemperatureEntry.objects.all().order_by('-entryTime').values()
            tempMin = min(tempEntries[0].get('probe2'), tempEntries[0].get('probe3'))
            tempMax = max(tempEntries[0].get('probe2'), tempEntries[0].get('probe3'))

            if tempMax > 65:
                advice += "The temperature of the composter is above 65 at probe 2 or 3: bacterial digestion process may be destroyed. " \
                          "\nPlease add more brown material than normally recommended"  # noqa:E501
            if tempMin < 55:
                advice += "The temperature of the composter is below 55 at probe 2 or 3: more heat is needed to cook out pathogens" \
                          "\nPlease add more green material than normally recommended"  # noqa:E501
            context['advice'] = advice

        # form is submitted, process as normal
        elif entry_form.is_valid() and input_formset.is_valid():
            entry = entry_form.save(commit=False)
            entry.user = user
            entry.save()
            for inputs in input_formset:
                input = inputs.save(commit=False)
                input.inputEntry = entry
                input.save()
            return redirect(reverse('composter:composter'))
        # otherwise, show errors
        else:
            print(entry_form.errors)
            for inputs in input_formset:
                print(inputs.errors)

        context['input_formset'] = input_formset
        context['entry_form'] = entry_form
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
    if request.user.is_authenticated:
        restaurant_notifs = RestaurantRequest.objects.all()
        return render(request, 'composter/restaurant_notifs.html', {'restaurant_notifs': restaurant_notifs})
    else:
        if request.method == "POST":
            restaurant_form = RestaurantForm(request.POST)
            if restaurant_form.is_valid():
                restaurant_req = restaurant_form.save(commit=False)
                restaurant_req.dateRequested = timezone.now()
                restaurant_req.save()
                return redirect(reverse('composter:index'))
            else:
                print(restaurant_form.errors)

        else:
            restaurant_form = RestaurantForm()
        return render(request, 'composter/restaurant_form.html', {'restaurant_form': restaurant_form})


@login_required(login_url='/composter/')
def collect_request(request, request_id):
    req = RestaurantRequest.objects.get(requestID=request_id)
    req.collected = True
    req.save()
    return redirect('composter:restaurant_form')


# admin only views
@login_required(login_url='/composter/')
def simple_admin(request):
    user = User.objects.get(username=request.user.username)
    context = {'user_form': UserForm(), 'input_type_form': InputTypeForm(),
               'change_password_form': ChangePasswordForm(), 'energy_form': EnergyForm()}
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
        elif 'add_meter_reading' in request.POST:
            energy_form = EnergyForm(request.POST)
            if energy_form.is_valid():
                energy_form.save()
                context['success_message'] = "Meter readings taken."
            else:
                context['energy_form'] = energy_form

    return render(request, 'composter/simple_admin.html', context)
