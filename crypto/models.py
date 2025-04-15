from django.conf import settings
from django.db import models

# Model representing a cryptocurrency
class CryptoCurrency(models.Model):
    name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='crypto_logos/', null=True, blank=True)

    def __str__(self):
        # Human-readable representation for admin and shell
        return f"{self.name} ({self.symbol.upper()})"

# Model representing a snapshot of a crypto's state at a given time
class CryptoSnapshot(models.Model):
    crypto = models.ForeignKey(CryptoCurrency, on_delete=models.CASCADE, related_name='snapshots')
    timestamp = models.DateTimeField()
    price = models.DecimalField(max_digits=20, decimal_places=8)
    market_cap = models.BigIntegerField()
    volume_24h = models.BigIntegerField()
    change_24h = models.FloatField(help_text="Pourcentage de variation sur 24h")

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        # Human-readable representation
        return f"{self.crypto.symbol} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"

# Model representing a user's followed cryptocurrencies
class FollowedCrypto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="followed_cryptos")
    crypto = models.ForeignKey('CryptoCurrency', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'crypto')

    def __str__(self):
        # Human-readable representation
        return f"{self.user.username} → {self.crypto.symbol}"
