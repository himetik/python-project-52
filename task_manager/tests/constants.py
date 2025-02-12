from task_manager.labels.models import Label
from task_manager.tasks.models import Task


MAIN_USER = {
    'username': 'main_user',
    'first_name': 'main_user_firstname',
    'last_name': 'main_user_lastname',
    'password1': 'main_user_password',
    'password2': 'umain_user_password',
}

USER_1 = {
    'username': 'user_1',
    'first_name': 'user_1_firstname',
    'last_name': 'user_1_lastname',
    'password1': 'user_1_password',
    'password2': 'user_1_password',
}

USER_2 = {
    'username': 'user_2',
    'first_name': 'user_2_firstname',
    'last_name': 'user_2_lastname',
    'password1': 'user_2_password',
    'password2': 'user_2_password',
}

MAIN_TASK = "Main Task"
TASK_NAME_1 = "Task 1"
TASK_NAME_2 = "Task 2"
TASK_DESCRIPTION = "Task Description"

MAIN_STATUS = "Main Status"
STATUS_NAME_1 = "Status 1"
STATUS_NAME_2 = "Status 2"

MAIN_LABEL = 'Main Label'
LABEL_NAME_1 = 'Label 1'
LABEL_NAME_2 = 'Label 2'
LABEL_NAME_3 = "Label 3"
LABEL_NAME_4 = "Label 4"

LONG_TASK = "A" * (Task._meta.get_field("name").max_length + 1)
LONG_LABEL = "L" * (Label._meta.get_field("name").max_length + 1)
EMPTY_NAME = ""
WHITESPACED_LABEL_NAME_3 = "  Label 3  "
