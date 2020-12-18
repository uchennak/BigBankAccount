from django.db import models
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):

    def register_validator(self, postData):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        # add keys and values to errors dictionary for each invalid field

        username_check = self.filter(username=postData['username'])
        email_check = self.filter(email=postData['email'])
        
        if username_check:
            errors['username_check'] = "Username already in use"
        if email_check:
            errors['email_check'] = "Email already in use"
        
        if not EMAIL_REGEX.match(postData['email']):                
            errors['email'] = ("Invalid email address!")

        if len(postData['username']) < 3:
            errors["username"] = "username should be more than 2 characters"
        if len(postData['username']) > 16:
            errors["username"] = "username should be less than 17 characters"
            
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 9 characters"
        if postData['password'] != postData['confirm_password']:
            errors["confirm_password"] = "Passwords dont match"

     
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, form):
        pw = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(

            email = form['email'], 
            username = form['username'],
            password = pw,
            account_balance = 0,
            coins = 5,
            level = 1,
            investment_click_counter = 5,
            invested_balance = 0,
            coin_click_counter = 5

            
        )


class User(models.Model):
    
    email = models.CharField(max_length=100)
    username =models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    account_balance = models.IntegerField()
    coins = models.IntegerField()
    invested_balance = models.IntegerField()
    date_joined = models.DateTimeField(auto_now_add=True)
    investment_click_counter = models.IntegerField()
    coin_click_counter = models.IntegerField()
    level = models.IntegerField() 
    objects = UserManager()


class Account(models.Model):
    account_balance = models.IntegerField()
    coins = models.IntegerField()
    invested_balance = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)


    