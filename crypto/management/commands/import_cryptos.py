import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from django.utils.timezone import make_aware
from crypto.models import CryptoCurrency, CryptoSnapshot

class Command(BaseCommand):
    help = 'Import cryptos and historical snapshots from CSV files'

    def add_arguments(self, parser):
        parser.add_argument('--cryptos', type=str, required=True, help='Path to cryptos.csv')
        parser.add_argument('--snapshots', type=str, required=True, help='Path to snapshots.csv')

    def handle(self, *args, **options):
        crypto_count = 0
        snapshot_count = 0

        # === Import cryptos ===
        with open(options['cryptos'], newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['symbol'].upper()
                crypto, created = CryptoCurrency.objects.get_or_create(
                    symbol=symbol,
                    defaults={
                        'name': row['name'],
                        'description': row.get('description', '')
                    }
                )
                if created:
                    crypto_count += 1

        self.stdout.write(self.style.SUCCESS(f"{crypto_count} cryptos imported."))

        # === Import snapshots ===
        with open(options['snapshots'], newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row['symbol'].upper()
                try:
                    crypto = CryptoCurrency.objects.get(symbol=symbol)
                except CryptoCurrency.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Unknown crypto symbol: {symbol}"))
                    continue

                try:
                    naive_dt = datetime.fromisoformat(row['date'])
                    timestamp = make_aware(naive_dt)
                except ValueError:
                    self.stdout.write(self.style.WARNING(f"Invalid date format: {row['date']}"))
                    continue

                CryptoSnapshot.objects.create(
                    crypto=crypto,
                    timestamp=timestamp,
                    price=row['price'],
                    change_24h=row['change_24h'],
                    market_cap = int(float(row['market_cap'])),
                    volume_24h=int(float(row['volume_24h'])),
                )
                snapshot_count += 1

        self.stdout.write(self.style.SUCCESS(f"{snapshot_count} snapshots imported."))
