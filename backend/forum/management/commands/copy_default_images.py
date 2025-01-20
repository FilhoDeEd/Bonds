import os
from shutil import copy
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Moves the images directory to MEDIA_ROOT/default_forum_images/'

    def handle(self, *args, **kwargs):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        source_dir = os.path.join(current_directory, 'images/')
        
        destination_dir = os.path.join(settings.MEDIA_ROOT, 'default_forum_images')

        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        if os.path.exists(source_dir):
            try:
                for filename in os.listdir(source_dir):
                    source_file = os.path.join(source_dir, filename)
                    destination_file = os.path.join(destination_dir, filename)

                    copy(source_file, destination_file)

                self.stdout.write(self.style.SUCCESS(f"All images have been moved to {destination_dir}."))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error moving images: {e}"))
        else:
            self.stdout.write(self.style.WARNING(f"Source directory 'images' not found."))
