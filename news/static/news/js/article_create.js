// Get references to key DOM elements
const container = document.getElementById("paragraphs-container");
const addButton = document.getElementById("add-paragraph");
const totalForms = document.getElementById("id_paragraph_set-TOTAL_FORMS");
const templateHtml = document.getElementById("empty-form-template").innerHTML;

// Handle dynamic addition of a new paragraph form
addButton.addEventListener("click", () => {
    const index = parseInt(totalForms.value); // Current total form count
    const newForm = templateHtml.replace(/__prefix__/g, index); // Replace placeholder with current index
    container.insertAdjacentHTML("beforeend", newForm); // Append the new form to the container
    totalForms.value = index + 1; // Update the total form count
});

// Handle removal of a paragraph form
container.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-paragraph")) {
        const group = e.target.closest(".paragraph-group");

        // Find the DELETE checkbox (used when editing existing forms)
        const deleteInput = group.querySelector('input[type="checkbox"][name*="-DELETE"]');

        if (deleteInput) {
            // Mark the form for deletion and hide it visually
            deleteInput.checked = true;
            group.style.display = "none";
        } else {
            // If it's a newly added form, just remove it from the DOM
            group.remove();
        }
    }
});
