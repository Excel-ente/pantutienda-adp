// custom_admin.js
document.addEventListener('DOMContentLoaded', () => {
    const modal = document.getElementById('custom-confirm');
    const confirmBtn = document.getElementById('confirm-btn');
    const cancelBtn = document.getElementById('cancel-btn');
    const closeBtn = modal.querySelector('.close');

    // Mostrar el popup sin abrir nuevas ventanas
    window.showCustomConfirm = (url) => {
        modal.classList.add('show');
        confirmBtn.onclick = () => {
            window.location.href = url;  // Redirige para confirmar la compra
        };
    };

    // Función para cerrar el modal
    const closeModal = () => modal.classList.remove('show');

    // Cerrar modal al hacer clic en los botones o fuera del contenido
    cancelBtn.onclick = closeModal;
    closeBtn.onclick = closeModal;
    window.onclick = (event) => {
        if (event.target === modal) closeModal();
    };
});
