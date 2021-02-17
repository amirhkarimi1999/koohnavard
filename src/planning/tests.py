from django.test import TestCase
from django.contrib.auth.models import User
from planning.models import Plan, Charge, PlanParticipant
from participation.models import Club, ClubMember
from accounts.models import UserProfile

class PlanTest(TestCase):
    def setUp(self):
        # info
        self.title = 'Sangchal to Diva'
        self.description = 'Lets go nuts'
        self.destination_address = 'Diva'
        self.head_man_name = 'aryan molanayi'

        # create a club
        self.club = Club.objects.create(title='my club', owner=User.objects.create(username='club_owner'))

        # create a head_man user
        head_man_user = User.objects.create(username=self.head_man_name)
        head_man_prof = UserProfile.objects.create(user=head_man_user)
        head_man_user.save()
        head_man_prof.save()
        self.head_user=head_man_user
        self.head_prof=head_man_prof
        self.head_club_member = ClubMember.objects.create(club=self.club, user=head_man_user, pending=False)

        self.plan = Plan.objects.create(club=self.club, title=self.title, description=self.description, destination_address=self.destination_address, head_man=self.head_man_name)

        # register the headman to the plan
        self.head_participant = PlanParticipant.objects.create(plan=self.plan, user=head_man_user, status='ACCEPTED')

        ## create some dummy users to be able to use below
        self.user1 = User.objects.create(username="user1")
        self.user2 = User.objects.create(username='user2')
        self.user1.save()
        self.user2.save()


    def test_plan_str(self):
        self.assertEqual(self.plan.__str__(), self.title + " " + self.club.__str__())

    def test_head_man_user_property(self):
        self.assertEqual(User.objects.get(username=self.head_man_name), self.plan.head_man_user)

    def test_participant_count(self):
        self.assertEqual(self.plan.participants_cnt, 1)

    def test_add_participant(self):
        self.assertEqual(self.plan.participants_cnt, 1)
        participant1 = PlanParticipant.objects.create(plan=self.plan, user=self.user1, status='ACCEPTED')
        participant1.save()
        self.assertEqual(self.plan.participants_cnt, 2)
        participant2 = PlanParticipant.objects.create(plan=self.plan, user=self.user2, status='PENDING')
        participant2.save()
        self.assertEqual(self.plan.participants_cnt, 2)


    def test_delete_participant(self):
        self.assertEqual(self.plan.participants_cnt, 1)
        participant1 = PlanParticipant.objects.create(plan=self.plan, user=self.user1, status='ACCEPTED')
        participant1.save()
        self.assertEqual(self.plan.participants_cnt, 2)
        participant2 = PlanParticipant.objects.create(plan=self.plan, user=self.user2, status='PENDING')
        participant2.save()
        self.assertEqual(self.plan.participants_cnt, 2)
        participant1.delete()
        self.assertEqual(self.plan.participants_cnt, 1)
        participant2.delete()
        self.assertEqual(self.plan.participants_cnt, 1)

    def test_total_pay(self):
        Charge.objects.create(plan=self.plan, user=self.plan.head_man_user, title='ash reshte',
                              description='eat', amount=20)
        self.assertEqual(self.head_participant.user_total_pay, 20)
        Charge.objects.create(plan=self.plan, user=self.plan.head_man_user, title='lubya polo',
                              description='eat', amount=50)
        self.assertEqual(self.head_participant.user_total_pay, 70)
        Charge.objects.create(plan=self.plan, user=self.plan.head_man_user, title='bread',
                              description='buy', amount=-10)
        self.assertEqual(self.head_participant.user_total_pay, 60)





    # someone who is not a member of the club shouldn't be able to particiapte in the plan
    def test_participation_of_a_non_club_member(self):
        participant1 = PlanParticipant.objects.create(plan=self.plan, user=self.user1)
        participant1.save()
        self.assertEqual(self.plan.participants_cnt, 1)



    def test_get_user_function_plan_participant(self):
        self.assertEqual(self.head_prof, self.head_participant.getUser)

    """
        todo! getting integrity error for the following two functions.
    """
    # def test_charges_after_deleting_plan(self):
    #     Charge.objects.create(plan=self.plan, user=self.plan.head_man_user, title='ash reshte',
    #                           description='eat', amount=20)
    #     self.assertEqual(self.head_participant.user_total_pay, 20)
    #     self.plan.delete()
    #     self.assertEqual(self.head_participant.user_total_pay, 0)
    #
    #
    # # a plan lives even after deleting its club
    # def test_plan_after_deleting_club(self):
    #     self.plan.club.delete()
    #     try:
    #         Plan.objects.get(headman=self.head_man_name)
    #     except Plan.DoesNotExist:
    #         self.assertTrue(False)
    #     else:
    #         self.assertTrue(True)


