import uuid
from django.db import models
from django.db.models.base import Model
from django.urls import reverse

# Create your models here.

# Confusing since not able to understand, if the class represents a table or a database.
class Genre(models.Model):
    """Model representing a book genre"""
    name = models.CharField(max_length=200,help_text="Add Book Genre")

    def __str__(self):
        return self.name

class Book(models.Model):
    """ This model represents the fields of the table"""
    title = models.CharField(max_length=200)

    # the reason why we are not using a integer because the underlying database may not be capable of holding a number which is of 13 digits.
    isbn = models.CharField('ISBN',max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    # figuring out the reason why author is being used as a foriegn key
    author = models.ForeignKey('Author',on_delete=models.SET_NULL,null=True)

    genre = models.ManyToManyField(Genre,help_text="Select the Genre of the book")

    summary = models.TextField(max_length=1000,help_text="Enter a brief summary of the book",)


    def __str__(self):
        return str(self.title)
    
    #
    def get_absolute_url(self):
        return reverse("book-detail", args=[str(self.id)])
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,help_text='Unique ID for this Book for whole library')

    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True,blank=True)

    LOAN_STATUS = (
        ('m','Maintenance'),
        ('o','On Loan'),
        ('a','Available'),
        ('r','Reserved')
    )

    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m',help_text='Book Avalibility')

    class Meta:
        ordering = ['due_back']

    # a little confusing but will see.

    def __str__(self):
        return f'{self.id},{self.book.title}'

class Author(models.Model):
    # field names of the Author table
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True,blank=True)
    date_of_death = models.DateField('Died',null=True,blank=True)

    class Meta:
        ordering = ['last_name','first_name']

    def get_absolute_url(self):
        return reverse("author-detail", args=[str(self.id)])
    
    def __str__(self):
        return f'{self.first_name} ,{self.last_name}'


    