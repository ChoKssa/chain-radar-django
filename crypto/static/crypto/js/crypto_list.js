// Get CSRF token from cookie for secure POST requests
const csrftoken = getCookie('csrftoken');

// Get the crypto table and header cells
const table = document.getElementById("crypto-table");
const headers = table.querySelectorAll("thead th");
let sortDirection = {};

// Add sorting behavior to table headers
headers.forEach((header, index) => {
    header.style.cursor = "pointer";

    header.addEventListener("click", () => {
        const columnKey = header.getAttribute("data-column");
        const rows = Array.from(table.querySelectorAll("tbody tr"));

        // Toggle sort direction for clicked column
        const dir = sortDirection[index] === "asc" ? "desc" : "asc";
        sortDirection = {};
        sortDirection[index] = dir;

        // Reset sort indicators
        headers.forEach(h => h.classList.remove("sorted-asc", "sorted-desc"));
        header.classList.add(dir === "asc" ? "sorted-asc" : "sorted-desc");

        // Sort rows by selected column
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

        // Re-attach sorted rows
        const tbody = table.querySelector("tbody");
        rows.forEach(row => tbody.appendChild(row));
    });
});

// Toggle visibility of the crypto creation form
const toggleBtn = document.getElementById('add-crypto-btn');
const formContainer = document.getElementById('crypto-form-container');

if (toggleBtn && formContainer) {
    toggleBtn.addEventListener('click', () => {
        formContainer.style.display = formContainer.style.display === 'none' ? 'block' : 'none';
    });
}

// Format numbers into currency with suffixes
function formatNumber(n) {
	if (n === null || n === undefined) return '-';
	if (n >= 1e9) return '$' + (n / 1e9).toFixed(2) + 'B';
	if (n >= 1e6) return '$' + (n / 1e6).toFixed(2) + 'M';
	if (n >= 1e3) return '$' + (n / 1e3).toFixed(2) + 'K';
	return '$' + parseFloat(n).toFixed(2);
}

// Fetch crypto data from the API and update the table
function getCryptos() {
	const tableBody = $('#crypto-table tbody');
	tableBody.html('<tr><td colspan="5" style="text-align:center;">Loading...</td></tr>');

	$.ajax({
		type: "GET",
		url: "/api/cryptos/",
		dataType: "json",
		success: function(data) {
			tableBody.empty();

			if (data.cryptos.length === 0) {
				tableBody.html('<tr><td colspan="5" style="text-align:center;">No data available.</td></tr>');
				return;
			}

			// Build each row from the data
			data.cryptos.forEach(c => {
				const row = `
					<tr style="cursor:pointer;" onclick="window.location.href='/cryptos/${c.id}/'">
						<td style="display:flex; align-items:center; gap:10px;">
							<img src="${c.logo || '/static/images/default-crypto.png'}" width="24" height="24" style="border-radius:50%; object-fit:contain;">
							<span class="crypto-name">${c.name} <small style="color:#888;">(${c.symbol})</small></span>
						</td>
						<td>${formatNumber(c.price)}</td>
						<td class="${c.change_24h > 0 ? 'green' : 'red'}">${formatNumber(c.change_24h)}%</td>
						<td>${formatNumber(c.market_cap)}</td>
						<td>${formatNumber(c.volume_24h)}</td>
					</tr>
				`;
				tableBody.append(row);
			});
		},
		error: function() {
			tableBody.html('<tr><td colspan="5" style="text-align:center;">Error loading data.</td></tr>');
		}
	});
}

// Validate form input before submission
function validateCryptoForm(formData) {
	const name = formData.get("name")?.trim();
	const symbol = formData.get("symbol")?.trim();
	const errorDiv = document.getElementById('form-error-message');
	errorDiv.textContent = '';

	if (!name || name.length < 2) {
		errorDiv.textContent = 'Name must be at least 2 characters long.';
		return false;
	}

	if (!symbol || symbol.length < 2 || symbol.length > 10) {
		errorDiv.textContent = 'Symbol must be between 2 and 10 characters.';
		return false;
	}

	const logo = formData.get("logo");
	if (logo && logo.size > 0) {
		const allowedTypes = ["image/png", "image/jpeg", "image/webp"];
		if (!allowedTypes.includes(logo.type)) {
			errorDiv.textContent = 'Logo must be a PNG, JPEG or WEBP image.';
			return false;
		}
	}

	return true;
}

// Submit the form via AJAX to add a new crypto
function addCrypto(formData) {
	$.ajax({
		url: '/api/cryptos/add/',
		type: 'POST',
		headers: { 'X-CSRFToken': csrftoken },
		data: formData,
		processData: false,
		contentType: false,
		success: function(data) {
			const errorDiv = $('#form-error-message');
			if (data.success) {
				$('#crypto-form')[0].reset();
				$('#crypto-form-container').hide();
				getCryptos();
			} else {
				errorDiv.text(data.error || 'Failed to add crypto.');
			}
		},
		error: function(xhr) {
			console.error('Error:', xhr);
			$('#form-error-message').text('An error occurred while submitting the form.');
		}
	});
}

// On page load: fetch data and set up form submission
$(document).ready(() => {
	getCryptos();

	const $form = $('#crypto-form');

	$form.on('submit', function (e) {
		e.preventDefault();

		const formData = new FormData(this);

		if (!validateCryptoForm(formData)) {
			return;
		}

		addCrypto(formData);
	});
});
