from django.test import TestCase
from django.contrib.auth.models import User

from accounts.models import UserProfile

class ProfileTest(TestCase):
    def setUp(self):
        self.prof = UserProfile()
        self.prof.user = User(username='testuser')
        self.prof.user.save()
        self.prof.first_name = "test_first_name"
        self.prof.last_name = "test_last_name"
        self.prof.email = "test@gmail.com"
        self.prof.bio = "test_bio"
        self.prof.save()


    def test_profile(self):
        prof = UserProfile()
        prof.user = User(username='myuser')
        prof.user.save()
        prof.first_name = "my_first_name"
        prof.last_name = "my_last_name"
        prof.email = "my@gmail.com"
        prof.bio = "my_bio"
        prof.save()
        record = UserProfile.objects.get(pk=2)

        self.assertEqual(prof, record)

    def test_profile_to_string(self):
        self.assertEqual(self.prof.__str__(), "test_first_name test_last_name")


