from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from app.models import Item
from django.contrib.auth import get_user_model
from decimal import Decimal

User = get_user_model()

class ItemAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = self._get_jwt_token()

        # Create an item to test against
        self.item = Item.objects.create(name="Test Item", description="Item Description", quantity=10, price=Decimal('9.99'))

    def _get_jwt_token(self):
        # Helper function to obtain JWT token
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'testuser',
            'password': 'testpass'
        })
        return response.data['access']

    def test_item_list(self):
        # Test GET /api/items/
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('item-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Check if the item is returned

    def test_create_item(self):
        # Test POST /api/items/
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        data = {
            "name": "New Item",
            "description": "Description of the new item",
            "quantity": 20,
            "price": Decimal('15.99')  # Use Decimal for the price
        }
        response = self.client.post(reverse('item-list'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)  # Check if the item count increased

    def test_retrieve_item(self):
        # Test GET /api/items/<id>/
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.get(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_update_item(self):
        # Test PUT /api/items/<id>/
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        updated_item_data = {
            "name": "Updated Item",
            "description": "Updated Description",
            "quantity": 30,
            "price": Decimal('19.99')  # Use Decimal for the price
        }
        response = self.client.put(reverse('item-detail', args=[self.item.id]), updated_item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()  # Refresh the item from the database
        self.assertEqual(self.item.name, "Updated Item")  # Check if the name was updated
        self.assertEqual(self.item.quantity, 30)  # Check if the quantity was updated
        self.assertEqual(self.item.price, Decimal('19.99'))  # Check if the price was updated

    def test_delete_item(self):
        # Test DELETE /api/items/<id>/
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
        response = self.client.delete(reverse('item-detail', args=[self.item.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Item.objects.count(), 0)  # Check if the item was deleted
