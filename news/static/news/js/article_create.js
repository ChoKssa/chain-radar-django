const container = document.getElementById("paragraphs-container");
const addButton = document.getElementById("add-paragraph");
const totalForms = document.getElementById("id_paragraph_set-TOTAL_FORMS");
const templateHtml = document.getElementById("empty-form-template").innerHTML;

addButton.addEventListener("click", () => {
    const index = parseInt(totalForms.value);
    const newForm = templateHtml.replace(/__prefix__/g, index);
    container.insertAdjacentHTML("beforeend", newForm);
    totalForms.value = index + 1;
});

container.addEventListener("click", (e) => {
    if (e.target.classList.contains("remove-paragraph")) {
        const group = e.target.closest(".paragraph-group");

        const deleteInput = group.querySelector('input[type="checkbox"][name*="-DELETE"]');

        if (deleteInput) {
            deleteInput.checked = true;
            group.style.display = "none";
        } else {
            group.remove();
        }
    }
}
);
