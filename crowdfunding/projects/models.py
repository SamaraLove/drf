from django.db import models
from django.contrib.auth import get_user_model
from django.utils.timezone import now
from datetime import datetime, timedelta    


class Category(models.Model):
    category = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.category

def get_deadline():
    return datetime.today() + timedelta(days=20)

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal = models.IntegerField()
    image = models.URLField()
    is_open = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add=True,editable=False)
    last_update_at = models.DateTimeField(auto_now=True,blank=True)
    deadline = models.DateField(default=get_deadline)
    company = models.TextField(default = "")
    
    # owner = models.CharField(max_length=200)
    owner = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='owner_projects'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='project_categories'
    )
    # CATEGORY_CHOICES = (
    # ('Suspension', 'Suspension'),
    # ('Driveline', 'Driveline'),
    # ('Body', 'Body'),
    # ('Acessories', 'Acessories'),
    # ('Race', 'Race'),
    # # ('No Category Assigned', 'No Category Assigned'),
    # )
    # category = models.CharField(max_length=60, blank=True, default='No Category Assigned',choices=CATEGORY_CHOICES,verbose_name="category")
    # VehicleType_CHOICES = (
    # ('4WD', '4WD'),
    # ('Custom', 'Custom'),
    # ('Toyota', 'Toyota'),
    # ('Sprint', 'Sprint'),
    # # ('No Category Assigned', 'No Category Assigned'),
    # )
    # vehicle_category = models.CharField(max_length=60, blank=True, default='No Category Assigned',choices=VehicleType_CHOICES,verbose_name="vehicle_category")




class Pledge(models.Model):
    amount = models.IntegerField()
    comment = models.CharField(max_length=200)
    anonymous = models.BooleanField()
    project = models.ForeignKey(
        'Project',
        on_delete=models.CASCADE,
        related_name='pledges'
    )
    # supporter = models.CharField(max_length=200)
    supporter = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='supporter_pledges'
    )