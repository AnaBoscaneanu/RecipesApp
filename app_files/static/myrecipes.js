// Disable the search button if nothing is typed

document.getElementById("search-ingr").onkeyup = function() {
    const search = document.getElementById("search-button");
    if (this.value === "") {
        search.disabled = true;
    } else {
        search.disabled = false;
    }
}