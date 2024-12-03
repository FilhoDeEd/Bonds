from django.core.management.base import BaseCommand
import pandas as pd
import os
from user_profile.models import Neighborhood

states = [
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG', 'PA', 
    'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
]

class Command(BaseCommand):
    help = 'Import data from an Excel file into the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--limit', type=int, help='Limit the number of neighborhoods to import'
        )

    def handle(self, *args, **kwargs):
        limit = kwargs.get('limit')  # Se não passar o limite, fica como None

        current_directory = os.path.dirname(os.path.abspath(__file__))
        excel_file = os.path.join(current_directory, 'neighborhoods.xlsx')

        if not os.path.exists(excel_file):
            self.stdout.write(self.style.ERROR(f"File '{excel_file}' not found."))
            return

        try:
            data = pd.read_excel(excel_file)

            required_columns = {'bairro', 'cidade', 'estado'}
            if not required_columns.issubset(data.columns):
                raise ValueError(f"The Excel file must contain the following columns: {required_columns}")

            count = 0  # Contador para os bairros
            for _, row in data.iterrows():
                if limit is not None and count >= limit:
                    break  # Se um limite foi definido, interrompe o loop

                try:
                    if row['estado'] not in states:
                        self.stdout.write(f"State '{row['estado']}' does not match the list of Federative Units.")
                    else:
                        Neighborhood.objects.create(
                            name=row['bairro'],
                            locality=row['cidade'],
                            state=row['estado'],
                        )
                        count += 1
                        self.stdout.write(f"Neighborhood '{row['bairro']}' | State '{row['estado']}' | City '{row['cidade']}' added.")
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error with neighborhood '{row['bairro']}': {e}"))
                    continue

            self.stdout.write(self.style.SUCCESS(f'Data imported successfully! {count} neighborhoods added.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error importing data: {e}"))
