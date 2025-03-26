/* ----------------------------
MENU TOGGLE FUNCTIONALITY
---------------------------- */
const menu = document.getElementById("menu"); // Get the menu element
const menuButton = document.getElementById("menu-button"); // Get the button that toggles the menu
const body = document.querySelector("body"); // Reference to the body element

// Function to toggle the menu's visibility
function toggleMenu() {
    if (menu.classList.contains("menu-open")) {
        // If menu is open, close it
        menu.classList.remove("menu-open");
        menu.classList.add("menu-close");
    } else {
        // If menu is closed, open it
        menu.classList.remove("menu-close");
        menu.classList.add("menu-open");
    }
}

/* ----------------------------
    CLOSE MENU WHEN CLICKING OUTSIDE
    ---------------------------- */
body.addEventListener("click", (event) => {
    // Close the menu if the user clicks anywhere outside the menu button
    if (event.target !== menuButton) {
        if (menu.classList.contains("menu-open")) {
            menu.classList.remove("menu-open");
            menu.classList.add("menu-close");
        }
    }
});

// Attach event listener to menu button to toggle menu when clicked
menuButton.addEventListener("click", toggleMenu);

/* ----------------------------
    ADJUST MENU POSITION ON SCROLL
    ---------------------------- */
window.addEventListener("scroll", () => {
    const header = document.querySelector("header"); // Get the header element
    const headerBottom = header.getBoundingClientRect().bottom; // Get the bottom position of the header

    if (menu.classList.contains("menu-open")) {
        if (headerBottom <= 0) {
            // If the header is completely out of view, move menu with the scroll position
            menu.style.top = `${window.scrollY}px`;
        } else {
            // Keep menu positioned just below the header
            menu.style.top = "50px";
        }
    } else {
        // Ensure menu remains in its default position when closed
        menu.style.top = "50px";
    }
});
