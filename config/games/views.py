from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from games.forms import SearchForm, GameTimeForm, InviteeForm, AttendanceForm
from games.models import Game, GameTime, GameTimeInvitation
from games.igdb_integration import search_and_save, fill_game_details


def index(request):
    return render(request, "games/index.html")


@login_required
def game_search(request):
    search_form = SearchForm(request.POST)

    if search_form.is_valid() and search_form.cleaned_data["term"]:
        term = search_form.cleaned_data["term"]
        search_and_save(term)
        game_list = Game.objects.filter(title__icontains=term)
        did_search = True
    else:
        game_list = []
        did_search = False

    return render(
        request,
        "games/search.html",
        {
            "page_group": "search",
            "search_form": search_form,
            "game_list": game_list,
            "did_search": did_search,
        },
    )


@login_required
def game_time_list(request):
    start_time_after = timezone.now() - timedelta(hours=2)
    created_game_times = GameTime.objects.filter(
        creator=request.user, start_time__gt=start_time_after
    )
    invited_game_times = GameTime.objects.filter(
        start_time__gt=start_time_after,
        invites__in=GameTimeInvitation.objects.filter(invitee=request.user),
    )

    return render(
        request,
        "games/game_time_list.html",
        {
            "page_group": "game-times",
            "created_game_times": created_game_times,
            "invited_game_times": invited_game_times,
        },
    )


@login_required
def game_detail(request, igdb_id):
    game = get_object_or_404(Game, igdb_id=igdb_id)
    fill_game_details(game)
    if request.method == "POST":
        game_time_form = GameTimeForm(request.POST)
        if game_time_form.is_valid():
            game_time = game_time_form.save(False)
            game_time.game = game
            game_time.creator = request.user
            game_time.save()
            return redirect("game_time_detail_ui", game_time.pk)
    else:
        game_time_form = GameTimeForm()
    return render(
        request,
        "games/game_detail.html",
        {"page_group": "search", "game": game, "game_time_form": game_time_form},
    )


@login_required
def game_time_detail(request, pk):
    game_time = get_object_or_404(GameTime, pk=pk)

    is_creator = game_time.creator == request.user

    invitee_form = None
    attendance_form = None

    invitees = {invitation.invitee for invitation in game_time.invites.all()}

    is_in_the_past = game_time.start_time < timezone.now()

    if not is_creator:
        if request.user not in invitees:
            raise PermissionDenied("You do not have access to this GameTime")

        invitation = game_time.invites.filter(invitee=request.user).first()

        if not is_in_the_past and request.method == "POST":
            attendance_form = AttendanceForm(request.POST, instance=invitation)
            if attendance_form.is_valid():
                attendance_form.save()
        else:
            attendance_form = AttendanceForm(instance=invitation)
    else:
        if not is_in_the_past and request.method == "POST":
            invitee_form = InviteeForm(request.POST)

            if invitee_form.is_valid():
                invitee = invitee_form._user

                if invitee == request.user or invitee in invitees:
                    invitee_form.add_error(
                        "email", "That user is the creator or already invited"
                    )
                else:
                    GameTimeInvitation.objects.create(
                        invitee=invitee, game_time=game_time
                    )
                    return redirect(request.path)  # effectively, just reload the page
        else:
            invitee_form = InviteeForm()

    return render(
        request,
        "games/game_time_detail.html",
        {
            "page_group": "game-times",
            "game_time": game_time,
            "is_creator": is_creator,
            "invitee_form": invitee_form,
            "attendance_form": attendance_form,
            "is_in_the_past": is_in_the_past,
        },
    )
