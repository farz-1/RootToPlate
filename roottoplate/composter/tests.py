from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
from composter.models import InputType, Input, InputEntry, TemperatureEntry, \
    RestaurantRequest, Output
import os
import warnings
import io
import sys
import datetime


class AnonymousURLTesting(TestCase):
    """
    Checks the URLS for anonymous users
    """
    def test_index_page_at_correct_location(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_available_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_template_name_correct(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'composter/base.html')

    def test_about_page_at_correct_location(self):
        response = self.client.get('/composter/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_available_by_name(self):
        response = self.client.get(reverse('composter:about'))
        self.assertEqual(response.status_code, 200)

    def test_about_template_name_correct(self):
        response = self.client.get(reverse('composter:about'))
        self.assertTemplateUsed(response, 'composter/about.html')

    def test_login_page_at_correct_location(self):
        response = self.client.get('/composter/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_available_by_name(self):
        response = self.client.get(reverse('composter:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_template_name_correct(self):
        response = self.client.get(reverse('composter:login'))
        self.assertTemplateUsed(response, 'composter/login.html')

    def test_logout_redirects_user(self):
        response = self.client.get('/composter/logout/')
        self.assertEqual(response.status_code, 302)

    def test_composter_page_at_correct_location(self):
        response = self.client.get('/composter/composter/')
        self.assertEqual(response.status_code, 200)

    def test_composter_page_available_by_name(self):
        response = self.client.get(reverse('composter:composter'))
        self.assertEqual(response.status_code, 200)

    def test_composter_template_name_correct(self):
        response = self.client.get(reverse('composter:composter'))
        self.assertTemplateUsed(response, 'composter/composter.html')

    def test_input_entry_page_redirects_user(self):
        response = self.client.get('/composter/input-entry/')
        self.assertEqual(response.status_code, 302)

    def test_temp_entry_page_redirects_user(self):
        response = self.client.get('/composter/temp-entry/')
        self.assertEqual(response.status_code, 302)

    def test_output_entry_page_redirects_user(self):
        response = self.client.get('/composter/output-entry/')
        self.assertEqual(response.status_code, 302)

    def test_simple_admin_page_redirects_user(self):
        response = self.client.get('/composter/simple-admin/')
        self.assertEqual(response.status_code, 302)


class LoggedInUserURLTesting(TestCase):
    """
    URL testing for logged in users
    """
    def setUp(self):
        set_up_test_users()

    def test_index_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_about_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/about/')
        self.assertEqual(response.status_code, 200)

    def test_about_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:about'))
        self.assertEqual(response.status_code, 200)

    def test_login_page_redirects_logged_in_user(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/login/')
        self.assertEqual(response.status_code, 302)

    def test_login_page_by_name_redirects_logged_in_user(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:login'))
        self.assertEqual(response.status_code, 302)

    def test_composter_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/composter/')
        self.assertEqual(response.status_code, 200)

    def test_composter_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:composter'))
        self.assertEqual(response.status_code, 200)

    def test_input_entry_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/input-entry/')
        self.assertEqual(response.status_code, 200)

    def test_input_entry_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:input_entry'))
        self.assertEqual(response.status_code, 200)

    def test_input_entry_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:input_entry'))
        self.assertTemplateUsed(response, 'composter/compost_form.html')

    def test_temp_entry_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/temp-entry/')
        self.assertEqual(response.status_code, 200)

    def test_temp_entry_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:temp_entry'))
        self.assertEqual(response.status_code, 200)

    def test_temp_entry_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:temp_entry'))
        self.assertTemplateUsed(response, 'composter/temperature_form.html')

    def test_output_entry_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/output-entry/')
        self.assertEqual(response.status_code, 200)

    def test_output_entry_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:output_entry'))
        self.assertEqual(response.status_code, 200)

    def test_output_entry_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:output_entry'))
        self.assertTemplateUsed(response, 'composter/compost_output_form.html')

    def test_simple_admin_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/simple-admin/')
        self.assertEqual(response.status_code, 200)

    def test_simple_admin_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:simple_admin'))
        self.assertEqual(response.status_code, 200)

    def test_simple_admin_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:simple_admin'))
        self.assertTemplateUsed(response, 'composter/simple_admin.html')

    def test_simple_admin_redirects_non_staff(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:simple_admin'))
        self.assertEqual(response.status_code, 302)

    def test_logout_working(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/logout/')
        self.assertEqual(response.status_code, 302)
        # should not redirect
        response = self.client.get('/composter/login/')
        self.assertEqual(response.status_code, 200)


class DatabaseConfigurationTests(TestCase):
    """
    Checks the database is correctly configured
    """
    def setUp(self):
        pass

    def test_databases_variable_exists(self):
        self.assertTrue(settings.DATABASES)
        self.assertTrue('default' in settings.DATABASES)

    def test_gitignore_contains_database(self):
        """
        gitignore should contain the database
        """
        base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        if base_dir.startswith('fatal'):
            warnings.warn("No github repo used")
        else:
            gitignore = os.path.join(base_dir, '.gitignore')

            if os.path.exists(gitignore):
                f = open(gitignore, 'r')

                for line in f:
                    line = line.strip()

                    if line.startswith('db.sqlite3'):
                        success = True
            self.assertTrue(success)


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
        6 input types should be created
        """
        input_types = InputType.objects.filter()
        length = len(input_types)
        strs = map(str, input_types)

        self.assertEqual(length, 6)
        self.assertTrue('Weeds' in strs)

    def test_input_entries(self):
        """
        3 input entries should be created
        """
        input_entries = InputEntry.objects.filter()
        self.assertEqual(len(input_entries), 3)

    def test_inputs(self):
        """
        4 inputs should be created
        """
        inputs = Input.objects.filter()
        self.assertEqual(len(inputs), 4)
        # test_object = Input.objects.get_or_create('Input object (2)')
        # self.assertEqual(test_object.inputEntry, 10003)

    def test_temp_entries(self):
        """
        4 temperature entries should be created
        """
        temp_entries = TemperatureEntry.objects.filter()
        strs = map(str, temp_entries)
        self.assertEqual(len(temp_entries), 4)
        self.assertTrue(str(10002) in strs)

    def test_users(self):
        """
        4 users should be created
        """
        users = User.objects.filter()
        strs = map(str, users)
        self.assertEqual(len(users), 4)
        self.assertTrue("kw01" in strs)

    def test_restaurant_requests(self):
        """
        1 restaurant request should be created
        """
        requests = RestaurantRequest.objects.filter()
        strs = map(str, requests)
        self.assertEqual(len(requests), 1)
        self.assertTrue("20002" in strs)

    def test_outputs(self):
        """
        5 output entries should be created
        """
        outputs = Output.objects.filter()
        strs = map(str, outputs)
        self.assertEqual(len(outputs), 5)
        self.assertTrue("1009" in strs)

    #  Test that the relationships have been created.
    def test_input_has_user(self):
        input_entry = InputEntry.objects.get(entryID=10001)
        user = User.objects.get(username="ag23")
        self.assertEqual(input_entry.user, user)

    def test_temp_entry_has_user(self):
        input_entry = TemperatureEntry.objects.get(entryID=34264)
        user = User.objects.get(username="kw01")
        self.assertEqual(input_entry.user, user)

    def test_output_entry_has_user(self):
        input_entry = Output.objects.get(outputID=1002)
        user = User.objects.get(username="lb212")
        self.assertEqual(input_entry.user, user)


class FormTests(TestCase):
    def setUp(self):
        set_up_test_users()

    def test_module_exists(self):
        project_path = os.getcwd()
        app_path = os.path.join(project_path, 'composter')
        forms_module_path = os.path.join(app_path, 'forms.py')
        self.assertTrue(os.path.exists(forms_module_path))

    # def test_user_form(self):
    #     self.client.login(username='kw01', password='grass99')
    #     expected = len(User.objects.filter())
    #     form_data = {'username': 'jdoe1', 'first_name': 'jane', 'last_name': 'doe', 'password1': 'test',
    #                  'password2': 'test'}
    #     self.client.post(reverse('composter:add_user'), form_data)
    #     users = User.objects.filter()
    #     self.assertEqual(len(users), expected)
    #     self.client.logout()
    #     self.assertTrue(self.client.login(username='jdoe1', password='test'))

    def test_restaurant_request_form(self):
        expected = len(RestaurantRequest.objects.filter()) + 1
        self.client.post(reverse('composter:restaurant_form'),
                         {'name': 'test', 'address': 'test', 'dateRequested': datetime.datetime.now(),
                          'deadlineDate': datetime.datetime.now() + (datetime.timedelta(weeks=1)),
                          'email': 'test@test.com', 'phoneNumber': '21234569812', 'numberOfBags': 2,
                          'notes': 'test'})
        restaurant = RestaurantRequest.objects.filter(name='test')
        self.assertEqual(len(restaurant), expected)
        self.assertEqual(restaurant[0].email, 'test@test.com')

    def test_temp_entry_form(self):
        expected = len(TemperatureEntry.objects.filter()) + 1
        self.client.login(username='ag23', password='compost1')  # non-admin
        self.client.post(reverse('composter:temp_entry'),
                         {'entryTime': datetime.datetime.now(), 'probe1': '54', 'probe2': '53', 'probe3': '51',
                          'probe4': '51', 'notes': 'test'})
        self.assertEqual(expected, len(TemperatureEntry.objects.filter()))

    def test_input_form(self):
        expected_entries = 1
        expected_inputs = 1
        InputType.objects.get_or_create(name='test_type',
                                        woodChipRatio=1,
                                        CNRatio=1)
        self.client.login(username='ag23', password='compost1')
        self.client.post(reverse('composter:input_entry'),
                         {'entryTime': datetime.datetime.now(),
                          'inputType': 'test_type', 'inputAmount': 1, 'notes': 'n'})
        self.assertEqual(expected_inputs, len(Input.objects.filter()))
        self.assertEqual(expected_entries, len(InputEntry.objects.filter()))

    def test_output_entry_form(self):
        expected = len(Output.objects.filter()) + 1
        self.client.login(username='ag23', password='compost1')
        self.client.post(reverse('composter:output_entry'),
                         {'time': datetime.datetime.now(), 'amount': 3, 'notes': 't'})
        self.assertTrue(expected, len(Output.objects.filter()))


def set_up_test_users():
    user = User.objects.create_user(username='kw01',
                                    password='grass99')
    user.is_staff = True
    user.is_superuser = True
    user.save()
    user2 = User.objects.create_user(username='ab88',
                                     password='45dirt')
    user2.is_staff = False
    user2.is_superuser = False
    user2.save()
    user3 = User.objects.create_user(username='ag23',
                                     password='compost1')
    user3.is_staff = False
    user3.is_superuser = False
    user3.save()
