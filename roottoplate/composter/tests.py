from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from composter.models import InputType, Input, InputEntry, TemperatureEntry, \
    RestaurantRequest, Output
import os
import io
import sys
from django.utils import timezone


class AnonymousURLTesting(TestCase):
    """
    Checks the URLS for anonymous users
    """
    def test_index_page_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, 'Index page at incorrect location.')

    def test_index_available_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200, 'Index not available by name.')

    def test_index_template_name_correct(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'composter/base.html', 'Index uses wrong template.')

    def test_about_page_at_correct_location(self):
        response = self.client.get('/composter/about/')
        self.assertEqual(response.status_code, 200, 'About page at incorrect location.')

    def test_about_page_available_by_name(self):
        response = self.client.get(reverse('composter:about'))
        self.assertEqual(response.status_code, 200, 'About page not available by name.')

    def test_about_template_name_correct(self):
        response = self.client.get(reverse('composter:about'))
        self.assertTemplateUsed(response, 'composter/about.html', 'About page uses wrong template.')

    def test_login_page_at_correct_location(self):
        response = self.client.get('/composter/login/')
        self.assertEqual(response.status_code, 200, 'Login page at incorrect location.')

    def test_login_page_available_by_name(self):
        response = self.client.get(reverse('composter:login'))
        self.assertEqual(response.status_code, 200, 'Login page not available by name.')

    def test_login_template_name_correct(self):
        response = self.client.get(reverse('composter:login'))
        self.assertTemplateUsed(response, 'composter/login.html', 'Login uses incorrect template.')

    def test_logout_redirects_user(self):
        response = self.client.get('/composter/logout/')
        self.assertEqual(response.status_code, 302, 'Logout page does not redirect user.')

    def test_composter_page_at_correct_location(self):
        response = self.client.get('/composter/composter/')
        self.assertEqual(response.status_code, 200, 'Composter page at incorrect location.')

    def test_composter_page_available_by_name(self):
        response = self.client.get(reverse('composter:composter'))
        self.assertEqual(response.status_code, 200, 'Composter page not available by name.')

    def test_composter_template_name_correct(self):
        response = self.client.get(reverse('composter:composter'))
        self.assertTemplateUsed(response, 'composter/composter.html', 'Composter page uses wrong template.')

    def test_input_entry_page_redirects_user(self):
        response = self.client.get('/composter/input-entry/')
        self.assertEqual(response.status_code, 302, 'Input entry page does not redirect anonymous users.')

    def test_temp_entry_page_redirects_user(self):
        response = self.client.get('/composter/temp-entry/')
        self.assertEqual(response.status_code, 302, 'Temperature entry page does not redirect anonymous users.')

    def test_output_entry_page_redirects_user(self):
        response = self.client.get('/composter/output-entry/')
        self.assertEqual(response.status_code, 302, 'Output entry page does not redirect anonymous users.')

    def test_simple_admin_page_redirects_user(self):
        response = self.client.get('/composter/simple-admin/')
        self.assertEqual(response.status_code, 302, 'Admin page does not redirect anonymous users.')


