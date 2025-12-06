function cargarCarrito() {
    const lista = document.getElementById("lista");
    const totalSpan = document.getElementById("total");

    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    let total = 0;

    lista.innerHTML = "";

    carrito.forEach((p, i) => {
        const subtotal = p.precio * p.cantidad;
        total += subtotal;

        lista.innerHTML += `
            <tr>
                <td>${p.nombre}</td>
                <td>${p.cantidad}</td>
                <td>$${p.precio.toFixed(2)}</td>
                <td>$${subtotal.toFixed(2)}</td>
                <td>
                    <button class="btn btn-danger btn-sm" onclick="eliminar(${i})">X</button>
                </td>
            </tr>
        `;
    });

    totalSpan.textContent = total.toFixed(2);
}

function eliminar(index) {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];
    carrito.splice(index, 1);
    localStorage.setItem("carrito", JSON.stringify(carrito));
    cargarCarrito();
}

async function realizarPedido() {
    const carrito = JSON.parse(localStorage.getItem("carrito"));
    if (!carrito || carrito.length === 0) return alert("Carrito vacío");

    const token = localStorage.getItem("token");
    if (!token) return alert("Debes iniciar sesión");

    const pedido = {
        tipo_entrega: "llevar",
        fecha: new Date().toISOString().slice(0, 10),
        hora: "14:00",
        metodo_pago: "efectivo",
        productos: carrito
    };

    const res = await fetch("http://localhost:8000/pedidos/crear", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": "Bearer " + token
        },
        body: JSON.stringify(pedido)
    });

    const data = await res.json();

    if (!res.ok) {
        alert("Error: " + data.detail);
        return;
    }

    alert("Pedido realizado con éxito 🎉");
    localStorage.removeItem("carrito");
    window.location.href = "index.html";
}

cargarCarrito();
