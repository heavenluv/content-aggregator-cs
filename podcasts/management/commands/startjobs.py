from django.core.management.base import BaseCommand
from podcasts.models import Category, Episode
from django.conf import settings
import logging
import feedparser
from dateutil import parser
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.schedulers.base import *
from pytz import utc
import re

logger = logging.getLogger(__name__)


def delete_old_job_executions(max_age=604_800):
    """Deletes all apscheduler job execution logs older than `max_age`."""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


def save_episode(feed, genre):
    podcast_title = feed.channel.title
    podcast_image = feed.channel.image["href"]
    for item in feed.entries:
        if not Episode.objects.filter(guid=item.guid).exists():
            episode = Episode(
                title=item.title,
                category=Category.objects.filter(title=genre)[0],
                description=re.sub("<.*?>", "", item.description),
                published_date=parser.parse(item.published),
                link=item.link,
                image=podcast_image,
                podcast_name=podcast_title,
                guid=item.guid,
            )
            episode.save()


def fetch_realpython_episode():
    feed = feedparser.parse("https://realpython.com/podcasts/rpp/feed")
    save_episode(feed, "Python")


def fetch_talkpython_episode():
    feed = feedparser.parse("https://talkpython.fm/episodes/rss")
    save_episode(feed, "Python")


def fetch_talkingmachine_episode():
    feed = feedparser.parse(
        "https://www.omnycontent.com/d/playlist/aaea4e69-af51-495e-afc9-a9760146922b/b92baa3c-b9c8-488c-aa9e-aafd001cbf66/12abbc3c-ae53-487a-b83b-aafd001cbf79/podcast.rss")
    save_episode(feed, "Machine Learning")


def fetch_nssdeviations_episode():
    feed = feedparser.parse(
        "https://nssdeviations.libsyn.com/rss")
    save_episode(feed, "Data Science")


def fetch_datastories_episode():
    feed = feedparser.parse(
        "https://datastori.es/feed/mp3/")
    save_episode(feed, "Data Science")


def fetch_superdatascience_episode():
    feed = feedparser.parse(
        "https://feeds.soundcloud.com/users/soundcloud:users:253585900/sounds.rss")
    save_episode(feed, "Data Science")


def fetch_learningmachine101_episode():
    feed = feedparser.parse(
        "https://learningmachines101.libsyn.com/rss")
    save_episode(feed, "Machine Learning")


def fetch_industryai_episode():
    feed = feedparser.parse(
        "https://techemergence.libsyn.com/rss")
    save_episode(feed, "Machine Learning")


def fetch_csstrickepisode():
    feed = feedparser.parse(
        "https://css-tricks.com/feed/")
    save_episode(feed, "Frontend")


def fetch_smashmagazine_episode():
    feed = feedparser.parse(
        "https://www.smashingmagazine.com/feed")
    save_episode(feed, "Frontend")


def fetch_crazyprogrammer_episode():
    feed = feedparser.parse(
        "http://www.thecrazyprogrammer.com/feed")
    save_episode(feed, "Backend")


def fetch_stackoverflow_episode():
    feed = feedparser.parse(
        "https://stackoverflow.blog/feed/")
    save_episode(feed, "Backend")


def fetch_stackabuse_episode():
    feed = feedparser.parse(
        "https://stackabuse.com/rss/")
    save_episode(feed, "Backend")


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        jobstores = {
            'default': DjangoJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(10),
        }
        job_defaults = {
            # 'coalesce': False,
            'max_instances': 8
        }
        scheduler = BlockingScheduler(
            executors=executors, job_defaults=job_defaults, timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            fetch_realpython_episode,
            trigger="interval",
            minutes=1,
            id="The Real Python Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Real Python Podcast.")

        scheduler.add_job(
            fetch_talkpython_episode,
            trigger="interval",
            minutes=1,
            id="Talk Python Feed",
            replace_existing=True,
        )
        logger.info("Added job: Talk Python Feed.")

        scheduler.add_job(
            fetch_talkingmachine_episode,
            trigger="interval",
            minutes=1,
            id="The Talking Machine Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Talking Machine Podcast.")

        scheduler.add_job(
            fetch_nssdeviations_episode,
            trigger="interval",
            minutes=1,
            id="The NSS Deviation Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The NSS Deviation Podcast.")

        scheduler.add_job(
            fetch_datastories_episode,
            trigger="interval",
            minutes=1,
            id="The Data Stories Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Data Stories Podcast.")

        scheduler.add_job(
            fetch_superdatascience_episode,
            trigger="interval",
            minutes=1,
            id="The Super Data Science Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Super Data Science Podcast.")

        scheduler.add_job(
            fetch_learningmachine101_episode,
            trigger="interval",
            minutes=1,
            id="The Learning Machine 101 Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The The Learning Machine 101 Podcast.")

        scheduler.add_job(
            fetch_industryai_episode,
            trigger="interval",
            minutes=1,
            id="The Industry AI Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Industry AI Podcast.")

        scheduler.add_job(
            fetch_csstrickepisode,
            trigger="interval",
            minutes=1,
            id="The CSS Trick Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The CSS Trick Podcast.")

        scheduler.add_job(
            fetch_smashmagazine_episode,
            trigger="interval",
            minutes=1,
            id="The Smashing Magazine Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Smashing Magazine Podcast.")

        scheduler.add_job(
            fetch_crazyprogrammer_episode,
            trigger="interval",
            minutes=1,
            id="The Crazy Programmer Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Crazy Programmer Podcast.")

        scheduler.add_job(
            fetch_stackoverflow_episode,
            trigger="interval",
            minutes=1,
            id="The Stack Overflow Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Stack Overflow Podcast.")

        scheduler.add_job(
            fetch_stackabuse_episode,
            trigger="interval",
            minutes=1,
            id="The Stack Abuse Podcast",
            replace_existing=True,
        )
        logger.info("Added job: The Stack Abuse Podcast.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),  # Midnight on Monday, before start of the next work week.
            id="Delete Old Job Executions",
            replace_existing=True,
        )
        logger.info("Added weekly job: Delete Old Job Executions.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
            scheduler.print_jobs()
        # except e:
        #     print(e)
        except KeyboardInterrupt:
            print("Stopping scheduler...")
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")


# class Command(BaseCommand):
#     help = "Runs apscheduler."
#     def handle(self, *args, **options):
#         scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
#         scheduler.add_jobstore(DjangoJobStore(), "default")

#         scheduler.add_job(
#             fetch_realpython_episode,
#             trigger="interval",
#             minutes=1,
#             id="The Real Python Podcast",
# #             replace_existing=True,
#         )
#         logger.info("Added job: The Real Python Podcast.")

#         scheduler.add_job(
#             fetch_talkpython_episode,
#             trigger="interval",
#             minutes=1,
#             id="Talk Python Feed",
# #             replace_existing=True,
#         )
#         logger.info("Added job: Talk Python Feed.")


#         scheduler.add_job(
#             delete_old_job_executions,
#             trigger=CronTrigger(
#                 day_of_week="mon", hour="00", minute="00"
#             ),  # Midnight on Monday, before start of the next work week.
#             id="Delete Old Job Executions",
# #             replace_existing=True,
#         )
#         logger.info("Added weekly job: Delete Old Job Executions.")

#         try:
#             logger.info("Starting scheduler...")
#             scheduler.start()
#         except KeyboardInterrupt:
#             logger.info("Stopping scheduler...")
#             scheduler.shutdown()
#             logger.info("Scheduler shut down successfully!")
