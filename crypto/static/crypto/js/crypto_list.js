const csrftoken = getCookie('csrftoken');
const table = document.getElementById("crypto-table");
const headers = table.querySelectorAll("thead th");
let sortDirection = {};


headers.forEach((header, index) => {
    header.style.cursor = "pointer";

    header.addEventListener("click", () => {
        const columnKey = header.getAttribute("data-column");
        const rows = Array.from(table.querySelectorAll("tbody tr"));

        const dir = sortDirection[index] === "asc" ? "desc" : "asc";
        sortDirection = {};
        sortDirection[index] = dir;

        headers.forEach(h => h.classList.remove("sorted-asc", "sorted-desc"));
        header.classList.add(dir === "asc" ? "sorted-asc" : "sorted-desc");

        rows.sort((a, b) => {
            let aVal, bVal;

            if (columnKey === "name") {
                aVal = a.querySelector(".crypto-name")?.innerText.trim().toLowerCase() || "";
                bVal = b.querySelector(".crypto-name")?.innerText.trim().toLowerCase() || "";
                return dir === "asc" ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
            } else {
                aVal = a.children[index].innerText.trim().replace(/[$,%MBK]/g, "");
                bVal = b.children[index].innerText.trim().replace(/[$,%MBK]/g, "");
                return dir === "asc"
                    ? parseFloat(aVal) - parseFloat(bVal)
                    : parseFloat(bVal) - parseFloat(aVal);
            }
        });

        const tbody = table.querySelector("tbody");
        rows.forEach(row => tbody.appendChild(row));
    });
});

const toggleBtn = document.getElementById('add-crypto-btn');
const formContainer = document.getElementById('crypto-form-container');

if (toggleBtn && formContainer) {
    toggleBtn.addEventListener('click', () => {
        formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
    });
}



function formatNumber(n) {
	if (n === null || n === undefined) return '-';
	if (n >= 1e9) return '$' + (n / 1e9).toFixed(2) + 'B';
	if (n >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
	if (n >= 1e3) return '$' + (n / 1e3).toFixed(2) + 'K';
	return '$' + parseFloat(n).toFixed(2);
}

const getCryptos = () => {
	const tableBody = document.querySelector('#crypto-table tbody');
	tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Loading...</td></tr>`;

	fetch('/api/cryptos/')
		.then(res => res.json())
		.then(data => {
			tableBody.innerHTML = '';

			if (data.cryptos.length === 0) {
				tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">No data available.</td></tr>`;
				return;
			}

			data.cryptos.forEach(c => {
				const tr = document.createElement('tr');
				tr.style.cursor = 'pointer';
				tr.onclick = () => window.location.href = `/cryptos/${c.id}/`;

				tr.innerHTML = `
					<td style="display:flex; align-items:center; gap:10px;">
						<img src="${c.logo || '/static/images/default-crypto.png'}" width="24" height="24" style="border-radius:50%; object-fit:contain;">
						<span class="crypto-name">${c.name} <small style="color:#888;">(${c.symbol})</small></span>
					</td>
					<td>${formatNumber(c.price)}</td>
					<td class="${c.change_24h > 0 ? 'green' : 'red'}">${formatNumber(c.change_24h)}%</td>
					<td>${formatNumber(c.market_cap)}</td>
					<td>${formatNumber(c.volume_24h)}</td>
				`;

				tableBody.appendChild(tr);
			});
		})
		.catch(err => {
			console.error('Failed to load cryptos:', err);
			tableBody.innerHTML = `<tr><td colspan="5" style="text-align:center;">Error loading data.</td></tr>`;
		});
};

getCryptos();

const form = document.getElementById('crypto-form');

form?.addEventListener('submit', (e) => {
	e.preventDefault();

	const formData = new FormData(form);

	fetch('/api/cryptos/add/', {
		method: 'POST',
		headers: {
			'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrftoken
		},
		body: formData
	})
	.then(res => res.json())
	.then(data => {
        const errorDiv = document.getElementById('form-error-message');
        errorDiv.textContent = data.error || 'Failed to add crypto.';

		if (data.success) {
			form.reset();
			document.getElementById('crypto-form-container').style.display = 'none';
			getCryptos();
		} else {
            errorDiv.textContent = data.error || 'Failed to add crypto.';
		}
	})
	.catch(err => {
		console.error('Error:', err);
		const errorDiv = document.getElementById('form-error-message');
	    errorDiv.textContent = 'An error occurred while submitting the form.';
	});
});
