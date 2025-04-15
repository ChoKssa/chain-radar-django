/**
 * Retrieves the value of a specific cookie by name.
 * Commonly used to extract the CSRF token stored in cookies.
 *
 * @param {string} name - The name of the cookie to retrieve.
 * @returns {string|null} - The cookie value, or null if not found.
 */
function getCookie(name) {
	let cookieValue = null;

	// Check if any cookies are present
	if (document.cookie && document.cookie !== '') {
		const cookies = document.cookie.split(';');

		for (let i = 0; i < cookies.length; i++) {
			const cookie = cookies[i].trim();

			// Check if this cookie matches the desired name
			if (cookie.substring(0, name.length + 1) === (name + '=')) {
				// Decode and return the cookie value
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}

	return cookieValue;
}
