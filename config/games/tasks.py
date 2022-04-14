from games import notifications
from games.models import GameTimeInvitation


def send_invitation(mni_pk):
    notifications.send_invitation(GameTimeInvitation.objects.get(pk=mni_pk))


def send_attendance_change(mni_pk, is_attending):
    notifications.send_attendance_change(
        GameTimeInvitation.objects.get(pk=mni_pk), is_attending
    )


def notify_of_starting_soon():
    notifications.notify_of_starting_soon()
