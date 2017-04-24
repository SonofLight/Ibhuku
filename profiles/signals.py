#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from PIL import Image, ImageOps
from io import StringIO, BytesIO

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from users.models import User
from profiles.models import Profile, ProfileAvatar


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


@receiver(post_save, sender=Profile)
def create_profile_avatar(sender, instance, created, **kwargs):
    if created:
        ProfileAvatar.objects.create(profile=instance)


@receiver(post_save, sender=Profile)
def save_profile_avatar(sender, instance, **kwargs):
    instance.profileavatar.save()


@receiver(post_save, sender=ProfileAvatar)
def profile_upload_delete_previous_file(sender, instance, **kwargs):
    profile = instance.avatar.name.split('/')[-1]
    if profile in getattr(instance.avatar, 'name'):
        pass
