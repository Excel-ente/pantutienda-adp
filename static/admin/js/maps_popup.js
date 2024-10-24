function openGoogleMapsPopup(inputId) {
    const mapsUrl = "https://www.google.com/maps/";
    const popup = window.open(mapsUrl, "popup", "width=800,height=600");

    popup.onunload = function () {
        const url = popup.location.href;
        if (url.includes("maps")) {
            // Guarda la URL en el campo correspondiente
            document.getElementById(inputId).value = url;
        }
    };
}
