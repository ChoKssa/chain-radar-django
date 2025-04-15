from django.shortcuts import render, get_object_or_404
from .models import CryptoCurrency, CryptoSnapshot, FollowedCrypto
from django.db.models import Max, OuterRef, Subquery
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.http import JsonResponse

# View to render the crypto list page
def crypto_list(request):
    return render(request, 'crypto/crypto_list.html')

# JSON endpoint that returns the latest snapshot data for all cryptos
def crypto_list_json(request):
    # Prepare a subquery to get the latest snapshot per cryptocurrency
    latest_snapshot = CryptoSnapshot.objects.filter(crypto=OuterRef('pk')).order_by('-timestamp')

    # Annotate each cryptocurrency with its latest snapshot values
    cryptos = CryptoCurrency.objects.annotate(
        latest_price=Subquery(latest_snapshot.values('price')[:1]),
        latest_change=Subquery(latest_snapshot.values('change_24h')[:1]),
        latest_marketcap=Subquery(latest_snapshot.values('market_cap')[:1]),
        latest_volume=Subquery(latest_snapshot.values('volume_24h')[:1]),
        latest_snapshot_id=Subquery(latest_snapshot.values('id')[:1]),
    )

    # Serialize the annotated data to JSON
    data = [
        {
            "id": c.pk,
            "name": c.name,
            "symbol": c.symbol,
            "logo": c.logo.url if c.logo else None,
            "price": float(c.latest_price) if c.latest_price else None,
            "change_24h": float(c.latest_change) if c.latest_change else None,
            "market_cap": c.latest_marketcap if c.latest_marketcap else None,
            "volume_24h": c.latest_volume if c.latest_volume else None,
        }
        for c in cryptos
    ]

    return JsonResponse({"cryptos": data})

# View restricted to staff users to add a new cryptocurrency via POST
@user_passes_test(lambda u: u.is_staff)
def add_crypto(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        symbol = request.POST.get('symbol')
        description = request.POST.get('description')
        logo = request.FILES.get('logo')

        # Validate required fields
        if not name.strip() or not symbol.strip():
            return JsonResponse({
                'success': False,
                'error': 'Name and symbol are required.'
            })

        # Create the new cryptocurrency entry
        crypto = CryptoCurrency.objects.create(
            name=name,
            symbol=symbol.upper(),
            description=description,
            logo=logo
        )

        # Return JSON response if it's an AJAX request
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'crypto_id': crypto.pk
            })

        return redirect('crypto_list')
    return redirect('crypto_list')

# View showing detailed data and chart for a single crypto
def crypto_detail(request, pk):
    crypto = get_object_or_404(CryptoCurrency, pk=pk)
    snapshots = CryptoSnapshot.objects.filter(crypto=crypto).order_by('timestamp')

    # Prepare data for chart rendering
    chart_dates = [snap.timestamp.strftime('%Y-%m-%d') for snap in snapshots]
    chart_prices = [float(snap.price) for snap in snapshots]

    latest_snapshot = snapshots.last()

    # Check if the current user follows this crypto
    is_followed = False
    if request.user.is_authenticated:
        is_followed = FollowedCrypto.objects.filter(user=request.user, crypto=crypto).exists()

    return render(request, 'crypto/crypto_detail.html', {
        'crypto': crypto,
        'price': latest_snapshot.price if latest_snapshot else 0,
        'change_24h': latest_snapshot.change_24h if latest_snapshot else 0,
        'market_cap': latest_snapshot.market_cap if latest_snapshot else 0,
        'volume_24h': latest_snapshot.volume_24h if latest_snapshot else 0,
        'chart_dates': chart_dates,
        'chart_prices': chart_prices,
        'is_followed': is_followed,
    })

# View to compare two cryptocurrencies side-by-side
def crypto_comparator(request):
    cryptos = CryptoCurrency.objects.all()

    crypto1 = crypto2 = snapshot1 = snapshot2 = None
    error_message = None

    if request.method == 'GET':
        id1 = request.GET.get('crypto1')
        id2 = request.GET.get('crypto2')

        if id1 and id2:
            try:
                crypto1 = CryptoCurrency.objects.get(pk=id1)
                crypto2 = CryptoCurrency.objects.get(pk=id2)

                print(f"Selected cryptocurrencies: {crypto1.name} and {crypto2.name}")

                # Get latest snapshots for each crypto
                latest_id_1 = CryptoSnapshot.objects.filter(crypto=crypto1).aggregate(Max('id'))['id__max']
                latest_id_2 = CryptoSnapshot.objects.filter(crypto=crypto2).aggregate(Max('id'))['id__max']

                snapshot1 = CryptoSnapshot.objects.get(id=latest_id_1) if latest_id_1 else None
                snapshot2 = CryptoSnapshot.objects.get(id=latest_id_2) if latest_id_2 else None
            except CryptoCurrency.DoesNotExist:
                error_message = "One or both selected cryptocurrencies do not exist."

    return render(request, 'crypto/crypto_comparator.html', {
        'cryptos': cryptos,
        'crypto1': crypto1,
        'crypto2': crypto2,
        'snapshot1': snapshot1,
        'snapshot2': snapshot2,
        'error_message': error_message,
    })
