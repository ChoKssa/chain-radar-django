import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from crypto.models import CryptoCurrency, CryptoSnapshot

class Command(BaseCommand):
    # Help text shown when running the command with --help
    help = 'Import cryptos and historical snapshots from CSV files'

    def add_arguments(self, parser):
        # Define two required arguments: one for the cryptos CSV and one for the snapshots CSV
        parser.add_argument('--cryptos', type=str, required=True, help='Path to cryptos.csv')
        parser.add_argument('--snapshots', type=str, required=True, help='Path to snapshots.csv')

    def handle(self, *args, **options):
        crypto_count = 0
        snapshot_count = 0

        # === Import cryptos from the CSV file ===
        with open(options['cryptos'], newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Ensure symbol is uppercase and try to find or create the CryptoCurrency
                symbol = row['symbol'].upper()
                crypto, created = CryptoCurrency.objects.get_or_create(
                    symbol=symbol,
                    defaults={
                        'name': row['name'],
                        'description': row.get('description', '')  # Default to empty string if not provided
                    }
                )
                if created:
                    crypto_count += 1  # Count only newly created cryptos

        # Display the number of cryptos successfully imported
        self.stdout.write(self.style.SUCCESS(f"{crypto_count} cryptos imported."))

        # === Import historical snapshots from the CSV file ===
        with open(options['snapshots'], newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['symbol'].upper()
                try:
                    # Look up the CryptoCurrency object using the symbol
                    crypto = CryptoCurrency.objects.get(symbol=symbol)
                except CryptoCurrency.DoesNotExist:
                    # Skip this row if the crypto does not exist
                    self.stdout.write(self.style.WARNING(f"Unknown crypto symbol: {symbol}"))
                    continue

                try:
                    # Parse and localize the date string into a timezone-aware datetime
                    naive_dt = datetime.fromisoformat(row['date'])
                    timestamp = make_aware(naive_dt)
                except ValueError:
                    # Skip this row if the date format is invalid
                    self.stdout.write(self.style.WARNING(f"Invalid date format: {row['date']}"))
                    continue

                # Create a new CryptoSnapshot entry for the crypto
                CryptoSnapshot.objects.create(
                    crypto=crypto,
                    timestamp=timestamp,
                    price=row['price'],
                    change_24h=row['change_24h'],
                    market_cap = int(float(row['market_cap'])),
                    volume_24h=int(float(row['volume_24h'])),
                )
                snapshot_count += 1

        # Display the number of snapshots successfully imported
        self.stdout.write(self.style.SUCCESS(f"{snapshot_count} snapshots imported."))
