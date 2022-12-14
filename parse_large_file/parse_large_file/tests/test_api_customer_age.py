import os
from unittest import TestCase

from django.conf import settings

from parse_large_file.utils import import_customers_from_file
from rest_framework.test import APIClient


class CustomerAgeTestCase(TestCase):
    def setUp(self) -> None:
        assets_path = os.path.join(settings.PROJECT_ROOT, 'parse_large_file', 'tests', 'assets')
        csv_file_path = os.path.join(assets_path, 'customer_import.csv')
        import_customers_from_file(csv_file_path)

    def test_age_group(self):
        client = APIClient()
        response = client.get('/customers-age/')
        resp_json = response.json()
        self.assertEqual(resp_json['count'], 3)

        result = {item['age']: item['total'] for item in response.json()['results']}
        expected_result = {15: 2, 28: 1, 43: 1}
        self.assertEqual(result, expected_result)
