import shutil

from pathlib import Path

from django.conf import settings

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from houses.models import House, HouseFile


@receiver(pre_delete, sender=HouseFile)
def house_file_delete(sender: type[HouseFile], instance: HouseFile, **kwargs):
    instance.file.delete()


@receiver(pre_delete, sender=House)
def house_file_delete(sender: type[House], instance: House, **kwargs):
    media_root = Path(settings.MEDIA_ROOT)
    media_house_directory = media_root.joinpath('houses').joinpath(str(instance.pk))

    if media_house_directory.exists():
        shutil.rmtree(media_house_directory, ignore_errors=True)
