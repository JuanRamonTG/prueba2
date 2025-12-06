function renderCarrito() {
    // Compatibilidad: esta función puede ejecutarse en varias páginas.
    const lista = document.getElementById('lista'); // tabla en carrito.html
    const totalEl = document.getElementById('total'); // total en carrito.html
    const carritoItemsModal = document.getElementById('carrito-items'); // modal en menu.html
    const carritoTotalModal = document.getElementById('carrito-total');

    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];

    // Si estamos en la página carrito.html (tabla), renderizar la tabla
    if (lista && totalEl) {
        lista.innerHTML = '';

        let total = 0;

        carrito.forEach((p, index) => {
            const subtotal = p.precio * p.cantidad;
            total += subtotal;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${p.nombre}</td>
                <td>
                    <button class="btn btn-sm btn-outline-secondary me-1" onclick="cambiarCantidad(${p.id}, -1)">-</button>
                    ${p.cantidad}
                    <button class="btn btn-sm btn-outline-secondary ms-1" onclick="cambiarCantidad(${p.id}, 1)">+</button>
                </td>
                <td>$${p.precio.toFixed(2)}</td>
                <td>$${subtotal.toFixed(2)}</td>
                <td><button class="btn btn-sm btn-danger" onclick="eliminarProducto(${p.id})">Eliminar</button></td>
            `;

            lista.appendChild(tr);
        });

        totalEl.textContent = total.toFixed(2);
    }

    // Si estamos en una página con modal (menu.html), actualizar el modal
    if (carritoItemsModal && carritoTotalModal) {
        if (carrito.length === 0) {
            carritoItemsModal.innerHTML = '<p class="text-center text-muted my-5">Tu carrito está vacío</p>';
            carritoTotalModal.textContent = '$0';
        } else {
            carritoItemsModal.innerHTML = '';
            let total = 0;
            carrito.forEach(item => {
                const subtotal = item.precio * item.cantidad;
                total += subtotal;

                const itemDiv = document.createElement('div');
                itemDiv.className = 'item-carrito';
                itemDiv.innerHTML = `
                    <div class="d-flex justify-content-between align-items-start">
                        <div>
                            <h6 class="mb-1">${item.nombre}</h6>
                            <p class="text-muted mb-1 small">${item.detalle || ''}</p>
                            <div class="d-flex align-items-center">
                                <button class="btn btn-sm btn-outline-secondary btn-restar" data-id="${item.id}">-</button>
                                <span class="mx-2">${item.cantidad}</span>
                                <button class="btn btn-sm btn-outline-secondary btn-sumar" data-id="${item.id}">+</button>
                                <button class="btn btn-sm btn-outline-danger ms-2 btn-eliminar" data-id="${item.id}">Eliminar</button>
                            </div>
                        </div>
                        <div class="text-end">
                            <p class="mb-1 fw-bold">$${(subtotal).toFixed(2)}</p>
                            <p class="text-muted small mb-0">$${(item.precio).toFixed(2)} c/u</p>
                        </div>
                    </div>
                `;
                carritoItemsModal.appendChild(itemDiv);
            });

            carritoTotalModal.textContent = `$${total.toFixed(2)}`;

            // Agregar listeners dinámicos dentro del modal
            carritoItemsModal.querySelectorAll('.btn-sumar').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const id = parseInt(e.currentTarget.getAttribute('data-id'));
                    const item = carrito.find(i => i.id === id);
                    if (item) {
                        item.cantidad += 1;
                        localStorage.setItem('carrito', JSON.stringify(carrito));
                        renderCarrito();
                        if (window.updateCartIndicator) window.updateCartIndicator();
                    }
                });
            });

            carritoItemsModal.querySelectorAll('.btn-restar').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const id = parseInt(e.currentTarget.getAttribute('data-id'));
                    const idx = carrito.findIndex(i => i.id === id);
                    if (idx !== -1) {
                        if (carrito[idx].cantidad > 1) carrito[idx].cantidad -= 1;
                        else carrito.splice(idx, 1);
                        localStorage.setItem('carrito', JSON.stringify(carrito));
                        renderCarrito();
                        if (window.updateCartIndicator) window.updateCartIndicator();
                    }
                });
            });

            carritoItemsModal.querySelectorAll('.btn-eliminar').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const id = parseInt(e.currentTarget.getAttribute('data-id'));
                    const idx = carrito.findIndex(i => i.id === id);
                    if (idx !== -1) {
                        carrito.splice(idx, 1);
                        localStorage.setItem('carrito', JSON.stringify(carrito));
                        renderCarrito();
                        if (window.updateCartIndicator) window.updateCartIndicator();
                    }
                });
            });
        }
    }
}

function cambiarCantidad(id, delta) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    const item = carrito.find(x => x.id === id);
    if (!item) return;

    item.cantidad += delta;
    if (item.cantidad <= 0) {
        carrito = carrito.filter(x => x.id !== id);
    }

    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    if (window.updateCartIndicator) window.updateCartIndicator();
}

function eliminarProducto(id) {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    carrito = carrito.filter(x => x.id !== id);
    localStorage.setItem('carrito', JSON.stringify(carrito));
    renderCarrito();
    if (window.updateCartIndicator) window.updateCartIndicator();
}

async function realizarPedido() {
    let carrito = JSON.parse(localStorage.getItem('carrito')) || [];
    if (carrito.length === 0) {
        alert('El carrito está vacío');
        return;
    }

    const items = carrito.map(p => ({ id: p.id, cantidad: p.cantidad, precio: p.precio }));
    const total = carrito.reduce((s, p) => s + p.precio * p.cantidad, 0);

    // Obtener datos del formulario (si existen en la página)
    const fechaEl = document.getElementById('pedido_fecha');
    const horaEl = document.getElementById('pedido_hora');
    const tipoEl = document.getElementById('tipo_entrega');
    const metodoEl = document.querySelector('input[name="metodo_pago"]:checked');

    const fecha = fechaEl ? fechaEl.value : null;
    const hora = horaEl ? horaEl.value : null;
    const tipo_entrega = tipoEl ? tipoEl.value : 'domicilio';
    const metodo_pago = metodoEl ? metodoEl.value : 'efectivo';

    // Validaciones básicas
    if (!fecha) {
        alert('Por favor selecciona la fecha del pedido.');
        return;
    }

    if (!hora) {
        alert('Por favor selecciona la hora del pedido.');
        return;
    }

    try {
        const res = await fetch('http://localhost:8000/pedidos/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ items, total, fecha_programada: fecha, hora_programada: hora, tipo_entrega, metodo_pago })
        });

        if (!res.ok) {
            // intentar leer cuerpo con detalle de error (FastAPI devuelve JSON con 'detail')
            let errText = 'Error al enviar pedido';
            try {
                const errBody = await res.json();
                if (errBody.detail) errText = JSON.stringify(errBody.detail);
                else errText = JSON.stringify(errBody);
            } catch (e) {
                errText = `${res.status} ${res.statusText}`;
            }
            throw new Error(errText);
        }

        const data = await res.json();
        alert('Pedido enviado: ' + data.mensaje);
        // limpiar carrito
        localStorage.removeItem('carrito');
        renderCarrito();
    if (window.updateCartIndicator) window.updateCartIndicator();
        // Cerrar modal si está abierto
        try {
            const modalEl = document.getElementById('modalCarrito');
            if (modalEl) {
                const modalInstance = bootstrap.Modal.getInstance(modalEl) || new bootstrap.Modal(modalEl);
                modalInstance.hide();
            }
        } catch (e) {
            // bootstrap no disponible o error, ignorar
        }
    } catch (e) {
        console.error(e);
        alert('No se pudo enviar el pedido. Revisa la consola.');
    }
}

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    renderCarrito();
});
