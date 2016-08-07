from __future__ import unicode_literals

from django.apps import AppConfig


class MainConfig(AppConfig):
    name = 'main'

    def ready(self):
        import main.badges # pylint: disable=unused-variable
