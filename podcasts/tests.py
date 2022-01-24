from urllib import response
from django.test import TestCase
from django.utils import timezone
from django.urls.base import reverse
from .models import Episode
from datetime import datetime

# Create your tests here.

class PodCastsTest(TestCase):
    def setUp(self):
        self.episode = Episode.objects.create(
            title="Testing Podcast Episode", 
            description="Take a look for testing", 
            published_date=timezone.now(),
            link="https://myawesomeshow.com",
            image="https://image.myawesomeshow.com",
            podcast_name="My Python Podcast",
            guid="de194720-7b4c-49e2-a05f-432436d3fetr"
            )

    def test_episode_content(self):
        self.assertEqual(self.episode.description, "Take a look for testing")
        self.assertEqual(self.episode.link, "https://myawesomeshow.com")
        self.assertEqual(
            self.episode.guid, "de194720-7b4c-49e2-a05f-432436d3fetr")

    def test_episode_str_respresentation(self):
        self.assertEqual(str(self.episode),
                         "My Python Podcast: Testing Podcast Episode")

    def test_homepage_status_code(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_homepage_with_correct_template(self):
        response = self.client.get(reverse("homepage"))
        self.assertTemplateUsed(response,"homepage.html")
    
    def test_homepage_list_content(self):
        response = self.client.get(reverse("homepage"))
        self.assertContains(response, "Testing Podcast Episode")
