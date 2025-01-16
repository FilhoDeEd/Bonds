from django.utils.text import slugify
from django.utils.timezone import now
from django.core.management.base import BaseCommand, CommandParser
from forum.models import Forum
from user_profile.models import Neighborhood
from django.db import transaction

class Command(BaseCommand):
    help = 'Creates default forums for each neighborhood.'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument(
            '--limit', 
            type=int, 
            help='Limit the number of neighborhoods to process (optional)',
        )

    def handle(self, *args, **kwargs):
        limit = kwargs.get('limit')

        neighborhoods = Neighborhood.objects.all()
        if limit:
            neighborhoods = neighborhoods[:limit]

        forum_titles = [
            'Notícias e Atualizações Locais',
            'Comércio Local',
            'Segurança e Emergências',
            'Transporte e Trânsito',
            'Vagas e Empregos Locais'
        ]

        forums_to_create = []

        counter = 1
        for neighborhood in neighborhoods:
            for title in forum_titles:
                base_slug = slugify(title)
                slug = base_slug

                slug = f'{base_slug}-{counter}'

                forums_to_create.append(Forum(
                    title=title,
                    description=f'Forum about {title}',
                    neighborhood=neighborhood,
                    type=Forum.TypeChoices.DEFAULT,
                    creation_date=now(),
                    update_date=now(),
                    slug=slug
                ))

            counter += 1

        try:
            with transaction.atomic():
                Forum.objects.bulk_create(forums_to_create)
            self.stdout.write(self.style.SUCCESS("Forums created successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating forums: {e}"))
