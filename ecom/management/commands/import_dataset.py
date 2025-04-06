import csv
from django.core.management.base import BaseCommand
from ecom.models import Product

class Command(BaseCommand):
    help = 'Import products from a CSV dataset'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_file',
            type=str,
            help='The path to the CSV file to import'
        )

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        try:
            with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    product, created = Product.objects.get_or_create(
                        uid=row['UID'],
                        defaults={
                            'name': row['NAME'],
                            'model': row['MODEL'],
                            'description': row['DESCRIPTION'],
                            'price': row['PRICE'],
                            'brand': row['BRAND'],
                            'size': row['SIZE'],
                            'age_group': row['Age Group'],
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Created product: {product.name}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Product {product.name} already exists."))
            self.stdout.write(self.style.SUCCESS("Dataset import complete."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error importing dataset: {e}"))