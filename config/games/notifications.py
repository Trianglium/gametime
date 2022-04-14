from datetime import timedelta
from urllib.parse import urljoin

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone

from games.models import GameTime


def send_invitation(game_time_invitation):
    subject = render_to_string(
        "games/notifications/invitation_subject.txt",
        {"game_time": game_time_invitation.game_time},
    )

    game_time_path = reverse(
        "game_time_detail_ui", args=(game_time_invitation.game_time.pk,)
    )

    body = render_to_string(
        "games/notifications/invitation_body.txt",
        {
            "creator": game_time_invitation.game_time.creator,
            "game_time": game_time_invitation.game_time,
            "game_time_url": urljoin(settings.BASE_URL, game_time_path),
        },
    )

    send_mail(
        subject,
        body,
        None,
        [game_time_invitation.invitee.email],
    )


def send_attendance_change(game_time_invitation, is_attending):
    subject = render_to_string(
        "games/notifications/attendance_update_subject.txt",
        {
            "game_time": game_time_invitation.game_time,
            "game_time_invitation": game_time_invitation,
        },
    )

    game_time_path = reverse(
        "game_time_detail_ui", args=(game_time_invitation.game_time.pk,)
    )

    body = render_to_string(
        "games/notifications/attendance_update_body.txt",
        {
            "is_attending": is_attending,
            "game_time_invitation": game_time_invitation,
            "game_time": game_time_invitation.game_time,
            "game_time_url": urljoin(settings.BASE_URL, game_time_path),
        },
    )

    send_mail(
        subject,
        body,
        None,
        [game_time_invitation.game_time.creator.email],
    )


def send_starting_notification(game_time):
    subject = render_to_string(
        "games/notifications/starting_subject.txt",
        {"game_time": game_time},
    )

    game_time_path = reverse("game_time_detail_ui", args=(game_time.pk,))

    body = render_to_string(
        "games/notifications/starting_body.txt",
        {
            "game_time": game_time,
            "game_time_url": urljoin(settings.BASE_URL, game_time_path),
        },
    )

    to_emails = [
        invite.invitee.email for invite in game_time.invites.filter(is_attending=True)
    ]
    to_emails.append(game_time.creator.email)

    send_mail(
        subject,
        body,
        None,
        to_emails,
    )
    game_time.start_notification_sent = True
    game_time.save()


def notify_of_starting_soon():
    # Find all events starting within the next 30 minutes
    start_before = timezone.now() + timedelta(minutes=30)

    game_times = GameTime.objects.filter(
        start_time__lte=start_before, start_notification_sent=False
    )

    for game_time in game_times:
        send_starting_notification(game_time)
