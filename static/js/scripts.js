document.addEventListener('DOMContentLoaded', () => {
    const modals = {
        login: document.getElementById('loginModal'),
        register: document.getElementById('registerModal'),
        profile: document.getElementById('profileModal'),
        pedidos: document.getElementById('pedidosModal')
    };

    const buttons = {
        login: document.getElementById('loginButton'),
        register: document.getElementById('registerButton'),
        profile: document.getElementById('profileButton'),
        pedidos: document.getElementById('pedidosButton')
    };

    const closeButtons = document.querySelectorAll('.modal .close');
    const pedidosTableBody = document.getElementById('pedidosTableBody');

    function showModal(modal) {
        if (modal) modal.classList.add('show');
    }

    function closeModal(modal) {
        if (modal) modal.classList.remove('show');
    }

    buttons.pedidos?.addEventListener('click', (e) => {
        e.preventDefault();
        showModal(modals.pedidos);
        const url = buttons.pedidos.getAttribute('data-url');
        cargarPedidos(url);
    });

    buttons.login?.addEventListener('click', (e) => {
        e.preventDefault();
        showModal(modals.login);
    });

    buttons.profile?.addEventListener('click', (e) => {
        e.preventDefault();
        showModal(modals.profile);
    });

    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => closeModal(btn.closest('.modal')));
    });

    Object.values(modals).forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) closeModal(modal);
        });
    });

    async function cargarPedidos(url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error('Error en la respuesta del servidor');
            const data = await response.json();

            pedidosTableBody.innerHTML = '';

            data.pedidos.forEach(pedido => {
                const row = document.createElement('tr');
                row.classList.add('pedido-row');
                row.innerHTML = `
                    <td>${pedido.id}</td>
                    <td>$${Number(pedido.total).toFixed(2)}</td>
                    <td>${pedido.estado}</td>
                    <td>
                        <button class="btn btn-info btn-sm ver-productos-btn">
                            Ver Productos
                        </button>
                    </td>
                `;
                pedidosTableBody.appendChild(row);

                const verProductosBtn = row.querySelector('.ver-productos-btn');
                verProductosBtn.addEventListener('click', () =>
                    toggleProductos(pedido.items, row)
                );
            });
        } catch (error) {
            console.error('Error al cargar los pedidos:', error);
        }
    }

    function toggleProductos(items, parentRow) {
        let productosRow = parentRow.nextElementSibling;
    
        if (productosRow && productosRow.classList.contains('productos-row')) {
            productosRow.remove(); 
        } else {
            productosRow = document.createElement('tr');
            productosRow.classList.add('productos-row');
            const productosHTML = items.map(item => `
                <li>${item.cantidad} x ${item.producto} - $${Number(item.subtotal).toFixed(2)}</li>
            `).join('');
            productosRow.innerHTML = `<td colspan="4"><ul>${productosHTML}</ul></td>`;
            parentRow.after(productosRow);
    
            // Asegurar que el nuevo contenido no desborde el modal
            const tableContainer = document.querySelector('.table-container');
            tableContainer.scrollTop = tableContainer.scrollHeight;
        }
    }
    
});
