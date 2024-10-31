document.addEventListener('DOMContentLoaded', () => {
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const closeButtons = document.querySelectorAll('.modal .close');
    const openRegisterModal = document.getElementById('openRegisterModal');
    const openLoginModal = document.getElementById('openLoginModal');

    openRegisterModal.addEventListener('click', (e) => {
        e.preventDefault();
        loginModal.classList.remove('show');
        registerModal.classList.add('show');
    });

    // Volver al login desde el modal de registro

    openLoginModal.addEventListener('click', function() {
        registerModal.classList.remove('show');
        loginModal.classList.add('show');
    });

    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            loginModal.classList.remove('show');
            registerModal.classList.remove('show');
        });
    });
/*
    window.addEventListener('click', (event) => {
        if (event.target === loginModal) {
            loginModal.classList.remove('show');
        }
        if (event.target === registerModal) {
            registerModal.classList.remove('show');
        }
    });*/
});