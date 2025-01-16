from django.core.management.base import BaseCommand, CommandParser
from forum.models import Forum
from user_profile.models import Neighborhood
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
        if limit:
            neighborhoods = Neighborhood.objects.all()[:limit]
        else:
            neighborhoods = Neighborhood.objects.all()
        for neighborhood in neighborhoods:
            try:
                forum_titles = [
                    f'Notícias e Atualizações Locais',
                    f'Comércio Local',
                    f'Segurança e Emergências',
                    f'Transporte e Trânsito',
                    f'Vagas e Empregos Locais'
                ]
                for title in forum_titles:
                    Forum.objects.create(
                        title=title,
                        description=f'Forum about {title}',
                        neighborhood=neighborhood,
                        type = Forum.TypeChoices.DEFAULT,
                    )
                self.stdout.write(self.style.SUCCESS(f"Forums created for neighborhood {neighborhood.name}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating forums for neighborhood {neighborhood.name}: {e}"))