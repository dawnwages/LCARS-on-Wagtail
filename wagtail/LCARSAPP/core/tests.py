import datetime
import json

from django.test import TestCase
from django.urls import reverse
from wagtail.images.tests.utils import get_test_image_file
from wagtail.images import get_image_model
from wagtail.models import Page

from core.models import CorePage


class CorePageAPITests(TestCase):
    """Pin the shape of the headless API that the Vue frontend consumes."""

    @classmethod
    def setUpTestData(cls):
        cls.image = get_image_model().objects.create(
            title="Enterprise", file=get_test_image_file()
        )
        root = Page.objects.get(depth=1).get_children().first()
        cls.page = root.add_child(instance=CorePage(
            title="Captain's log",
            slug="captains-log",
            date=datetime.date(2364, 1, 1),
            intro="Stardate 41153.7",
            body=json.dumps([
                {"type": "heading", "value": "Encounter at Farpoint"},
                {"type": "paragraph", "value": '<p>Our destination is <a href="https://example.com">Farpoint</a>.</p>'},
                {"type": "image", "value": cls.image.pk},
            ]),
        ))

    def get_json(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, response.content[:500])
        return response.json()

    def test_listing_includes_core_page(self):
        data = self.get_json("/api/v2/pages/?type=core.CorePage&fields=date,intro")
        self.assertEqual(data["meta"]["total_count"], 1)
        item = data["items"][0]
        self.assertEqual(item["title"], "Captain's log")
        self.assertEqual(item["date"], "2364-01-01")
        self.assertEqual(item["intro"], "Stardate 41153.7")
        self.assertEqual(item["meta"]["type"], "core.CorePage")

    def test_frontend_listing_body_blocks(self):
        # The exact request made by LCARS/src/services/DataService.js
        data = self.get_json("/api/v2/pages/?type=core.CorePage&fields=intro,body,id,date")
        body = data["items"][0]["body"]
        self.assertEqual([b["type"] for b in body], ["heading", "paragraph", "image"])
        self.assertEqual(body[0]["value"], "Encounter at Farpoint")
        self.assertIn("Farpoint", body[1]["value"])

        image = body[2]["value"]
        self.assertEqual(image["id"], self.image.pk)
        self.assertEqual(image["title"], "Enterprise")
        self.assertEqual(set(image["large"]), {"src", "width", "height", "alt"})
        self.assertEqual(set(image["thumbnail"]), {"src", "width", "height", "alt"})
        self.assertEqual((image["thumbnail"]["width"], image["thumbnail"]["height"]), (120, 120))

    def test_detail_endpoint(self):
        data = self.get_json(f"/api/v2/pages/{self.page.pk}/")
        self.assertEqual(data["intro"], "Stardate 41153.7")
        self.assertEqual(len(data["body"]), 3)

    def test_external_links_are_nofollow_when_rendered(self):
        from wagtail.rich_text import expand_db_html

        html = expand_db_html('<a linktype="external" href="https://example.com">x</a>')
        self.assertIn('rel="nofollow"', html)

    def test_images_endpoint(self):
        data = self.get_json("/api/v2/images/")
        self.assertEqual(data["meta"]["total_count"], 1)

    def test_cors_allows_frontend_origin(self):
        response = self.client.get("/api/v2/pages/", HTTP_ORIGIN="http://localhost:8080")
        self.assertEqual(response["access-control-allow-origin"], "http://localhost:8080")


class SiteSmokeTests(TestCase):
    def test_admin_login_renders(self):
        self.assertEqual(self.client.get("/admin/login/").status_code, 200)

    def test_core_page_editor_renders(self):
        from django.contrib.auth import get_user_model

        user = get_user_model().objects.create_superuser("picard", "picard@example.com", "engage")
        self.client.force_login(user)
        parent = Page.objects.get(depth=2)
        response = self.client.get(f"/admin/pages/add/core/corepage/{parent.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_search_renders(self):
        response = self.client.get(reverse("search"), {"query": "farpoint"})
        self.assertEqual(response.status_code, 200)
