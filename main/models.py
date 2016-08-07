from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth import models as auth_models
import django.dispatch


STAR_BADGE = 'star'
COLLECTOR_BADGE = 'collector'
PIONEER_BADGE = 'pioneer'


class User(auth_models.AbstractUser):
    def has_badge(self, name):
        """
        Check if user has some badge

        :param str name: the badge name to search
        :returns: None or the searched badge
        """
        return next((badge for badge in self.badge_set.all() if badge.name == name), None)

    def ensure_badge(self, name):
        """
        Ensure user has a given badge

        :param str name: the badge name to add to the user
        """
        if not self.has_badge(name):
            self.badge_set.create(name=name)


class Badge(models.Model):
    """
    Model for badge
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50)

    class Meta(object):
        unique_together = [
            ('owner', 'name')
        ]


class Model3D(models.Model):
    """
    A 3D Model. Just an image actually
    """
    viewed = django.dispatch.Signal(providing_args=['model'])
    created = django.dispatch.Signal(providing_args=['model'])

    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    name = models.CharField(max_length=50)
    data = models.ImageField()
    view_count = models.IntegerField(default=0)

    def inc_views(self):
        """
        Increment the view count on this model
        """
        self.view_count += 1
        Model3D.viewed.send(self)
        self.save()
