import uuid
from datetime import datetime
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models.query import QuerySet
from model_utils.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class CustomUserManager(BaseUserManager):

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        """
                Create and save a user with the given username, email, and password.
                """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractUser, TimeStampedModel):
    guid = models.UUIDField(default=uuid.uuid4, unique=True)
    username = None
    email = models.EmailField(_('email address'), unique=True)
    contact_number = models.CharField(max_length=20, null=True)
    minimum_download = models.IntegerField(null=True)
    deleted_at = models.DateTimeField(blank=True, null=True, default=None)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        db_table = "account_users"

    def __str__(self):
        return '%s %s' % (self.first_name, self.last_name)

    @property
    def full_name(self):
        """Returns the person's full name."""
        return '%s %s' % (self.first_name, self.last_name)


class SoftDeletionQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeletionQuerySet, self).update(deleted_at=datetime.now())

    def hard_delete(self):
        return super(SoftDeletionQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)


class SoftDeletionManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeletionManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeletionQuerySet(self.model).filter(deleted_at=None)
        return SoftDeletionQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()


class SoftDeletionModel(models.Model):
    deleted_at = models.DateTimeField(blank=True, null=True)

    objects = SoftDeletionManager()
    all_objects = SoftDeletionManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = datetime.now()
        self.save()

    def hard_delete(self):
        super(SoftDeletionModel, self).delete()
