from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    # Validations for creating a new User
    def user_validation(self, postData):
        errors = {}
        # Filter index for name format
        gex = re.compile(r'^[a-zA-Z]+$')
        # Filter index for Email format
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        # Checking for numerical characters(first name)
        if not gex.match(postData['fname']):
            errors['fnumname'] = "Your First Name should not have numerical or specail characters!"
        # Checking length of characters(first name)
        if len(postData['fname']) < 2:
            errors['fname'] = "Your First Name should be at least 2 characters!"
        # Checking for numerical characters(last name)
        if not gex.match(postData['lname']):
            errors['lnumname'] = "Your Last Name should not have numerical or specail characters!"
        # Checking length of characters(last name)
        if len(postData['lname']) < 2:
            errors['lname'] = "Your Last Name should be at least 2 characters!"
        # Checking format of email and characters
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Your email format was incorrect!"
        if User.objects.filter(email=postData['email']):
            errors['used_email'] = "This email is already associated with another User!"
        if len(postData['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters!"
        if not postData['password'] == postData['conpw']:
            errors['conpw'] = "Your passwords don't match!"
        return errors

    # Validations for User Login
    def login_validation(self, postData):
        errors = {}
        # The User being validated
        user = User.objects.filter(email=postData['email'])
        # Checking if email exist
        if len(user) == 0:
            errors['email'] = "That user does not exist, Please try again!"
        if len(user) == 1:
            hashkey = bcrypt.checkpw(postData['password'].encode(), user[0].password.encode())
            # Checking if password is correct
            if hashkey == False:
                errors['password'] = "The password you entered was invalid, Please try again!"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(max_length=60)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
    # user_profile