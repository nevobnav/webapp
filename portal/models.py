from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from datetime import date,time

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length = 100, blank = True)
    def __str__(self):
        return str(self.customer_name)

    def get_all_parent_plots(self):
        user = self.user
        if user.is_staff:
            all_parent_plots = Parent_Plot.objects.all().reverse().order_by('-name')
        else:
            all_parent_plots = Parent_Plot.objects.filter(customer_id=self.pk)
        return all_parent_plots

class Parent_Plot(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.customer) + ' - ' + self.name + ' parent'

    def get_plot(self):
        my_plot = Plot.objects.filter(parent_plot_id=self.pk).first()
        return my_plot

class Plot(models.Model):
    parent_plot = models.ForeignKey(Parent_Plot, on_delete=models.SET_NULL, null=True)
    plot_shape = models.PolygonField(null=True, blank=True, geography=True)
    starting_point = models.PointField(null=True, blank=True, geography=True)

    crop_choices = (
    ('BROCCOLI', 'Broccoli'),
    ('BLOEMKOOL', 'Bloemkool'),
    ('TULP', 'Tulpen'),
    ('LELY', 'Lelies'),
    ('CICHOREI', 'Cichorei'),
    ('AARDAPPEL', 'Aardappelen'),
    ('SPRUIT', 'Spruiten'),
    ('SLA', 'Sla')
    )
    crop_type = models.CharField(
        max_length=100,
        choices=crop_choices,
        default='None'
    )

    active = models.BooleanField(default=True)

    startdate= models.DateField(default=date.today())


    def __str__(self):
        myname = str(self.parent_plot.customer.customer_name) + ' - ' + self.parent_plot.name
        return myname

    def get_absolute_url(self):
        return reverse('portal-map',kwargs={'id': self.id})

    @property
    def area(self):
        area = (1/10000) * self.plot_shape.transform(28992,clone=True).area
        return area

    def save(self, *args, **kwargs):
        if not self.starting_point:
            self.starting_point = self.plot_shape.centroid
        super().save(*args, **kwargs)


class Scan(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())
    time = models.TimeField(default= time(2,0))
    zoomlevel = models.PositiveSmallIntegerField(default = 23)
    flight_altitude = models.PositiveSmallIntegerField(default = 35)

    def __str__(self):
        return (self.date.strftime('%Y-%m-%d') + ' ' + self.time.strftime('%H:%M') + ' - ' + str(self.plot))

class Logbook(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)
