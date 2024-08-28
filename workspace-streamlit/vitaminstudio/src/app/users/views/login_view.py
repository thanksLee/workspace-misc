from users.components.login_form import LoginForm
from users.components.db_info_form import DBInfoForm


class LoginView:
    def __init__(self):
        self.login_form = LoginForm()
        self.db_info_form = DBInfoForm()

    def render(self):
        self.login_form.render()
        self.db_info_form.render()
