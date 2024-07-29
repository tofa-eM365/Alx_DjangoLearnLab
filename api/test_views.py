from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Author, Book
from django.contrib.auth.models import User


class BookAPITests(APITestCase):
    def setUp(self):
        # Create a test user and authenticate
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Create an author
        self.author = Author.objects.create(name='J.K. Rowling')

        # Create a book
        self.book = Book.objects.create(
            title="Harry Potter and the Philosopher's Stone", publication_year=1997, author=self.author)

    def test_create_book(self):
        url = reverse('book-list')
        data = {'title': 'New Book', 'publication_year': 2023,
                'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(id=2).title, 'New Book')

    def test_retrieve_book_list(self):
        url = reverse('book-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_book_detail(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book.title)

    def test_update_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        data = {'title': 'Updated Book',
                'publication_year': 1997, 'author': self.author.id}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Updated Book')

    def test_delete_book(self):
        url = reverse('book-detail', kwargs={'pk': self.book.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 0)

    def test_unauthenticated_create_book(self):
        self.client.logout()
        url = reverse('book-list')
        data = {'title': 'New Book', 'publication_year': 2023,
                'author': self.author.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
