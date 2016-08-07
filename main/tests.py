import time

from dateutil.relativedelta import relativedelta
from django.contrib.auth import user_logged_in
from django.test import TestCase
import mock

from main.models import User
from main.models import COLLECTOR_BADGE, PIONEER_BADGE, STAR_BADGE


class UserTestCase(TestCase):
    def test_ensure_badge(self):
        user = User.objects.create(username='t1', email='xx')

        assert not user.has_badge('some-badge')
        user.ensure_badge('some-badge')

        # badge is assigned to user
        assert user.has_badge('some-badge')

        # ensure_badge is idempotent
        user.ensure_badge('some-badge')
        assert user.has_badge('some-badge')
        assert user.badge_set.count() == 1


class BadgeSignalTest(TestCase):
    """
    Check signals awarding badges
    """

    def setUp(self):
        self.user1 = User.objects.create(username='t1', email='xx')

    @mock.patch('django.conf.settings.STAR_BADGE_LIMIT', 3)
    def test_check_star_badge(self):
        """
        Check start badge is awarded after some views of one of its models
        """
        m1 = self.user1.model3d_set.create(name='model1')

        for _ in range(3):
            assert not self.user1.has_badge(STAR_BADGE)
            m1.inc_views()

        assert self.user1.has_badge(STAR_BADGE)

    @mock.patch('django.conf.settings.COLLECTOR_BADGE_LIMIT', 3)
    def test_check_collector_badge(self):
        """
        Check collector badge is awarded after user has uploaded
        `settings.COLLECTOR_BADGE_LIMIT`  models
        """
        for i in range(3):
            assert not self.user1.has_badge(COLLECTOR_BADGE)
            self.user1.model3d_set.create(name='model' + str(i))

        assert self.user1.has_badge(COLLECTOR_BADGE)

    @mock.patch('django.conf.settings.PIONEER_BADGE_LIMIT', relativedelta(seconds=1))
    def test_check_pioneer_badge(self):
        """
        Check pionner badge is awarded to user after some time
        """
        assert not self.user1.has_badge(PIONEER_BADGE)

        # first login won't affect the badge
        user_logged_in.send(User, user=self.user1)
        assert not self.user1.has_badge(PIONEER_BADGE)

        time.sleep(1)

        # after settings.PIONEER_BADGE_LIMIT, new logins does award the badge
        user_logged_in.send(User, user=self.user1)
        assert self.user1.has_badge(PIONEER_BADGE)
