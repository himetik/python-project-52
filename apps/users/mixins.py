from django.contrib.auth import get_user_model


class SetUpLoggedUserMixin:
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='password123'
        )
        login_successful = self.client.login(
            username='testuser',
            password='password123'
        )
        if not login_successful:
            raise Exception("Failed to log in test user")
        super().setUp() if hasattr(super(), 'setUp') else None
