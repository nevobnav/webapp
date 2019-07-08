from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django.contrib.postgres.fields import JSONField
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

    def get_all_plots(self):
        parent_plots = self.get_all_parent_plots()
        plots = [x.plot_set.filter(active=True).first() for x in parent_plots]
        return plots

    def get_all_unseen_parent_plots(self):
        plots = self.get_all_plots()
        plot_ids = [x.id for x in plots]
        relevant_scans = Scan.objects.filter(plot_id__in=plot_ids).filter(seen_by_user=False).filter(live=True)
        unseen_parent_plots = []
        for scan in relevant_scans:
            unseen_parent_plots.append(scan.plot.parent_plot.id)
        return unseen_parent_plots



class Parent_Plot(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.customer) + ' - ' + self.name + ' parent'

    def get_plot(self):
        my_plot = Plot.objects.filter(parent_plot_id=self.pk).filter(active=True).first()
        return my_plot




class Plot(models.Model):
    parent_plot = models.ForeignKey(Parent_Plot, on_delete=models.SET_NULL, null=True)
    shape = models.PolygonField(null=True, blank=True, geography=True)
    starting_point = models.PointField(null=True, blank=True, geography=True)

    crop_choices = (
    ('BROCCOLI', 'Broccoli'),
    ('BLOEMKOOL', 'Bloemkool'),
    ('TULP', 'Tulpen'),
    ('LELY', 'Lelies'),
    ('HYACINTH', 'Hyacinth'),
    ('CICHOREI', 'Cichorei'),
    ('AARDAPPEL', 'Aardappelen'),
    ('SPRUIT', 'Spruiten'),
    ('SLA', 'Sla'),
    ('PEEN', 'Peen'),
    ('UI', 'Ui'),
    )
    crop = models.CharField(
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
        area = (1/10000) * self.shape.transform(28992,clone=True).area
        return area

    def save(self, *args, **kwargs):
        if not self.starting_point:
            self.starting_point = self.shape.centroid
        super().save(*args, **kwargs)




class Scan(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())
    time = models.TimeField(default= time(2,0))
    no_imgs = models.PositiveIntegerField(null=True, blank=True)
    zoomlevel = models.PositiveSmallIntegerField(default = 23)
    flight_altitude = models.PositiveSmallIntegerField(default = 35)
    sensor = models.CharField(default = 'unknown', max_length = 100)
    quality_choices = (
    ('LOW', 'Low'),
    ('MED', 'Medium'),
    ('HIGH', 'High'),
    )
    quality = models.CharField(
        max_length=10,
        choices=quality_choices,
        default = 'MED'
    )
    upload = models.DateTimeField(null=True, blank=True)
    preprocess = models.DateTimeField(null=True, blank=True)
    ortho = models.DateTimeField(null=True, blank=True)
    tiles = models.DateTimeField(null=True, blank=True)
    live = models.BooleanField(default=True)
    seen_by_user = models.BooleanField(default=False)


    def __str__(self):
        return (self.date.strftime('%Y-%m-%d') + ' ' + self.time.strftime('%H:%M') + ' - ' + str(self.plot))

class MapNote(models.Model):
    time = models.DateTimeField(auto_now_add=True)
    name = models.CharField(default = 'unkown', max_length = 100)
    note = models.TextField(null=True)
    lat = models.FloatField(null=True)
    lon = models.FloatField(null=True)
    scan = models.ForeignKey(Scan, on_delete=models.CASCADE)


class Logbook(models.Model):
    #Class used to log visits to the website. Can be viewed in dev.vanboven-drones.nl/phppgmyadmin
    time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

#Next up: DB entries made to keep track of measurements
class Breed(models.Model):
    name = models.CharField(max_length=100, null=True)
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
    crop = models.CharField(
        max_length=25,
        choices=crop_choices,
        null=True
    )
    season_choices = (
    ('SPRING','Voorjaar'),
    ('SUMMER','Zomer'),
    ('FALL','Herfst'),
    ('WINTER','Winter'),
    )
    season = models.CharField(max_length = 25, choices=season_choices,null=True)

class Planting(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.SET_NULL, null=True)
    breed = models.ForeignKey(Breed, on_delete=models.SET_NULL, null=True)
    shape = models.PolygonField(null=True, geography=True)
    no_of_plants = models.PositiveIntegerField(null=True)
    plant_date = models.DateField(null=True)
    harvest_date_projected = models.DateField(null=True)
    harvest_date_actual = models.DateField(null=True)
    harvest_date_modelled = models.DateField(null=True)

class Plant(models.Model):
    planting = models.ForeignKey(Planting, on_delete=models.SET_NULL, null=True)
    location = models.PointField(null=True, geography=True)

class Measurement(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.SET_NULL, null=True)
    scan = models.ForeignKey(Scan,on_delete=models.SET_NULL, null=True)
    diameter = models.FloatField(null=True)
    height = models.FloatField(null=True)
    shape = models.PolygonField(null=True, geography=True)

class Datalayer(models.Model):
    time = models.DateTimeField(null=True)
    data = JSONField(null=True)
    property_name = models.CharField(max_length = 256,null=True)
    layer_name = models.CharField(max_length = 256, null=True)
    legend_title = models.CharField(max_length = 256, null=True)
    legend_unit = models.CharField(max_length = 256, null=True)
    scan = models.ForeignKey(Scan, on_delete=models.SET_NULL, null=True)
