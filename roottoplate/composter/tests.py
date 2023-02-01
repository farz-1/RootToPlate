import os
import warnings
from django.test import SimpleTestCase, TestCase
from django.urls import reverse
from composter.models import InputType, Input, InputEntry, \
    TemperatureEntry, RestaurantRequest, Output


class SimpleAnonymousComposterURLTesting(SimpleTestCase):
    """
    Do the URLs work as intended for an anonymous user?
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

#  TESTS BELOW HERE GONNA GET CHANGED PROBS


class ComposterDatabaseConfigurationTests(TestCase):
    """
    Is the database configured correctly?
    """

    def setUp(self):
        pass

    def is_database_in_gitignore(self):
        """
        Checks if database is in gitignore
        """
        git_base_dir = os.popen('git rev-parse --show-toplevel').read().strip()

        if git_base_dir.startswith('fatal'):
            warnings.warn("No github repository used")
        else:
            gitignore_path = os.path.join(git_base_dir, '.gitignore')

            if os.path.exists(gitignore_path):
                self.assertTrue(self.is_database_in_gitignore(gitignore_path),
                                "Your .gitignore file does not "
                                "include 'db.sqlite3'")
            else:
                warnings.warn("No .gitignore file")


class ComposterPopulationScriptTesting(TestCase):
    """
    Tests whether the population script works as expected
    """

    def setUp(self):
        try:
            import population_script
        except ImportError:
            raise ImportError("Population script could not be imported.")

        if 'populate' not in dir(population_script):
            raise NameError("population_script.py does not "
                            "contain the populate() function.")

        population_script.populate()

    def test_temperature_entries(self):
        """
        There should be 4 temperature entries created.
        """
        temperature_entries = TemperatureEntry.objects.filter()
        count = len(temperature_entries)
        entry_strs = map(str, temperature_entries)

        self.assertEqual(count, 4,
                         f'Expected 4 temperature entries to be created '
                         f'from the population script but found {count}')
        self.assertTrue('34264' in entry_strs, "Temperature entry with id "
                                               "34264 was expected but not"
                                               " present in database.")
