from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from django.db.models import Sum, F


# Create your models here.

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, lastname, age, gender, password=None, ):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, lastname=lastname, gender=gender, age=age)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, lastname, age, gender, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, lastname, age, gender, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    gender_options = (
        ('M', 'Male'),
        ('F', 'Female')
    )
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    age = models.PositiveIntegerField(default=0)
    gender = models.CharField(max_length=1, choices=gender_options, default='M')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'lastname', 'age', 'gender']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    def get_lastname(self):
        """Retrieve lastname of user"""
        return self.lastname

    def get_lastage(self):
        """Retrieve lastname of user"""
        return self.age

    def __str__(self):
        """Return string representation of user"""
        return self.email


class Category(models.Model):
    category_name = models.CharField(max_length=50, unique=True)
    description = models.TextField(max_length=255, blank=True)
    image = models.ImageField(upload_to="photos/categories", blank=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Product(models.Model):
    product_name = models.CharField(max_length=250, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    images = models.ImageField(upload_to='photos/products', blank=True)
    quantity = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class Invoice(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    @property
    def total(self):
        # sum = 0
        # for item in self.invoiceitem_set.all():
        #     sum += item.total
        # return sum
        return self.invoiceitem_set.all().aggregate(total=Sum(F('quantity') * F('price')))

    def __str__(self):
        return f'{self.client} / {self.date}'


Mosha = [
    ("a", "0-3 vjec"),
    ("b", "3-6 vjec"),
    ("c", ">6 vjec")
]

Gjinia = [
    ("M", "Boy"),
    ("F", "Girl"),
    ("U", "Unisex"),
]


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations_category = models.CharField(max_length=250, choices=Mosha)
    gender = models.CharField(max_length=1, choices=Gjinia)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.product


class InvoiceItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    quantity = models.FloatField(default=0)
    price = models.FloatField(default=0)

    # total = models.FloatField(default=0)

    @property
    def total(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product} - {self.invoice}'


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    subject = models.CharField(max_length=250, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
