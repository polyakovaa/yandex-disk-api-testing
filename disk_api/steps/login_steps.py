from pages.login_page import LoginPage


class LoginSteps:
    def __init__(self, login_page: LoginPage):
        self.__login_page = login_page

    def fill_login_form(self, email: str, password: str):
        self.__login_page.fill_email(email)
        self.__login_page.click_next()
        self.__login_page.fill_password(password)
        self.__login_page.click_next()
        self.__login_page.click_remind_later()
