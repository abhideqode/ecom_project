"""
    this is the Customer USER MANAGER File
"""
from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    """
        this is the Customer User manager
    """
    use_in_migrations: True

    def create_user(self, email, password=None, **extra_fields):
        """
            this is the create super user functions
        """
        if not email:
            raise ValueError('required')
        email = self.normalize_email(email)
        print('create_user')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
            this is the create super user functions
        """
        # import pdb;
        # pdb.set_trace()
        # user = self.model(email=email, **extra_fields)
        # user.user_type = "admin"

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('user_type', 'admin')
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        print('create_superuser')
        return self.create_user(email, password, **extra_fields,)

    def create_suser(self, email, password=None, **extra_fields):
        """
            this is the create shop user functions
        """
        if not email:
            raise ValueError('required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        print('create_suser')
        user.save(using=self._db)
        return user

    def create_shopuser(self, email, password=None, **extra_fields):
        """
            this is the create shop user functions
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', False)
        extra_fields.setdefault('is_superuser', True)
        print('create_shopuser')
        return self.create_suser(email, password, **extra_fields)
