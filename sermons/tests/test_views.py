from django.test import TestCase
from django.urls import reverse

from sermons.models import Sermon, SermonCollection, SermonTag


class SermonViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        collection = SermonCollection.objects.create(
            name="Genesis Saga",
            description="A series through Genesis.",
        )
        tag = SermonTag.objects.create(name="Covenant")
        cls.published = Sermon.objects.create(
            title="God's Promise",
            speaker="Pastor Jordan",
            sermon_date="2026-08-09",
            summary="A summary of the message.",
            thesis="God keeps his promises.",
            main_scripture="Genesis 12",
            transcript="Welcome to the sermon.",
            media_file="sermons/audio/promise.mp3",
            collection=collection,
            is_published=True,
        )
        cls.published.tags.add(tag)
        cls.unpublished = Sermon.objects.create(
            title="Private Draft",
            speaker="Pastor Jordan",
            sermon_date="2026-08-02",
            summary="Not public.",
            thesis="Not public.",
            main_scripture="Genesis 11",
            media_file="sermons/audio/draft.mp3",
            collection=collection,
            is_published=False,
        )

    def test_library_shows_published_sermons_only(self):
        response = self.client.get(reverse("sermons:list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "God&#x27;s Promise", html=False)
        self.assertNotContains(response, "Private Draft")

    def test_search_matches_thesis_and_filters_unpublished_sermons(self):
        response = self.client.get(reverse("sermons:list"), {"q": "promises"})

        self.assertContains(response, "God&#x27;s Promise", html=False)
        self.assertNotContains(response, "Private Draft")

    def test_detail_shows_direct_audio_url_and_content(self):
        response = self.client.get(
            reverse("sermons:detail", kwargs={"slug": self.published.slug})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "sermons/audio/promise.mp3")
        self.assertContains(response, "God keeps his promises.")
        self.assertContains(response, "Welcome to the sermon.")

    def test_detail_shows_other_published_sermons_in_same_collection(self):
        related = Sermon.objects.create(
            title="Related Message",
            speaker="Pastor Jordan",
            sermon_date="2026-08-16",
            summary="A related summary.",
            thesis="A related thesis.",
            main_scripture="Genesis 13",
            media_file="sermons/audio/related.mp3",
            collection=self.published.collection,
            is_published=True,
        )
        Sermon.objects.create(
            title="Private Related Draft",
            speaker="Pastor Jordan",
            sermon_date="2026-08-17",
            summary="Not public.",
            thesis="Not public.",
            main_scripture="Genesis 14",
            media_file="sermons/audio/private-related.mp3",
            collection=self.published.collection,
            is_published=False,
        )

        response = self.client.get(
            reverse("sermons:detail", kwargs={"slug": self.published.slug})
        )

        self.assertContains(response, "Related Message")
        self.assertContains(response, f"/sermons/{related.slug}/", html=False)
        self.assertNotContains(response, "Private Related Draft")

    def test_unpublished_detail_returns_404(self):
        response = self.client.get(
            reverse("sermons:detail", kwargs={"slug": self.unpublished.slug})
        )

        self.assertEqual(response.status_code, 404)

    def test_collection_and_tag_pages_show_published_sermons(self):
        collection_response = self.client.get(
            reverse(
                "sermons:collection_detail",
                kwargs={"slug": self.published.collection.slug},
            )
        )
        tag_response = self.client.get(
            reverse(
                "sermons:tag_detail", kwargs={"slug": self.published.tags.first().slug}
            )
        )

        self.assertContains(collection_response, "God&#x27;s Promise", html=False)
        self.assertNotContains(collection_response, "Private Draft", html=False)
        self.assertContains(tag_response, "God&#x27;s Promise", html=False)

    def test_library_renders_spanish_interface_text(self):
        self.client.cookies["django_language"] = "es"

        response = self.client.get(reverse("sermons:list"))

        self.assertContains(response, "Escucha y crece")
        self.assertContains(response, "Buscar sermones")
        self.assertContains(response, "Todas las colecciones")
