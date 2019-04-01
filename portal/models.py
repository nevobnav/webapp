from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models
from datetime import date

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customer_id = models.CharField(max_length = 100, blank = True)
    def __str__(self):
        return str(self.customer_id)
    def get_all_plots(self):
        all_plots = Plot.objects.filter(customer_id=self.pk).order_by('-startdate')
        return all_plots

class Plot(models.Model):
    name = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    number = models.IntegerField()
    shape = models.PolygonField(null=True, blank=True, geography=True)

    crop_choices = (
    ('AKKER', 'Akkerbouw'),
    ('BOL', 'Bollenteelt'),
    ('GROENTE', 'Groenteteelt')
    )
    crop = models.CharField(
        max_length=100,
        choices=crop_choices,
        default='None'
    )
    startdate= models.DateField(default=date.today())
    customer = models.ForeignKey(Customer,blank = True, on_delete=models.CASCADE)

    def __str__(self):
        myname = str(self.customer) + ' - ' + self.name
        return myname

    def get_absolute_url(self):
        return reverse('portal-map',kwargs={'id': self.id})

    @property
    def area(self):
        area = (1/10000) * self.shape.transform(28992,clone=True).area
        return area

class Scan(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE)
    date = models.DateField(default=date.today())

    def __str__(self):
        return (self.date.strftime('%Y-%m-%d') + ' - ' + str(self.plot))

class Logbook(models.Model):
    time = models.DateTimeField(auto_now_add=True, null=True,blank=True)
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)
