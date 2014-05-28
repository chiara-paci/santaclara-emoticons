from django.db import models

import santaclara_emoticons.settings as settings

# Create your models here.

class EmoticonsCollection(models.Model):
    name = models.CharField(max_length=1024)
    author = models.CharField(max_length=1024,blank=True)
    url = models.URLField(max_length=1024)

    def __unicode__(self): return unicode(self.name)

class EmoticonsSet(models.Model):
    class Meta:
        ordering = [ 'name' ]

    name = models.CharField(max_length=1024)
    colspan = models.IntegerField()

    def __unicode__(self):
        return "%s (%d)" % (unicode(self.name),self.numerosity())

    def numerosity(self):
        return self.emoticon_set.all_enabled().count()

class EmoticonManager(models.Manager):
    def all_enabled(self):
        return(self.all().filter(enabled=True))

class Emoticon(models.Model):
    class Meta:
        ordering = [ 'set','label' ]
    label = models.SlugField(unique=True)
    name  = models.CharField(max_length=512)
    image = models.CharField(max_length=512)
    collection = models.ForeignKey(EmoticonsCollection)
    enabled = models.BooleanField(default=True)
    set = models.ForeignKey(EmoticonsSet)
    objects = EmoticonManager()

    def get_absolute_url(self):
        return settings.SANTACLARA_EMOTICONS_CONTEXT+"/"+unicode(self.image)

    def get_image(self):
        return u'<img src="'+self.get_absolute_url()+u'"/>'
    get_image.allow_tags=True

    def __unicode__(self): return unicode(self.name)
