from django.contrib.auth import get_user_model


def get_full_user_name(self):
    return f'{self.first_name} {self.last_name}'


get_user_model().add_to_class('__str__', get_full_user_name)
