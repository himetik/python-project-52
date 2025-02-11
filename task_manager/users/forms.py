from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'username')


class CustomUserChangeForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields

    def clean_username(self):
        return self.cleaned_data.get('username')
