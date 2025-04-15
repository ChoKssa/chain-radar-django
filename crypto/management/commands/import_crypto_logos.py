import os
from django.core.management.base import BaseCommand, CommandError
from django.core.files import File
from crypto.models import CryptoCurrency

class Command(BaseCommand):
    # Help text shown when running the command with --help
    help = 'Import crypto logos from a specified folder'

    def add_arguments(self, parser):
        # Define one required argument for the folder containing the logo images
        parser.add_argument('folder_path', type=str, help='Path to the folder containing the crypto logos')

    def handle(self, *args, **options):
        folder = options['folder_path']

        # Check if the specified folder exists
        if not os.path.isdir(folder):
            raise CommandError(f"❌ Directory'{folder}' does not exist.")

        imported = 0

        # Iterate over all cryptocurrencies in the database
        for crypto in CryptoCurrency.objects.all():
            # Build the expected filename for the logo based on the symbol
            logo_filename = f"{crypto.symbol.upper()}.png"
            logo_path = os.path.join(folder, logo_filename)

            # Check if the logo image file exists in the folder
            if os.path.exists(logo_path):
                # Open the image file and assign it to the crypto's logo field
                with open(logo_path, 'rb') as f:
                    crypto.logo.save(logo_filename, File(f), save=True)
                self.stdout.write(self.style.SUCCESS(f"✅ Log added for {crypto.name}"))
                imported += 1
            else:
                # If no image file is found, print a warning message
                self.stdout.write(self.style.WARNING(f"⚠️  No image foud for {crypto.symbol}"))

        # Final summary of the number of logos imported
        self.stdout.write(self.style.SUCCESS(f"\nImport finished. {imported} logos added."))
