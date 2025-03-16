document.addEventListener("scroll", function () {
    let navbar = document.getElementById("navbar");
    if (window.scrollY > 60) {
        navbar.classList.add("scrolled");
    } else {
        navbar.classList.remove("scrolled");
    }
});
