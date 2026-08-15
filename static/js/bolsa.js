/**
 * bolsa.js - Lógica para el carrito de compras (Bolsa) vía WhatsApp
 * Flujo: pago por Nequi (312 308 0861) + envío de comprobante por WhatsApp
 */

document.addEventListener('DOMContentLoaded', () => {
    let bag = JSON.parse(localStorage.getItem('heilyn_bag')) || [];
    const bagSidebar = document.getElementById('bag-sidebar');
    const bagOverlay = document.getElementById('bag-overlay');
    const openBagBtn = document.getElementById('open-bag');
    const closeBagBtn = document.getElementById('close-sidebar');
    const bagItemsContainer = document.getElementById('bag-items-container');
    const bagCountBadge = document.getElementById('bag-count');
    const bagTotalDisplay = document.getElementById('bag-total');
    const clearBagBtn = document.getElementById('clear-bag');
    const whatsappCheckoutBtn = document.getElementById('whatsapp-checkout');

    // Update UI on load
    renderBag();

    // Event Listeners
    if (openBagBtn) openBagBtn.addEventListener('click', toggleBag);
    if (closeBagBtn) closeBagBtn.addEventListener('click', toggleBag);
    if (bagOverlay) bagOverlay.addEventListener('click', toggleBag);
    if (clearBagBtn) clearBagBtn.addEventListener('click', clearBag);
    if (whatsappCheckoutBtn) whatsappCheckoutBtn.addEventListener('click', checkoutWhatsApp);

    // Global click for "Add to Bag" buttons (using event delegation)
    document.addEventListener('click', (e) => {
        const addBtn = e.target.closest('.add-to-bag');
        if (addBtn) {
            const product = {
                id: addBtn.dataset.id,
                name: addBtn.dataset.name,
                price: parseFloat(addBtn.dataset.price),
                image: addBtn.dataset.image,
                talla: addBtn.dataset.talla || 'Única',
                color: addBtn.dataset.color || 'Único'
            };

            // Si hay selector de talla en la tarjeta y aún no eligió, alertar
            const card = addBtn.closest('.ha-card');
            if (card) {
                const activeSize = card.querySelector('.ha-size-btn.active');
                if (addBtn.dataset.requireSize === 'true' && !activeSize) {
                    alert('Selecciona una talla primero');
                    return;
                }
                if (activeSize) product.talla = activeSize.dataset.value;
            }
            addToBag(product);
        }

        // Controles de cantidad / eliminación dentro del carrito
        const qtyBtn = e.target.closest('[data-qty]');
        if (qtyBtn && bagItemsContainer.contains(qtyBtn)) {
            const index = parseInt(qtyBtn.dataset.index, 10);
            const delta = parseInt(qtyBtn.dataset.qty, 10);
            if (bag[index]) {
                bag[index].quantity = (bag[index].quantity || 1) + delta;
                if (bag[index].quantity < 1) bag[index].quantity = 1;
                saveBag(); renderBag();
            }
        }
        const removeBtn = e.target.closest('[data-remove]');
        if (removeBtn && bagItemsContainer.contains(removeBtn)) {
            const index = parseInt(removeBtn.dataset.remove, 10);
            bag.splice(index, 1);
            saveBag(); renderBag();
        }
    });

    function toggleBag() {
        bagSidebar.classList.toggle('open');
        bagOverlay.classList.toggle('open');
        document.body.style.overflow = bagSidebar.classList.contains('open') ? 'hidden' : '';
    }

    function addToBag(product) {
        const existing = bag.find(item => item.id === product.id && item.talla === product.talla && item.color === product.color);
        if (existing) {
            existing.quantity = (existing.quantity || 1) + 1;
        } else {
            product.quantity = 1;
            bag.push(product);
        }
        saveBag();
        renderBag();
        if (!bagSidebar.classList.contains('open')) toggleBag();
    }

    function clearBag() {
        if (confirm('¿Deseas vaciar tu selección?')) {
            bag = [];
            saveBag();
            renderBag();
        }
    }

    function saveBag() {
        localStorage.setItem('heilyn_bag', JSON.stringify(bag));
    }

    function money(n) {
        return '$' + Math.round(n).toLocaleString('es-CO');
    }

    function renderBag() {
        if (!bagItemsContainer) return;
        const totalQuantity = bag.reduce((acc, item) => acc + (item.quantity || 1), 0);
        if (bagCountBadge) bagCountBadge.innerText = totalQuantity;

        if (bag.length === 0) {
            bagItemsContainer.innerHTML =
                '<div class="ha-cart-empty">' +
                '  <div class="ha-cart-empty-icon"><i class="fas fa-shopping-bag"></i></div>' +
                '  <div class="ha-cart-empty-title">Tu carrito está vacío</div>' +
                '  <p class="ha-cart-empty-sub">Añade tus must-haves y paga por WhatsApp en segundos.</p>' +
                '</div>';
            bagTotalDisplay.innerText = '$0';
            return;
        }

        let total = 0;
        bagItemsContainer.innerHTML = bag.map((item, index) => {
            const itemTotal = item.price * (item.quantity || 1);
            total += itemTotal;
            const img = item.image
                ? '<img src="' + item.image + '" alt="' + item.name + '">'
                : '<i class="fas fa-image"></i>';
            return (
                '<div class="ha-cart-item">' +
                '  <div class="ha-cart-item-img">' + img + '</div>' +
                '  <div class="ha-cart-item-body">' +
                '    <div class="ha-cart-item-top">' +
                '      <span class="ha-cart-item-name">' + item.name + '</span>' +
                '      <button class="ha-cart-remove" data-remove="' + index + '" aria-label="Eliminar"><i class="fas fa-times"></i></button>' +
                '    </div>' +
                '    <div class="ha-cart-item-meta">Talla ' + item.talla + ' | ' + item.color + '</div>' +
                '    <div class="ha-cart-item-bottom">' +
                '      <span class="ha-cart-item-price">' + money(itemTotal) + '</span>' +
                '      <div class="ha-qty">' +
                '        <button class="ha-qty-btn" data-qty="-1" data-index="' + index + '" aria-label="Menos"><i class="fas fa-minus"></i></button>' +
                '        <span class="ha-qty-num">' + (item.quantity || 1) + '</span>' +
                '        <button class="ha-qty-btn" data-qty="1" data-index="' + index + '" aria-label="Más"><i class="fas fa-plus"></i></button>' +
                '      </div>' +
                '    </div>' +
                '  </div>' +
                '</div>'
            );
        }).join('');
        bagTotalDisplay.innerText = money(total);
    }

    function checkoutWhatsApp() {
        if (bag.length === 0) return;

        let message = "¡Hola! 👋 Me interesa adquirir las siguientes prendas de la tienda:\n\n";
        let total = 0;

        bag.forEach(item => {
            const itemTotal = item.price * (item.quantity || 1);
            message += `👗 *${item.name}*\n   Talla: ${item.talla} | Color: ${item.color}\n   Cant: ${item.quantity || 1} - Precio: $${Math.round(item.price).toLocaleString('es-CO')} COP\n\n`;
            total += itemTotal;
        });

        message += `💰 *Total a pagar: $${Math.round(total).toLocaleString('es-CO')} COP*\n\n¡Hola! Acabo de hacer la transferencia por Nequi. En este chat adjuntaré el pantallazo para que me despachen el pedido. Quedo atenta para los datos de envío. 🚚✨`;

        const whatsappUrl = `https://wa.me/573123080861?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
    }
});