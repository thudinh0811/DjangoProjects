from django.db import models
from django.utils import timezone
import datetime
from django.contrib.auth.models import User


class Topic(models.Model):
    topic = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.topic

class Recipe(models.Model):
    recipe_name = models.CharField(max_length= 200)
    pub_date = models.DateTimeField('date published')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    #recipe_picture = models.ImageField(upload_to = '', default= '')

    def __str__(self):
        return self.recipe_name

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=30) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Ingredient(models.Model):
    #topic = models.ForeignKey(Topic, on_delete= models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete= models.CASCADE)
    ingredient_name = models.CharField(max_length=300)
    ingredient_amount = models.CharField(max_length= 60)

    def __str__(self):
        return self.ingredient_name

class Instruction(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete= models.CASCADE)
    instruction_step = models.CharField(max_length= 1000)

    def __str__(self):
        return self.instruction_step