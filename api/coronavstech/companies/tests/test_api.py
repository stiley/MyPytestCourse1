import json
from typing import List
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company

pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class BaseCompanyApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.companies_url = reverse("companies-list")

    def tearDown(self) -> None:
        pass


class TestGetCompanies(BaseCompanyApiTestCase):
    def test_zero_companies_should_return_empty_list(self) -> None:
        resp = self.client.get(self.companies_url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(json.loads(resp.content), [])

    def test_one_company_exists_should_return(self) -> None:
        test_company = Company.objects.create(name="Amazonia")
        resp = self.client.get(self.companies_url)
        resp_content = json.loads(resp.content)[0]
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp_content.get("name"), "Amazonia")
        self.assertEqual(resp_content.get("status"), "Hiring")
        self.assertEqual(resp_content.get("notes"), "")
        self.assertEqual(resp_content.get("application_link"), "")


class TestPostOperationToCreateNewCompany(BaseCompanyApiTestCase):
    def test_create_company_without_args_should_Fail(self) -> None:
        response = self.client.post(path=self.companies_url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content), {"name": ["This field is required."]}
        )

    def test_create_duplicate_should_fail(self) -> None:
        test_company = Company.objects.create(name="2263020 Ontario INC.")
        resp = self.client.post(
            path=self.companies_url, data={"name": "2263020 Ontario INC."}
        )
        resp_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp_content, {"name": ["company with this name already exists."]}
        )

    def test_create_should_pass(self) -> None:
        resp = self.client.post(
            path=self.companies_url, data={"name": "Test Company Name"}
        )
        resp_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_content.get("name"), "Test Company Name")
        self.assertEqual(resp_content.get("status"), "Hiring")
        self.assertEqual(resp_content.get("notes"), "")
        self.assertEqual(resp_content.get("application_link"), "")

    def test_create_status_layoff_should_pass(self) -> None:
        resp = self.client.post(
            path=self.companies_url,
            data={"name": "Another Test Company", "status": "Layoffs"},
        )
        resp_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp_content.get("name"), "Another Test Company")
        self.assertEqual(resp_content.get("status"), "Layoffs")

    def test_create_invalid_status_should_fail(self) -> None:
        resp = self.client.post(
            path=self.companies_url,
            data={"name": "Another Test Company", "status": "wrongStatus"},
        )
        resp_content = json.loads(resp.content)
        self.assertEqual(resp.status_code, 400)
        self.assertIn("is not a valid choice.", str(resp_content))

    @pytest.mark.xfail
    def test_flaky_example(self) -> None:
        self.assertEqual(1, 2)

    @pytest.mark.skip
    def test_should_skip_this_test(self) -> None:
        self.assertEqual(1, 2)
