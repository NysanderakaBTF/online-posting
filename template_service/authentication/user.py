class CustomUser:
    def __init__(self, user_data):
        self.id = user_data.get('pk')
        self.email = user_data.get('email')
        self.name = user_data.get('name')
        self.is_admin = user_data.get('is_admin', False)
        self.is_staff = self.is_admin
        self.is_superuser = self.is_admin
        self.is_active = True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name