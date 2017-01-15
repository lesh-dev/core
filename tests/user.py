import random_crap as rc


class User(object):

    xtest = None
    login = None
    email = None
    password = None
    name = None

    def __init__(self, xtest):
        self.xtest = xtest
        self.aux_params = list()

    def create_new_user(
        self,
        login=str(),
        email=str(),
        password=str(),
        name=str(),
        random=False,
        validate=True,
        manager_rights=False,
        login_as_admin=True,
        logout_admin=True,
    ):
        if random:
            login += "_" + rc.random_text(6)
            email += "_" + rc.randomEmail()
            password += "_" + rc.random_text(6)
            name += "_" + rc.random_text(6)

        if not validate:
            self.aux_params.append("do_not_validate")
        if manager_rights:
            self.aux_params.append("manager_rights")
        if not login_as_admin:
            self.aux_params.append("do_not_login_as_admin")
        if not logout_admin:
            self.aux_params.append("do_not_logout_admin")
        self.login, self.email, self.password, self.name = self.xtest.createNewUser(login, email, password, name, self.aux_params)

        return self.login, self.email, self.password, self.name
