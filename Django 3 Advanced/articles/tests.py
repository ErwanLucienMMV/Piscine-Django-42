from urllib.parse import parse_qs, urlsplit

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import Client, TestCase
from django.urls import resolve, reverse
from django.utils import translation
from django.views.generic import CreateView, DetailView, ListView, RedirectView

from .models import Article, UserFavouriteArticle
from .templatetags.article_tags import short_synopsis


class ArticleSiteTests(TestCase):
    fixtures = ["demo"]

    def setUp(self):
        translation.activate("en")
        self.alice = get_user_model().objects.get(username="alice")
        self.bob = get_user_model().objects.get(username="bob")
        self.article = Article.objects.get(pk=1)

    def tearDown(self):
        translation.deactivate()

    def login(self):
        self.client.force_login(self.alice)

    def test_favourites_publications_and_publish_redirect_anonymous_gets_without_rendering_their_templates(self):
        for name in ("favourites", "publications", "publish"):
            with self.subTest(view=name):
                target = reverse(name)
                response = self.client.get(target)
                self.assertEqual(response.status_code, 302)
                redirect = urlsplit(response.url)
                self.assertEqual(redirect.path, reverse("login"))
                self.assertEqual(parse_qs(redirect.query)["next"], [target])
                self.assertTemplateNotUsed(response, "articles/" + name + ".html")
                self.assertTemplateNotUsed(response, "articles/form.html")

    def test_anonymous_publish_and_favourite_posts_do_not_create_records(self):
        article_count = Article.objects.count()
        favourite_count = UserFavouriteArticle.objects.count()
        self.assertEqual(self.client.post(reverse("publish"), {
            "title": "Blocked", "synopsis": "Blocked", "content": "Blocked"
        }).status_code, 302)
        self.assertEqual(self.client.post(reverse("add_favourite", kwargs={"pk": self.article.pk})).status_code, 302)
        self.assertEqual(Article.objects.count(), article_count)
        self.assertEqual(UserFavouriteArticle.objects.count(), favourite_count)

    def test_favourites_publications_and_publish_render_their_templates_for_authenticated_users(self):
        self.login()
        for name, template in (("favourites", "favourites"), ("publications", "publications"), ("publish", "form")):
            with self.subTest(view=name):
                response = self.client.get(reverse(name))
                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f"articles/{template}.html")

    def test_authenticated_users_cannot_get_the_registration_form(self):
        self.login()
        response = self.client.get(reverse("register"))
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        self.assertTemplateNotUsed(response, "articles/form.html")

    def test_authenticated_users_cannot_create_another_account_by_posting_to_register(self):
        self.login()
        count = get_user_model().objects.count()
        response = self.client.post(reverse("register"), {
            "username": "another-account", "password1": "Strong-New-Password-42!", "password2": "Strong-New-Password-42!"
        })
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        self.assertEqual(get_user_model().objects.count(), count)

    def test_posting_the_same_article_twice_creates_only_one_favourite(self):
        self.login()
        route = reverse("add_favourite", kwargs={"pk": self.article.pk})
        for _ in range(2):
            response = self.client.post(route)
            self.assertRedirects(response, self.article.get_absolute_url())
        self.assertEqual(UserFavouriteArticle.objects.filter(user=self.alice, article=self.article).count(), 1)

    def test_database_constraint_also_rejects_duplicate_favourites(self):
        favourite = UserFavouriteArticle.objects.filter(user=self.alice).first()
        with self.assertRaises(IntegrityError), transaction.atomic():
            UserFavouriteArticle.objects.create(user=self.alice, article=favourite.article)

    def test_different_users_can_each_save_the_same_article(self):
        UserFavouriteArticle.objects.create(user=self.alice, article=self.article)
        self.client.force_login(self.bob)
        self.client.post(reverse("add_favourite", kwargs={"pk": self.article.pk}))
        self.assertEqual(UserFavouriteArticle.objects.filter(article=self.article).count(), 2)

    def test_favourite_post_uses_the_session_user_and_url_article_despite_forged_fields(self):
        self.login()
        self.client.post(reverse("add_favourite", kwargs={"pk": self.article.pk}), {"user": self.bob.pk, "article": 5})
        self.assertTrue(UserFavouriteArticle.objects.filter(user=self.alice, article=self.article).exists())
        self.assertFalse(UserFavouriteArticle.objects.filter(user=self.bob, article=self.article).exists())

    def test_favourite_get_redirects_to_detail_without_creating_a_favourite(self):
        self.login()
        count = UserFavouriteArticle.objects.count()
        self.assertRedirects(self.client.get(reverse("add_favourite", kwargs={"pk": self.article.pk})), self.article.get_absolute_url())
        self.assertEqual(UserFavouriteArticle.objects.count(), count)

    def test_unknown_article_returns_404_for_detail_and_favourite_actions(self):
        self.login()
        for name in ("detail", "add_favourite"):
            for method in (self.client.get, self.client.post) if name == "add_favourite" else (self.client.get,):
                with self.subTest(view=name, method=method.__name__):
                    self.assertEqual(method(reverse(name, kwargs={"pk": 999999})).status_code, 404)

    def test_publications_only_include_articles_owned_by_the_current_user(self):
        self.login()
        response = self.client.get(reverse("publications"))
        self.assertEqual(set(response.context["articles"]), set(Article.objects.filter(author=self.alice)))
        self.assertContains(response, reverse("publish"))

    def test_favourites_only_include_the_current_users_saved_articles(self):
        UserFavouriteArticle.objects.create(user=self.bob, article=self.article)
        self.login()
        response = self.client.get(reverse("favourites"))
        self.assertEqual(list(response.context["favourites"].values_list("article_id", flat=True)), [2, 3])
        for favourite in response.context["favourites"]:
            self.assertContains(response, favourite.article.get_absolute_url())

    def test_publish_form_omits_author_and_created_fields_and_assigns_the_logged_in_author(self):
        self.login()
        form = self.client.get(reverse("publish")).context["form"]
        self.assertEqual(set(form.fields), {"title", "synopsis", "content"})
        response = self.client.post(reverse("publish"), {
            "title": "A new story", "synopsis": "A short introduction", "content": "The complete story.", "author": self.bob.pk
        })
        article = Article.objects.get(title="A new story")
        self.assertEqual(article.author, self.alice)
        self.assertIsNotNone(article.created)
        self.assertRedirects(response, article.get_absolute_url())

    def test_publish_rejects_overlong_titles_and_synopses_without_saving(self):
        self.login()
        count = Article.objects.count()
        response = self.client.post(reverse("publish"), {"title": "x" * 65, "synopsis": "y" * 313, "content": "Story"})
        self.assertFormError(response.context["form"], "title", "Ensure this value has at most 64 characters (it has 65).")
        self.assertIn("synopsis", response.context["form"].errors)
        self.assertEqual(Article.objects.count(), count)

    def test_anonymous_registration_creates_a_user_with_a_hashed_password(self):
        password = "Strong-New-Password-42!"
        response = self.client.post(reverse("register"), {"username": "new-reader", "password1": password, "password2": password})
        self.assertRedirects(response, reverse("login"))
        user = get_user_model().objects.get(username="new-reader")
        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_staff)

    def test_registration_rejects_mismatched_passwords_and_duplicate_usernames(self):
        count = get_user_model().objects.count()
        response = self.client.post(reverse("register"), {"username": "alice", "password1": "New-Strong-Pass-42!", "password2": "Different-Strong-Pass-42!"})
        self.assertIn("username", response.context["form"].errors)
        self.assertIn("password2", response.context["form"].errors)
        self.assertEqual(get_user_model().objects.count(), count)

    def test_valid_menu_login_redirects_home_and_invalid_login_renders_errors(self):
        response = self.client.post(reverse("login"), {"menu-username": "alice", "menu-password": "wrong"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="login-errors"')
        response = self.client.post(reverse("login"), {"menu-username": "alice", "menu-password": "Articles-Demo-42!"})
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.alice.pk)

    def test_logout_requires_post_and_clears_the_authenticated_session(self):
        self.login()
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_registration_publish_favourite_and_logout_posts_require_csrf_tokens(self):
        client = Client(enforce_csrf_checks=True)
        for name in ("login", "register"):
            self.assertEqual(client.post(reverse(name), {}).status_code, 403)
        client.force_login(self.alice)
        for name in ("publish", "logout", "add_favourite"):
            with self.subTest(view=name):
                kwargs = {"pk": self.article.pk} if name == "add_favourite" else None
                self.assertEqual(client.post(reverse(name, kwargs=kwargs), {}).status_code, 403)

    def test_home_redirects_to_the_article_list(self):
        self.assertRedirects(self.client.get(reverse("root")), reverse("articles"))
        self.assertRedirects(self.client.get(reverse("home")), reverse("articles"))

    def test_all_five_demo_articles_are_listed_newest_first_without_full_content(self):
        response = self.client.get(reverse("articles"))
        self.assertEqual([article.pk for article in response.context["articles"]], [5, 4, 3, 2, 1])
        for article in response.context["articles"]:
            self.assertContains(response, article.title)
            self.assertContains(response, article.get_absolute_url())
            self.assertNotContains(response, article.content)

    def test_synopsis_filter_limits_long_values_to_twenty_characters_with_three_dots(self):
        self.assertEqual(short_synopsis("short"), "short")
        self.assertEqual(short_synopsis("x" * 20), "x" * 20)
        self.assertEqual(short_synopsis("x" * 21), "x" * 17 + "...")
        self.assertContains(self.client.get(reverse("articles")), short_synopsis(self.article.synopsis))

    def test_detail_contains_every_article_field_and_an_empty_favourite_form_only_when_logged_in(self):
        response = self.client.get(self.article.get_absolute_url())
        for value in (self.article.title, self.article.synopsis, self.article.content, self.article.author.username):
            self.assertContains(response, value)
        self.assertContains(response, str(self.article.created.year))
        self.assertNotIn("favourite_form", response.context)
        self.login()
        response = self.client.get(self.article.get_absolute_url())
        self.assertEqual(list(response.context["favourite_form"].fields), [])
        self.assertEqual(response.context["favourite_form"].instance.article, self.article)

    def test_article_and_favourite_string_representations_return_the_article_title(self):
        self.assertEqual(str(self.article), self.article.title)
        favourite = UserFavouriteArticle.objects.first()
        self.assertEqual(str(favourite), favourite.article.title)

    def test_english_and_french_article_pages_translate_menu_headers_times_and_language_links(self):
        for language, tagline, title in (("en", "Share your writings", "Title"), ("fr", "Partagez vos écrits", "Titre")):
            with self.subTest(language=language), translation.override(language):
                response = self.client.get(reverse("articles"))
                self.assertContains(response, f'<html lang="{language}">')
                self.assertContains(response, tagline)
                self.assertContains(response, f'<th scope="col">{title}</th>', html=True)
                self.assertContains(response, self.article.title)
                target_language = "fr" if language == "en" else "en"
                with translation.override(target_language):
                    target = reverse("articles")
                self.assertContains(response, f'href="{target}" lang="{target_language}"')
                self.assertEqual(response.headers["Content-Language"], language)
                self.assertContains(response, "Il y a" if language == "fr" else "ago")

    def test_french_logged_in_menu_translates_session_username_and_logout(self):
        self.login()
        with translation.override("fr"):
            response = self.client.get(reverse("articles"))
        self.assertContains(response, "Connecté en tant que alice")
        self.assertContains(response, "Déconnexion")
        self.assertContains(response, "Favoris")

    def test_menu_login_is_available_on_every_public_page_and_private_navigation_after_login(self):
        for name in ("articles", "login", "register", "detail"):
            with self.subTest(view=name):
                kwargs = {"pk": self.article.pk} if name == "detail" else None
                response = self.client.get(reverse(name, kwargs=kwargs))
                self.assertContains(response, 'name="menu-username"')
                self.assertContains(response, 'name="menu-password"')
        self.login()
        for name in ("articles", "favourites", "publications", "publish", "detail"):
            with self.subTest(view=name):
                kwargs = {"pk": self.article.pk} if name == "detail" else None
                response = self.client.get(reverse(name, kwargs=kwargs))
                self.assertContains(response, "Logged as alice")
                self.assertContains(response, reverse("logout"))
                self.assertNotContains(response, 'name="menu-password"')

    def test_required_actions_use_the_requested_generic_view_classes(self):
        for name, base in (("home", RedirectView), ("articles", ListView), ("publications", ListView), ("favourites", ListView), ("detail", DetailView), ("register", CreateView), ("publish", CreateView), ("add_favourite", CreateView)):
            with self.subTest(view=name):
                kwargs = {"pk": self.article.pk} if name in ("detail", "add_favourite") else None
                self.assertTrue(issubclass(resolve(reverse(name, kwargs=kwargs)).func.view_class, base))

