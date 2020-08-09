from django.db import models
from django.contrib.auth.models import User
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator


def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.jobcreator.id, filename)
# Create your models here.


class Userjob(models.Model):

    NEWORDER = 'neworder'
    RUNNING = 'running'
    QC = 'QC'
    SHIPPED = 'shipped'
    COMPLETED = 'completed'
    DOMORE = 'Do more'
    REDO = 'Redo'


    STATUS = [
    (NEWORDER, ('New Order')),
    (RUNNING, ('Running')),
    (QC, ('Quality Check')),
    (SHIPPED, ('Shipped to Customer')), 
    (COMPLETED, ('Order Completed')),
    (DOMORE, ('Do More')),
    (REDO, ('Redo')),
    ]


    idxml= models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=250)
    jobcreator = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    orderdate = models.DateTimeField(auto_now_add=True)
    deadlinedate = models.DateTimeField(help_text="Enter the date of the Deadline", validators=[MinValueValidator(limit_value=datetime.now)])
    completeddate = models.DateTimeField(null=True, blank=True)
    amountimages = models.IntegerField()
    important = models.BooleanField(default=False)
    newzip = models.FileField(upload_to=user_directory_path)
    examplezip = models.FileField(upload_to=user_directory_path, blank=True)
    status = models.CharField(max_length=9, choices=STATUS, default=NEWORDER)

    def __str__(self):

        return self.title + ' by ' + self.jobcreator.username + ' on ' + self.orderdate.__str__()