class LoggedInUserURLTesting(TestCase):
    """
    URL testing for logged in users
    """
    def setUp(self):
        create_non_admin()

    def test_index_page_at_correct_location(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200, 'Index at incorrect location.')

    def test_index_available_by_name(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200, 'Index not available by name.')

    def test_about_page_at_correct_location(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/about/')
        self.assertEqual(response.status_code, 200, 'About page at incorrect location.')

    def test_about_page_available_by_name(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:about'))
        self.assertEqual(response.status_code, 200, 'About page not available by name.')

    def test_login_page_redirects_logged_in_user(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/login/')
        self.assertEqual(response.status_code, 302, 'Login page does not redirect user.')

    def test_login_page_by_name_redirects_logged_in_user(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:login'))
        self.assertEqual(response.status_code, 302, 'Login page does not redirect user.')

    def test_composter_page_at_correct_location(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/composter/')
        self.assertEqual(response.status_code, 200, 'Composter page at incorrect location.')

    def test_composter_page_available_by_name(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:composter'))
        self.assertEqual(response.status_code, 200, 'Composter page not available by name.')

    def test_input_entry_page_at_correct_location(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/input-entry/')
        self.assertEqual(response.status_code, 200, 'Input entry page at incorrect location.')

    def test_input_entry_page_available_by_name(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:input_entry'))
        self.assertEqual(response.status_code, 200, 'Input entry page could not be accessed by name.')

    def test_input_entry_template_name_correct(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:input_entry'))
        self.assertTemplateUsed(response, 'composter/compost_form.html', 'Input entry page uses incorrect template.')

    def test_temp_entry_page_at_correct_location(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/temp-entry/')
        self.assertEqual(response.status_code, 200, 'Temperature entry at incorrect location.')

    def test_temp_entry_page_available_by_name(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:temp_entry'))
        self.assertEqual(response.status_code, 200, 'Temperature entry page could not be accessed by name.')

    def test_temp_entry_template_name_correct(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:temp_entry'))
        self.assertTemplateUsed(response, 'composter/temperature_form.html', 'Temperature entry '
                                                                             'uses incorrect template.')

    def test_output_entry_page_at_correct_location(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/output-entry/')
        self.assertEqual(response.status_code, 200, 'Output entry at incorrect location.')

    def test_output_entry_page_available_by_name(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:output_entry'))
        self.assertEqual(response.status_code, 200, 'Output could not be accessed by name.')

    def test_output_entry_template_name_correct(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:output_entry'))
        self.assertTemplateUsed(response, 'composter/compost_output_form.html', 'Output entry uses incorrect template.')

    def test_simple_admin_redirects_non_staff(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:simple_admin'))
        self.assertEqual(response.status_code, 302, 'Admin page does not redirect non-staff users.')

    def test_logout_working(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get('/composter/logout/')
        self.assertEqual(response.status_code, 302, 'Logout button did not redirect user')
        # should not redirect
        response = self.client.get('/composter/login/')
        self.assertEqual(response.status_code, 200, 'Logout button did not log out user')


class DatabaseConfigurationTests(TestCase):
    """
    Checks the database is correctly configured
    """
    def setUp(self):
        pass

    def test_databases_variable_exists(self):
        self.assertTrue(settings.DATABASES, 'Database variable does not exist.')
        self.assertTrue('default' in settings.DATABASES)


class PopulationScriptTests(TestCase):
    """
    Checks if the population script is correctly configured
    """
    def setUp(self):
        try:
            import population_script
        except ImportError:
            raise ImportError("Error importing population_script.py")

        if 'populate' not in dir(population_script):
            raise NameError("population_script.py does not contain the populate() method")

        text_trap = io.StringIO()
        sys.stdout = text_trap
        population_script.populate()
        sys.stdout = sys.__stdout__

    def test_input_types(self):
        """
        14 input types should be created
        """
        input_types = InputType.objects.filter()
        length = len(input_types)
        strs = map(str, input_types)

        self.assertEqual(length, 14, f'14 input types expected from population script, {len(input_types)} created.')
        self.assertTrue('Grass clippings' in strs, 'Population script did not create expected input type data.')

    def test_input_entries(self):
        """
        3 input entries should be created
        """
        input_entries = InputEntry.objects.filter()
        self.assertEqual(len(input_entries), 48, f'48 input entries expected from population script, '
                                                 f'{len(input_entries)} created.')

    def test_inputs(self):
        """
        117 inputs should be created
        """
        inputs = Input.objects.filter()
        self.assertEqual(len(inputs), 117, f'117 inputs expected from population script, {len(inputs)} created.')

    def test_temp_entries(self):
        """
        4 temperature entries should be created
        """
        temp_entries = TemperatureEntry.objects.filter()
        self.assertEqual(len(temp_entries), 45, f'45 temperature entries expected from population script, '
                                                f'{len(temp_entries)} created.')

    def test_users(self):
        """
        4 users should be created
        """
        users = User.objects.filter()
        strs = map(str, users)
        self.assertEqual(len(users), 4, f'4 users expected from population script, {len(users)} created.')
        self.assertTrue("kw01" in strs, 'Users incorrectly created from population script.')


class FormTests(TestCase):
    """
    Testing of login, input, temperature, output and restaurant forms.
    Ensures they create new entry in database.
    """
    def setUp(self):
        create_non_admin()

    def test_module_exists(self):
        project_path = os.getcwd()
        app_path = os.path.join(project_path, 'composter')
        forms_module_path = os.path.join(app_path, 'forms.py')
        self.assertTrue(os.path.exists(forms_module_path))

    def test_user_login_form(self):
        response = self.client.post(reverse('composter:login'), {'username': 'ab88', 'password': '45dirt'},
                                    follow=True)
        self.assertTrue(response.context['user'].is_active, 'Could not log in with user form.')

    def test_restaurant_request_form(self):
        expected = len(RestaurantRequest.objects.filter()) + 1
        self.client.post(reverse('composter:restaurant_form'),
                         {'name': 'test', 'address': 'test',
                          'deadlineDate': timezone.now() + (timezone.timedelta(weeks=1)),
                          'email': 'test@test.com', 'phoneNumber': '21234569812', 'numberOfBags': 2,
                          'notes': 'test'})
        restaurant = RestaurantRequest.objects.filter(name='test')
        self.assertEqual(len(restaurant), expected, 'Could not create restaurant request from form.')
        self.assertEqual(restaurant[0].email, 'test@test.com', 'Restaurant request incorrectly created from form.')

    def test_temp_entry_form(self):
        expected = len(TemperatureEntry.objects.filter()) + 1
        self.client.login(username='ab88', password='45dirt')  # non-admin
        self.client.post(reverse('composter:temp_entry'),
                         {'entryTime': timezone.now(), 'probe1': '54', 'probe2': '53', 'probe3': '51',
                          'probe4': '51', 'notes': 'test'})
        self.assertEqual(expected, len(TemperatureEntry.objects.filter()), 'Temperature entry form could not create a'
                                                                           ' new temperature entry.')

    def test_input_form(self):
        expected_entries = 1
        expected_inputs = 1
        InputType.objects.get_or_create(name='test_type', moisturePercent=1, CNRatio=1, nitrogenPercent=1)
        type_pk = InputType.objects.get(pk='test_type').pk
        self.client.login(username='ab88', password='45dirt')
        self.client.post(reverse('composter:input_entry'),
                         {'entryTime': timezone.now(), 'form-TOTAL_FORMS': 1, 'form-INITIAL_FORMS': 0,
                          'form-0-inputType': type_pk, 'form-0-inputAmount': 1, 'notes': 'n'})
        self.assertEqual(expected_entries, len(InputEntry.objects.filter()), 'Input form could not create a new input.')
        self.assertEqual(expected_inputs, len(Input.objects.filter()), 'Input form could not create a new input '
                                                                       'entry.')

    def test_output_entry_form(self):
        expected = len(Output.objects.filter()) + 1
        self.client.login(username='ab88', password='45dirt')
        self.client.post(reverse('composter:output_entry'),
                         {'time': timezone.now(), 'amount': 3, 'notes': 't'})
        self.assertEqual(expected, len(Output.objects.filter()), 'Output form could not create a new output.')


class AdminTests(TestCase):
    """
    Tests admin functionality. Tests the admin forms and makes sure they create new entries in database.
    Tests the admin pages and their templates.
    """
    def setUp(self):
        create_admin()

    def test_add_user(self):
        expected = len(User.objects.filter()) + 1
        user_data = {'add_user': True, 'username': 'test', 'first_name': 'test', 'last_name': 'mctest',
                     'password1': 'composter82', 'password2': 'composter82', 'is_staff': False}
        self.client.login(username='kw01', password='grass99')
        self.client.post(reverse('composter:simple_admin'), user_data, follow=True)
        self.assertEqual(expected, len(User.objects.filter()), 'Could not add new user from admin form.')

    def test_add_input_type(self):
        expected = len(InputType.objects.filter()) + 1
        type_data = {'add_input_type': True, 'name': 'test', 'CNRatio': 2, 'nitrogenPercent': 2,
                     'moisturePercent': 2}
        self.client.login(username='kw01', password='grass99')
        self.client.post(reverse('composter:simple_admin'), type_data, follow=True)
        self.assertEqual(expected, len(InputType.objects.filter()), 'Could not create new input type with admin form.')

    def test_change_other_user_password(self):
        create_non_admin()
        self.client.login(username='kw01', password='grass99')
        password_data = {'change_password': True, 'username': 'ab88', 'password': '11compost99'}
        self.client.post(reverse('composter:simple_admin'), password_data, follow=True)
        self.assertTrue(self.client.login(username='ab88', password='11compost99'), 'Could not change user password '
                                                                                    'with admin form.')

    def test_change_own_password(self):
        self.client.login(username='kw01', password='grass99')
        password_data = {'change_password': True, 'username': 'kw01', 'password': '11compost99'}
        self.client.post(reverse('composter:simple_admin'), password_data, follow=True)
        self.assertTrue(self.client.login(username='kw01', password='11compost99'), 'Could not change own user '
                                                                                    'password with admin form.')

    def test_simple_admin_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/simple-admin/')
        self.assertEqual(response.status_code, 200, 'Admin page at incorrect location.')

    def test_simple_admin_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:simple_admin'))
        self.assertEqual(response.status_code, 200, 'Admin page could not be accessed by name.')

    def test_simple_admin_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:simple_admin'))
        self.assertTemplateUsed(response, 'composter/simple_admin.html', 'Admin page does not use correct template')


#  Creates a test admin user
def create_admin():
    user = User.objects.create_user(username='kw01', password='grass99')
    user.is_staff = True
    user.is_superuser = True
    user.save()


#  Creates a test non-admin user
def create_non_admin():
    user = User.objects.create_user(username='ab88', password='45dirt')
    user.is_staff = False
    user.is_superuser = False
    user.save()
