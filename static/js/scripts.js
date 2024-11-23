// Evitar que el dropdown de marcas se cierre automáticamente
document.getElementById('makes-list').addEventListener('click', function (event) {
    event.stopPropagation(); // Evita que el evento cierre el dropdown
});
