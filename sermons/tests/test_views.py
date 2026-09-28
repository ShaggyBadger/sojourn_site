from django.test import TestCase
from django.urls import reverse

from sermons.models import Sermon, SermonCollection, SermonTag, SermonTranslation


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

    def test_library_uses_ten_sermons_per_page_in_newest_first_order(self):
        for index in range(10):
            Sermon.objects.create(
                title=f"Archive Message {index}",
                speaker="Pastor Jordan",
                sermon_date=f"2026-07-{index + 1:02d}",
                summary="An archive summary.",
                thesis="An archive thesis.",
                main_scripture="Genesis 1",
                media_file=f"sermons/audio/archive-{index}.mp3",
                is_published=True,
            )

        response = self.client.get(reverse("sermons:list"))

        self.assertEqual(response.context["paginator"].per_page, 10)
        self.assertEqual(response.context["paginator"].num_pages, 2)
        self.assertContains(response, "Archive Message 9")
        self.assertNotContains(response, "Archive Message 0")

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

    def test_spanish_detail_metadata_and_structured_data_use_translation(self):
        SermonTranslation.objects.create(
            sermon=self.published,
            language=SermonTranslation.Language.SPANISH,
            title="La promesa de Dios",
            summary="Un resumen del mensaje.",
            thesis="Dios cumple sus promesas.",
            transcript="Bienvenidos al sermón.",
        )

        response = self.client.get(
            f"/es{reverse('sermons:detail', kwargs={'slug': self.published.slug})}"
        )

        self.assertContains(response, "<title>La promesa de Dios | Sermones</title>", html=False)
        self.assertContains(
            response,
            'name="description" content="Un resumen del mensaje."',
            html=False,
        )
        self.assertContains(response, '"headline":"La promesa de Dios"', html=False)
        self.assertContains(response, '"description":"Un resumen del mensaje."', html=False)
        self.assertContains(response, '"inLanguage":"es"', html=False)
        self.assertContains(
            response,
            f'"url":"https://sojourn-church.com/es/sermons/{self.published.slug}/"',
            html=False,
        )
        self.assertContains(response, 'name="robots" content="index,follow"', html=False)
        self.assertContains(
            response,
            f'rel="canonical" href="https://sojourn-church.com/es/sermons/{self.published.slug}/"',
            html=False,
        )
        self.assertContains(response, 'hreflang="es"', html=False)

    def test_incomplete_spanish_detail_is_not_indexed_as_an_english_duplicate(self):
        response = self.client.get(
            f"/es{reverse('sermons:detail', kwargs={'slug': self.published.slug})}"
        )

        self.assertContains(response, 'name="robots" content="noindex,follow"', html=False)
        self.assertContains(
            response,
            f'rel="canonical" href="https://sojourn-church.com/sermons/{self.published.slug}/"',
            html=False,
        )
        self.assertNotContains(response, 'hreflang="es"', html=False)

    def test_sermon_sitemap_advertises_only_complete_spanish_translations(self):
        complete = Sermon.objects.create(
            title="A Complete Message",
            speaker="Pastor Jordan",
            sermon_date="2026-08-16",
            summary="An English summary.",
            thesis="An English thesis.",
            main_scripture="Genesis 13",
            transcript="An English transcript.",
            media_file="sermons/audio/complete.mp3",
            is_published=True,
        )
        SermonTranslation.objects.create(
            sermon=complete,
            language=SermonTranslation.Language.SPANISH,
            title="Un mensaje completo",
            summary="Un resumen completo.",
            thesis="Una tesis completa.",
            transcript="Una transcripción completa.",
        )

        response = self.client.get("/sitemap.xml")

        self.assertContains(response, f"/es/sermons/{complete.slug}/")
        self.assertNotContains(response, f"/es/sermons/{self.published.slug}/")

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

    def test_spanish_collection_and_tag_pages_are_not_indexed_without_translations(self):
        collection_path = reverse(
            "sermons:collection_detail",
            kwargs={"slug": self.published.collection.slug},
        )
        tag_path = reverse(
            "sermons:tag_detail", kwargs={"slug": self.published.tags.first().slug}
        )

        for path in (collection_path, tag_path):
            with self.subTest(path=path):
                english_response = self.client.get(path)
                self.assertNotContains(english_response, 'hreflang="es"', html=False)

                response = self.client.get(f"/es{path}")
                self.assertContains(
                    response,
                    'name="robots" content="noindex,follow"',
                    html=False,
                )
                self.assertNotContains(response, 'hreflang="es"', html=False)

    def test_library_renders_spanish_interface_text(self):
        response = self.client.get("/es/sermons/")

        self.assertContains(response, "Escucha y crece")
        self.assertContains(response, "Buscar sermones")
        self.assertContains(response, "Todas las colecciones")
