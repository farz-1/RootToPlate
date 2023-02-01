from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from django.contrib.auth.models import User
import os
import warnings


class SimpleAnonymousComposterURLTesting(TestCase):
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

    def test_add_user_page_redirects_user(self):
        response = self.client.get('/composter/add-user/')
        self.assertEqual(response.status_code, 302)

    def test_input_type_page_redirects_user(self):
        response = self.client.get('/composter/add-input-type/')
        self.assertEqual(response.status_code, 302)

    def test_change_password_page_redirects_user(self):
        response = self.client.get('/composter/change-password/')
        self.assertEqual(response.status_code, 302)


class LoggedInUserURLTesting(TestCase):
    """
    URL testing for logged in users
    """
    def setUp(self):
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

    def test_add_user_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/add-user/')
        self.assertEqual(response.status_code, 200)

    def test_add_user_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:add_user'))
        self.assertEqual(response.status_code, 200)

    def test_add_user_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:add_user'))
        self.assertTemplateUsed(response, 'composter/admin_add_user.html')

    def test_add_user_redirects_non_staff(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:add_user'))
        self.assertEqual(response.status_code, 302)

    def test_add_type_page_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/add-input-type/')
        self.assertEqual(response.status_code, 200)

    def test_add_type_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:add_input_type'))
        self.assertEqual(response.status_code, 200)

    def test_add_type_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:add_input_type'))
        self.assertTemplateUsed(response, 'composter/admin_add_input_type.html')

    def test_add_type_redirects_non_staff(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:add_input_type'))
        self.assertEqual(response.status_code, 302)

    def test_change_password_at_correct_location(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get('/composter/change-password/')
        self.assertEqual(response.status_code, 200)

    def test_change_password_page_available_by_name(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:change_password'))
        self.assertEqual(response.status_code, 200)

    def test_change_password_template_name_correct(self):
        self.client.login(username='kw01', password='grass99')
        response = self.client.get(reverse('composter:change_password'))
        self.assertTemplateUsed(response, 'composter/admin_change_password.html')

    def test_change_password_redirects_non_staff(self):
        self.client.login(username='ab88', password='45dirt')
        response = self.client.get(reverse('composter:change_password'))
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
