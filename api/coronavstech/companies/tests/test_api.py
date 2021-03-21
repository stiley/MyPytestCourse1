import json
from typing import List
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company

pytestmark = pytest.mark.django_db



@pytest.mark.django_db
class TestGetCompanies(TestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        client = Client()
        # companies_url = "http://127.0.0.1:8000/companies/1"
        companies_url = reverse('companies-list')
        resp = client.get(companies_url)
        self.assertEqual(resp.status_code, 200)
        # print(resp.status_code)
        # print((resp))
        self.assertEqual(json.loads(resp.content), [])

    def test_one_company_exists_should_return(self) -> None:
        client = Client()
        amazon = Company.objects.create(name="Amazonia")
        companies_url = reverse('companies-list')
        resp = client.get(companies_url)
        resp_content = json.loads(resp.content)[0]
        self.assertEqual(resp.status_code,200)
        self.assertEqual(resp_content.get("name"), "Amazonia")
        self.assertEqual(resp_content.get("status"), "Hiring")
        self.assertEqual(resp_content.get("notes"), "")
        self.assertEqual(resp_content.get("application_link"), "")
