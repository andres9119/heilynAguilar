/**
 * bolsa.js - Lógica para el carrito de compras (Bolsa) vía WhatsApp
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
        if (e.target.classList.contains('add-to-bag')) {
            const product = {
                id: e.target.dataset.id,
                name: e.target.dataset.name,
                price: parseFloat(e.target.dataset.price),
                image: e.target.dataset.image,
                talla: e.target.dataset.talla || 'Única',
                color: e.target.dataset.color || 'Único'
            };
            addToBag(product);
        }
    });

    function toggleBag() {
        bagSidebar.classList.toggle('active');
        bagOverlay.classList.toggle('active');
    }

    function addToBag(product) {
        // Check if item already exists with same talla & color
        const existing = bag.find(item => item.id === product.id && item.talla === product.talla && item.color === product.color);
        if (existing) {
            existing.quantity = (existing.quantity || 1) + 1;
        } else {
            product.quantity = 1;
            bag.push(product);
        }
        saveBag();
        renderBag();
        if (!bagSidebar.classList.contains('active')) toggleBag();
    }

    function removeFromBag(index) {
        bag.splice(index, 1);
        saveBag();
        renderBag();
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

    function renderBag() {
        if (!bagItemsContainer) return;
        
        bagCountBadge.innerText = bag.reduce((acc, item) => acc + (item.quantity || 1), 0);
        
        if (bag.length === 0) {
            bagItemsContainer.innerHTML = '<div class="text-center py-5 text-muted small">Tu bolsa está vacía</div>';
            bagTotalDisplay.innerText = '$0';
            return;
        }

        let total = 0;
        bagItemsContainer.innerHTML = bag.map((item, index) => {
            total += item.price * (item.quantity || 1);
            return `
                <div class="bag-item d-flex gap-3 mb-4">
                    <img src="${item.image}" alt="${item.name}" style="width: 70px; height: 90px; object-fit: cover; border-radius: 4px;">
                    <div class="flex-grow-1">
                        <div class="d-flex justify-content-between">
                            <h6 class="mb-1 small fw-bold">${item.name}</h6>
                            <button class="btn-close" style="font-size: 0.6rem;" onclick="removeFromBag(${index})"></button>
                        </div>
                        <p class="text-muted mb-1" style="font-size: 0.7rem;">TALLA: ${item.talla} | COLOR: ${item.color}</p>
                        <div class="d-flex justify-content-between align-items-center mt-2">
                             <span class="small fw-bold">$${Math.round(item.price).toLocaleString('es-CO')} COP</span>
                             <span class="small text-muted">Cant: ${item.quantity || 1}</span>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
        bagTotalDisplay.innerText = `$${Math.round(total).toLocaleString('es-CO')} COP`;
    }

    window.removeFromBag = removeFromBag; // Make it global for the onclick

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
