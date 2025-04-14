import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from crypto.models import CryptoCurrency

class Command(BaseCommand):
    help = 'Import crypto logos from a specified folder'

    def add_arguments(self, parser):
        parser.add_argument('folder_path', type=str, help='Path to the folder containing the crypto logos')

    def handle(self, *args, **options):
        folder = options['folder_path']

        if not os.path.isdir(folder):
            raise CommandError(f"❌ Directory'{folder}' does not exist.")

        imported = 0
        for crypto in CryptoCurrency.objects.all():
            logo_filename = f"{crypto.symbol.upper()}.png"
            logo_path = os.path.join(folder, logo_filename)

            if os.path.exists(logo_path):
                with open(logo_path, 'rb') as f:
                    crypto.logo.save(logo_filename, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"✅ Log added for {crypto.name}"))
                imported += 1
            else:
                self.stdout.write(self.style.WARNING(f"⚠️  No image foud for {crypto.symbol}"))

        self.stdout.write(self.style.SUCCESS(f"\nImport finished. {imported} logos added."))
