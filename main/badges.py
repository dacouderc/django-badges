"""
Signal handler to award badges to user
"""

from datetime import datetime

from django.conf import settings
from django.contrib.auth import user_logged_in
from django.dispatch import receiver
from django.db.models.signals import post_save
import pytz

from main.models import Model3D, STAR_BADGE, COLLECTOR_BADGE, PIONEER_BADGE


@receiver(user_logged_in)
def check_pionner_badge(user, **kwargs):
    """
    Check pioneer badge requirement after each login
    """
    now = datetime.now(pytz.utc)
    if user.date_joined + settings.PIONEER_BADGE_LIMIT < now:
        user.ensure_badge(PIONEER_BADGE)


@receiver(post_save, sender=Model3D)
def check_collector_badges(instance, created, **kwargs):
    """
    Check number of uploaded model to award the collector badge

    :param Model3D instance: the model which has been viewed
    :param bool created: Wether the instance is new or not
    """
    if created:
        if instance.owner.model3d_set.count() >= settings.COLLECTOR_BADGE_LIMIT:
            instance.owner.ensure_badge(COLLECTOR_BADGE)


@receiver(Model3D.viewed)
def check_star_badge(sender, **kwargs):
    """
    When a model is viewed, check the view count
    of the model to award the STAR_BADGE

    :param Model3D sender: the model which has been viewed
    """
    if sender.view_count >= settings.STAR_BADGE_LIMIT:
        sender.owner.ensure_badge(STAR_BADGE)
