from app.users.components.login import LoginForm
from app.users.components.db_info import DBInfoForm


class LoginView:
    def __init__(self):
        self.login_form = LoginForm()
        self.db_info_form = DBInfoForm()

    def render(self):
        self.login_form.render()
        self.db_info_form.render()
