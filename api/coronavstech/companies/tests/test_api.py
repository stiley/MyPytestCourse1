import json
from typing import List
from unittest import TestCase

import pytest
from django.test import Client
from django.urls import reverse

from api.coronavstech.companies.models import Company

companies_url = reverse("companies-list")
pytestmark = (
    pytest.mark.django_db
)  # this replaces @pytest.mark.django_db on each test method


def test_zero_companies_should_return_empty_list(client) -> None:
    resp = client.get(companies_url)
    assert resp.status_code == 200
    assert json.loads(resp.content) == []


def test_one_company_exists_should_return(client) -> None:
    test_company = Company.objects.create(name="Amazonia")
    resp = client.get(companies_url)
    resp_content = json.loads(resp.content)[0]
    assert resp.status_code == 200
    assert resp_content.get("name") == "Amazonia"
    assert resp_content.get("status") == "Hiring"
    assert resp_content.get("notes") == ""
    assert resp_content.get("application_link") == ""


# ---  POST  Requests


def test_create_company_without_args_should_Fail(client) -> None:
    response = client.post(path=companies_url)
    assert response.status_code == 400
    assert json.loads(response.content) == {"name": ["This field is required."]}


def test_create_duplicate_should_fail(client) -> None:
    test_company = Company.objects.create(name="2263020 Ontario INC.")
    resp = client.post(path=companies_url, data={"name": "2263020 Ontario INC."})
    resp_content = json.loads(resp.content)
    assert resp.status_code == 400
    assert "company with this name already exists." in str(resp_content)


def test_create_should_pass(client) -> None:
    resp = client.post(path=companies_url, data={"name": "Test Company Name"})
    resp_content = json.loads(resp.content)
    assert resp.status_code == 201
    assert resp_content.get("name") == "Test Company Name"
    assert resp_content.get("status") == "Hiring"
    assert resp_content.get("notes") == ""
    assert resp_content.get("application_link") == ""


def test_create_status_layoff_should_pass(client) -> None:
    resp = client.post(
        path=companies_url,
        data={"name": "Another Test Company", "status": "Layoffs"},
    )
    resp_content = json.loads(resp.content)
    assert resp.status_code == 201
    assert resp_content.get("name") == "Another Test Company"
    assert resp_content.get("status") == "Layoffs"


def test_create_invalid_status_should_fail(client) -> None:
    resp = client.post(
        path=companies_url,
        data={"name": "Another Test Company", "status": "wrongStatus"},
    )
    resp_content = json.loads(resp.content)
    assert resp.status_code == 400
    assert "is not a valid choice." in str(resp_content)


@pytest.mark.xfail
def test_flaky_example() -> None:
    assert 1 == 2


@pytest.mark.skip
def test_should_skip_this_test() -> None:
    assert 1 == 2
