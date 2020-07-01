import pytest
import uuid
from django.urls import reverse_lazy

@pytest.fixture
def api_client():
   from rest_framework.test import APIClient
   return APIClient()
@pytest.fixture
def test_password():
   return 'strong-test-pass'
@pytest.fixture
def create_user(db, django_user_model, test_password):
   def make_user(**kwargs):
       kwargs['password'] = test_password
       if 'username' not in kwargs:
           kwargs['username'] = str(uuid.uuid4())
       return django_user_model.objects.create_user(**kwargs)
   return make_user
@pytest.fixture
def api_client_with_credentials(db,create_user,api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
@pytest.mark.django_db
def test_items_list(api_client_with_credentials):
    url = reverse_lazy('items_list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200



@pytest.mark.django_db
def test_orders_list(api_client_with_credentials):
    url = reverse_lazy('cart_list')
    response = api_client_with_credentials.get(url)
    assert response.status_code == 200