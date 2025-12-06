function getCartCount() {
    const carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    return carrito.reduce((s, p) => s + (p.cantidad || 0), 0);
}

function updateCartIndicator() {
    const el = document.getElementById('cart-count');
    if (!el) return;
    const count = getCartCount();
    el.textContent = count || '';
    el.style.display = count > 0 ? 'inline-block' : 'none';
}

// Escuchar cambios en localStorage (otras pestañas) para mantener sincronizado
window.addEventListener('storage', function(e) {
    if (e.key === 'carrito') updateCartIndicator();
});

// Hacer la función pública
window.updateCartIndicator = updateCartIndicator;

// Actualizar al cargar
document.addEventListener('DOMContentLoaded', updateCartIndicator);
