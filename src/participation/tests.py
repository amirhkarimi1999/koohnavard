from django.test import TestCase
from participation.models import Club, ClubMember
from accounts.models import User


def create_club():
    user = User.objects.create(username='my_username')
    return Club.objects.create(title='my club', owner=user)


# Create your tests here.
class ClubModelTests(TestCase):
    def test_club_creation(self):
        club = create_club()
        owner = ClubMember.objects.create(user=club.owner, club=club, pending=False)
        self.assertEqual(club.members_cnt, 1)
        self.assertEqual(owner.pending, False)

    def test_add_member_to_club(self):
        club = create_club()
        user2 = User.objects.create(username='my_username2')
        owner = ClubMember.objects.create(user=club.owner, club=club, pending=False)
        club_member = ClubMember.objects.create(user=user2, club=club)
        self.assertEqual(club_member.pending, True)
        self.assertEqual(club.members_cnt, 1)
        club_member.pending = False
        club_member.save()
        self.assertEqual(club.members_cnt, 2)

    def test_delete_member_from_club(self):
        user = User.objects.create(username='my_username')
        club = Club.objects.create(title='my club', owner=user)
        owner = ClubMember.objects.create(user=club.owner, club=club, pending=False)
        user2 = User.objects.create(username='my_username2')
        club_member = ClubMember.objects.create(user=user2, club=club, pending=False)
        user2.delete()
        self.assertEqual(club.members_cnt, 1)

    def test_delete_owner_from_club(self):
        user = User.objects.create(username='my_username')
        club = Club.objects.create(title='my club', owner=user)
        owner = ClubMember.objects.create(user=club.owner, club=club, pending=False)
        user.delete()
        try:
            club.refresh_from_db()
        except Club.DoesNotExist:
            self.assertTrue(True)
        else:
            self.assertTrue(False)