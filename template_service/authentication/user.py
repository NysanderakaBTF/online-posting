from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

class CustomUser(AbstractBaseUser):
    def __init__(self, user_data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.id = user_data.get('id')
        self.email = user_data.get('email')
        self.name = user_data.get('name')
        self.is_admin = user_data.get('is_admin', False)
        self.is_staff = self.is_admin
        self.is_superuser = self.is_admin
        self.is_active = True
        self._is_authenticated = True

    @property
    def is_authenticated(self):
        return self._is_authenticated

    def is_anonymous(self):
        return False

    USERNAME_FIELD = 'email'