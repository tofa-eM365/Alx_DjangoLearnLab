from django.db import models
"""
The Author model represents an author with a name.
An author can have multiple books associated with them.
"""


class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    The Book model represents a book with a title, publication year, and an author.
    Each book is linked to a single author.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self):
        return self.title
