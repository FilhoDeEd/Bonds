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

        # Retrieve the neighborhoods with an optional limit
        neighborhoods = Neighborhood.objects.all()
        if limit:
            neighborhoods = neighborhoods[:limit]

        # Prepare default forum titles in advance
        forum_titles = [
            'Notícias e Atualizações Locais',
            'Comércio Local',
            'Segurança e Emergências',
            'Transporte e Trânsito',
            'Vagas e Empregos Locais'
        ]

        forums_to_create = []  # Batch creation to reduce database hits

        for neighborhood in neighborhoods:
            for title in forum_titles:
                forums_to_create.append(Forum(
                    title=title,
                    description=f'Forum about {title}',
                    neighborhood=neighborhood,
                    type=Forum.TypeChoices.DEFAULT,
                ))

        try:
            with transaction.atomic():
                # Use bulk_create to minimize database access
                Forum.objects.bulk_create(forums_to_create)
            self.stdout.write(self.style.SUCCESS("Forums created successfully."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error creating forums: {e}"))
