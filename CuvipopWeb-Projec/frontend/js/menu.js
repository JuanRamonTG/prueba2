async function cargarProductos() {
    const contenedor = document.getElementById("productos");

    const res = await fetch("http://localhost:8000/productos/");
    const productos = await res.json();

    productos.forEach(p => {
        contenedor.innerHTML += `
            <div class="col-md-4">
                <div class="producto-card">
                    <img src="${p.imagen}" class="producto-img">

                    <div class="p-3 text-center">
                        <h5>${p.nombre}</h5>
                        <p>$${p.precio.toFixed(2)}</p>
                        <button class="btn btn-pastel" onclick="agregarCarrito(${p.id}, '${p.nombre}', ${p.precio})">
                            Agregar 🛒
                        </button>
                    </div>
                </div>
            </div>
        `;
    });
}

function agregarCarrito(id, nombre, precio) {
    let carrito = JSON.parse(localStorage.getItem("carrito")) || [];

    const existe = carrito.find(p => p.id === id);

    if (existe) {
        existe.cantidad++;
    } else {
        carrito.push({ id, nombre, precio, cantidad: 1 });
    }

    localStorage.setItem("carrito", JSON.stringify(carrito));

    // Actualizar indicador global si existe
    if (window.updateCartIndicator) window.updateCartIndicator();

    alert("Producto agregado al carrito 🍡");
}

cargarProductos();
