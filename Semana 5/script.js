// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Obtener elementos del DOM
    const gallery = document.getElementById('gallery');
    const imageUrlInput = document.getElementById('imageUrl');
    const addButton = document.getElementById('addButton');
    const deleteButton = document.getElementById('deleteButton');
    const clearButton = document.getElementById('clearButton');
    const imageCountElement = document.getElementById('imageCount');
    const previewImage = document.getElementById('previewImage');
    const previewPlaceholder = document.getElementById('previewPlaceholder');
    
    // Variable para almacenar la imagen seleccionada
    let selectedImage = null;
    
    // Función para actualizar el contador de imágenes
    function updateImageCount() {
        const images = document.querySelectorAll('.image-item');
        const count = images.length;
        imageCountElement.textContent = `${count} ${count === 1 ? 'imagen' : 'imágenes'}`;
        
        // Mostrar u ocultar mensaje de galería vacía
        const emptyGallery = document.querySelector('.empty-gallery');
        if (count === 0 && !emptyGallery) {
            gallery.innerHTML = '<div class="empty-gallery"><i class="fas fa-image"></i><p>Tu galería está vacía. ¡Agrega tu primera imagen!</p></div>';
        } else if (count > 0 && emptyGallery) {
            emptyGallery.remove();
            if (!document.querySelector('.gallery-container')) {
                const galleryContainer = document.createElement('div');
                galleryContainer.className = 'gallery-container';
                gallery.appendChild(galleryContainer);
            }
        }
    }
    
    // Función para agregar una imagen a la galería
    function addImage(url) {
        // Validar URL
        if (!url || url.trim() === '') {
            alert('Por favor, ingresa una URL de imagen válida.');
            return;
        }
        
        // Verificar si la galería tiene el contenedor
        let galleryContainer = document.querySelector('.gallery-container');
        if (!galleryContainer) {
            // Eliminar mensaje de galería vacía si existe
            const emptyGallery = document.querySelector('.empty-gallery');
            if (emptyGallery) emptyGallery.remove();
            
            // Crear contenedor de galería
            galleryContainer = document.createElement('div');
            galleryContainer.className = 'gallery-container';
            gallery.appendChild(galleryContainer);
        }
        
        // Crear elemento de imagen
        const imageItem = document.createElement('div');
        imageItem.className = 'image-item';
        
        // Crear elemento img
        const img = document.createElement('img');
        img.src = url;
        img.alt = 'Imagen de galería';
        
        // Crear overlay para la imagen
        const overlay = document.createElement('div');
        overlay.className = 'image-overlay';
        overlay.textContent = 'Haz clic para seleccionar';
        
        // Agregar imagen y overlay al contenedor
        imageItem.appendChild(img);
        imageItem.appendChild(overlay);
        
        // Agregar evento click para seleccionar la imagen
        imageItem.addEventListener('click', function() {
            selectImage(imageItem);
        });
        
        // Agregar la imagen a la galería
        galleryContainer.appendChild(imageItem);
        
        // Limpiar el campo de entrada
        imageUrlInput.value = '';
        
        // Actualizar contador
        updateImageCount();
    }
    
    // Función para seleccionar una imagen
    function selectImage(imageElement) {
        // Deseleccionar la imagen actualmente seleccionada
        if (selectedImage) {
            selectedImage.classList.remove('selected');
        }
        
        // Seleccionar la nueva imagen
        selectedImage = imageElement;
        selectedImage.classList.add('selected');
        
        // Habilitar el botón de eliminar
        deleteButton.disabled = false;
        
        // Actualizar vista previa
        const imgSrc = imageElement.querySelector('img').src;
        previewImage.src = imgSrc;
        previewImage.style.display = 'block';
        previewPlaceholder.style.display = 'none';
    }
    
    // Función para eliminar la imagen seleccionada
    function deleteSelectedImage() {
        if (!selectedImage) return;
        
        // Eliminar la imagen del DOM
        selectedImage.remove();
        
        // Limpiar selección
        selectedImage = null;
        
        // Deshabilitar botón de eliminar
        deleteButton.disabled = true;
        
        // Limpiar vista previa
        previewImage.src = '';
        previewImage.style.display = 'none';
        previewPlaceholder.style.display = 'block';
        
        // Actualizar contador
        updateImageCount();
    }
    
    // Función para limpiar toda la galería
    function clearGallery() {
        if (confirm('¿Estás seguro de que quieres eliminar todas las imágenes de la galería?')) {
            // Eliminar todas las imágenes
            const galleryContainer = document.querySelector('.gallery-container');
            if (galleryContainer) {
                galleryContainer.remove();
            }
            
            // Limpiar selección
            selectedImage = null;
            
            // Deshabilitar botón de eliminar
            deleteButton.disabled = true;
            
            // Limpiar vista previa
            previewImage.src = '';
            previewImage.style.display = 'none';
            previewPlaceholder.style.display = 'block';
            
            // Actualizar contador
            updateImageCount();
        }
    }
    
    // Agregar eventos
    
    // Agregar imagen al hacer clic en el botón
    addButton.addEventListener('click', function() {
        addImage(imageUrlInput.value);
    });
    
    // Agregar imagen al presionar Enter en el campo de entrada
    imageUrlInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            addImage(imageUrlInput.value);
        }
    });
    
    // Eliminar imagen seleccionada
    deleteButton.addEventListener('click', deleteSelectedImage);
    
    // Limpiar toda la galería
    clearButton.addEventListener('click', clearGallery);
    
    // Inicializar contador de imágenes
    updateImageCount();
    
    // Agregar algunas imágenes por defecto al cargar la página
    // Esto es opcional, pero ayuda a probar la funcionalidad
    setTimeout(() => {
        const defaultImages = [
            'https://images.unsplash.com/photo-1506744038136-46273834b3fb',
            'https://images.unsplash.com/photo-1519681393784-d120267933ba',
            'https://images.unsplash.com/photo-1501785888041-af3ef285b470',
            'https://images.unsplash.com/photo-1475924156734-496f6cac6ec1'
        ];
        
        // Agregar solo si la galería está vacía
        if (document.querySelector('.empty-gallery')) {
            defaultImages.forEach(url => {
                addImage(url);
            });
        }
    }, 500);
});