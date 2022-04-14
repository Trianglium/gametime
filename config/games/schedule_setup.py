from django_celery_beat.models import IntervalSchedule, PeriodicTask, CrontabSchedule
import json

def schedule_setup():
    min_schedule, created = IntervalSchedule.objects.get_or_create(period=IntervalSchedule.MINUTES, every=1)

    args = json.dumps(["schedule_setup"])
    PeriodicTask.objects.create(
        name="Notify of Start Every Minute",
        interval=min_schedule,
        args=args,
        task="games.tasks.notify_of_starting_soon",
    )
