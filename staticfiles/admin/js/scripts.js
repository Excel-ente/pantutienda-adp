function showModal(card) {
    const name = card.dataset.name;
    const image = card.dataset.image;
    const prices = JSON.parse(card.dataset.prices);

    document.getElementById('modalImage').src = image;
    document.getElementById('modalTitle').textContent = name;

    priceSelect.innerHTML = '';
    prices.forEach(price => {
        const option = document.createElement('option');
        option.value = price;
        option.textContent = `$${price.toFixed(2)}`;
        priceSelect.appendChild(option);
    });

    updateTotal();
    modal.classList.add('show'); // Agregar clase 'show'
}

// closeBtn.onclick = () => modal.classList.remove('show'); // Remover clase 'show'
// window.onclick = (event) => {
//     if (event.target === modal) modal.classList.remove('show');
// };
