// arreglo inicial
let productos = [
    {
        nombre: "Ryunx Gamer Pro",
        precio: 1599.99,
        descripcion: "Laptop de ultima generacion para gaming y desarrollo"
    },
    {
        nombre: "Teclado Mecanico RGB %75",
        precio: 66.66,
        descripcion: "Teclado mecánico con retroiluminación RGB personalizable"
    },
    {
        nombre: "Mouse Inalambrico Logitech",
        precio: 75.50,
        descripcion: "Mouse ergonómico con conexión Bluetooth y 6 botones programables"
    },
    {
        nombre: "Monitor 4K 27''",
        precio: 325.99,
        descripcion: "Monitor UHD con tasa de refresco de 144Hz y HDR"
    },
    {
        nombre: "Auriculares Noise Cancelling",
        precio: 99.99,
        descripcion: "Auriculares con cancelación activa de ruido y sonido surround"
    }
];

// elementos del DOM
const productList = document.getElementById('productList');
const productTemplate = document.getElementById('productTemplate');
const addProductBtn = document.getElementById('addProductBtn');
const clearListBtn = document.getElementById('clearListBtn');
const loadSampleBtn = document.getElementById('loadSampleBtn');
const productCount = document.getElementById('productCount');

// inputs
const productNameInput = document.getElementById('productName');
const productPriceInput = document.getElementById('productPrice');
const productDescriptionInput = document.getElementById('productDescription');

// formatear la fecha
function formatearFecha(fecha) {
    return fecha.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
    });
}

// formatear precio
function formatearPrecio(precio) {
    return `$${precio.toFixed(2)}`;
}

// renderizar todos los productos
function renderizarProductos() {
    // Limpiar lista 
    productList.innerHTML = '';
    
    // producto en el arreglo
    productos.forEach((producto, index) => {
        // clonar 
        const productClone = document.importNode(productTemplate.content, true);
        
        // elementos
        const productName = productClone.querySelector('.product-name');
        const productPrice = productClone.querySelector('.product-price');
        const productDescription = productClone.querySelector('.product-description');
        const productTime = productClone.querySelector('.product-time');
        
        // asignar valores
        productName.textContent = producto.nombre;
        productPrice.textContent = formatearPrecio(producto.precio);
        productDescription.textContent = producto.descripcion;
        productTime.textContent = producto.hora ? producto.hora : formatearFecha(new Date());
        
        // agregar a lista
        productList.appendChild(productClone);
    });
    
    // actualizar
    actualizarContador();
}

// nuevo producto
function agregarProducto() {
    const nombre = productNameInput.value.trim();
    const precio = parseFloat(productPriceInput.value);
    const descripcion = productDescriptionInput.value.trim();
    
    // validaciones
    if (!nombre) {
        alert('Por favor, digita el nombre del producto');
        productNameInput.focus();
        return;
    }
    
    if (!precio || precio <= 0) {
        alert('Debes ingresar un precio válido (mayor a 0)');
        productPriceInput.focus();
        return;
    }
    
    if (!descripcion) {
        alert('Por favor, registra una descripción del producto');
        productDescriptionInput.focus();
        return;
    }
    
    // nuevo producto
    const nuevoProducto = {
        nombre: nombre,
        precio: precio,
        descripcion: descripcion,
        hora: formatearFecha(new Date())
    };
    
    // arreglo
    productos.push(nuevoProducto);
    
    // renderizar
    renderizarProductos();
    
    // formulario
    productNameInput.value = '';
    productPriceInput.value = '';
    productDescriptionInput.value = '';
    productNameInput.focus();
    
    // confirmación
    console.log(`Producto "${nombre}" agregado exitosamente.`);
}

// productos de ejemplo
function cargarProductosEjemplo() {
    // productos iniciales
    productos = [
        {
            nombre: "Ryunx Gamer Pro",
            precio: 1599.99,
            descripcion: "Laptop de alto rendimiento para gaming y desarrollo"
        },
        {
            nombre: "Teclado Mecánico RGB %75",
            precio: 66.66,
            descripcion: "Teclado mecánico con retroiluminación RGB personalizable"
        },
        {
            nombre: "Mouse Inalámbrico Logitech",
            precio: 75.50,
            descripcion: "Mouse ergonómico con conexión Bluetooth y 6 botones programables"
        },
        {
            nombre: "Monitor 4K 27''",
            precio: 325.99,
            descripcion: "Monitor UHD con tasa de refresco de 144Hz y HDR"
        },
        {
            nombre: "Auriculares Noise Cancelling",
            precio: 99.99,
            descripcion: "Auriculares con cancelación activa de ruido y sonido surround"
        }
    ];
    
    renderizarProductos();
    alert('Productos de ejemplo cargados exitosamente.');
}

// limpiar la lista
function limpiarLista() {
    if (productos.length === 0) {
        alert('La lista ya está vacía.');
        return;
    }
    
    if (confirm('¿Estás seguro de que deseas eliminar todos los productos?')) {
        productos = [];
        renderizarProductos();
        console.log('Lista de productos limpiada.');
    }
}

// actualizar el contador de productos
function actualizarContador() {
    productCount.textContent = `Productos en lista: ${productos.length}`;
}

// Listeners
addProductBtn.addEventListener('click', agregarProducto);

clearListBtn.addEventListener('click', limpiarLista);

loadSampleBtn.addEventListener('click', cargarProductosEjemplo);

// agregar producto
[productNameInput, productPriceInput, productDescriptionInput].forEach(input => {
    input.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            agregarProducto();
        }
    });
});

// Inicializar
document.addEventListener('DOMContentLoaded', function() {
    // Renderizar
    renderizarProductos();
    
    // Mensaje
    console.log('Aplicación de lista de productos cargada exitosamente.');
    console.log('Instrucciones:');
    console.log('1. Usa el formulario para agregar nuevos productos');
    console.log('2. Haz clic en "Cargar Productos de Ejemplo" para restaurar la lista inicial');
    console.log('3. Haz clic en "Limpiar Lista" para eliminar todos los productos');
});

// Carga con timeout
setTimeout(() => {
    console.log('Aplicación lista para usar. Total de productos:', productos.length);
}, 1000);