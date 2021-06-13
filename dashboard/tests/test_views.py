# -*- coding: utf-8 -*-
from datetime import datetime

# Fixture package

# Test package & Utils
from django.test import TestCase
import pytest

pytestmark = pytest.mark.django_db

# models
from django.contrib.auth.models import User


from django.db import models

from django.urls import reverse


@pytest.mark.django_db
def test_view(client):
    url = reverse("get_operators_currently_online")
    response = client.get(url)
    assert response.status_code == 200
