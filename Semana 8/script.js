// Botón de alerta personalizada
document.getElementById('alertButton').addEventListener('click', function() {
    Swal.fire({
        title: '¡Alerta Personalizada!',
        text: 'Esta es una alerta personalizada usando JavaScript. ¡Bien hecho!',
        icon: 'info',
        confirmButtonText: 'Entendido',
        confirmButtonColor: '#007bff',
        backdrop: true,
        timer: 5000,
        timerProgressBar: true,
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        }
    });
});

// Validación del formulario
(function() {
    'use strict';
    
    // Fetch all forms that need validation
    const form = document.getElementById('contactForm');
    const formMessage = document.getElementById('formMessage');
    
    // Validación al enviar el formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        event.stopPropagation();
        
        if (!form.checkValidity()) {
            // Mostrar mensajes de error
            event.preventDefault();
            event.stopPropagation();
        } else {
            // Formulario válido - simular envío
            enviarFormulario();
        }
        
        form.classList.add('was-validated');
    }, false);
    
    // Validación en tiempo real
    const campos = form.querySelectorAll('input, textarea, select');
    campos.forEach(campo => {
        campo.addEventListener('input', function() {
            validarCampo(this);
        });
        
        campo.addEventListener('blur', function() {
            validarCampo(this);
        });
    });
    
    // Función para validar campo individual
    function validarCampo(campo) {
        if (campo.checkValidity()) {
            campo.classList.remove('is-invalid');
            campo.classList.add('is-valid');
        } else {
            campo.classList.remove('is-valid');
            campo.classList.add('is-invalid');
        }
    }
    
    // Función para enviar el formulario (simulación)
    function enviarFormulario() {
        // Mostrar mensaje de éxito
        formMessage.classList.remove('d-none');
        formMessage.textContent = '¡Mensaje enviado correctamente! Te contactaremos pronto.';
        
        // Limpiar formulario después de 3 segundos
        setTimeout(() => {
            form.reset();
            form.classList.remove('was-validated');
            
            // Remover clases de validación
            campos.forEach(campo => {
                campo.classList.remove('is-valid', 'is-invalid');
            });
            
            formMessage.classList.add('d-none');
        }, 3000);
    }
    
    // Validación especial para el campo de email
    const emailInput = document.getElementById('email');
    emailInput.addEventListener('input', function() {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        
        if (!emailRegex.test(this.value) && this.value !== '') {
            this.setCustomValidity('Por favor, ingresa un correo electrónico válido.');
        } else {
            this.setCustomValidity('');
        }
    });
})();

// SweetAlert (para alertas más atractivas)
// Incluimos SweetAlert desde CDN dinámicamente
function cargarSweetAlert() {
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/sweetalert2@11';
    script.onload = function() {
        // También cargamos animate.css para efectos
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css';
        document.head.appendChild(link);
    };
    document.head.appendChild(script);
}

// Cargar SweetAlert cuando se cargue la página
window.addEventListener('DOMContentLoaded', cargarSweetAlert);

// Función para hacer la navegación suave
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});