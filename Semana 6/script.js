// Esperar a que el DOM esté completamente cargado
document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const form = document.getElementById('registrationForm');
    const nombreInput = document.getElementById('nombre');
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirmPassword');
    const edadInput = document.getElementById('edad');
    const submitBtn = document.getElementById('submitBtn');
    const resetBtn = document.getElementById('resetBtn');
    const togglePasswordBtn = document.getElementById('togglePassword');
    const toggleConfirmPasswordBtn = document.getElementById('toggleConfirmPassword');
    const validCountSpan = document.getElementById('validCount');
    const statusMessage = document.getElementById('statusMessage');
    
    // Referencias a mensajes de error
    const nombreError = document.getElementById('nombre-error');
    const emailError = document.getElementById('email-error');
    const passwordError = document.getElementById('password-error');
    const confirmPasswordError = document.getElementById('confirmPassword-error');
    const edadError = document.getElementById('edad-error');
    
    // Elementos para indicador de fuerza de contraseña
    const strengthFill = document.getElementById('strengthFill');
    const strengthText = document.getElementById('strengthText');
    
    // Objeto para rastrear el estado de validación de cada campo
    const validationState = {
        nombre: false,
        email: false,
        password: false,
        confirmPassword: false,
        edad: false
    };
    
    // Función para actualizar el contador de campos válidos
    function updateValidCount() {
        const validCount = Object.values(validationState).filter(Boolean).length;
        validCountSpan.textContent = validCount;
        return validCount;
    }
    
    // Función para verificar si todos los campos son válidos
    function checkAllFieldsValid() {
        const allValid = Object.values(validationState).every(Boolean);
        submitBtn.disabled = !allValid;
        return allValid;
    }
    
    // Función para mostrar/ocultar contraseña
    function togglePasswordVisibility(inputElement, toggleButton) {
        const type = inputElement.getAttribute('type') === 'password' ? 'text' : 'password';
        inputElement.setAttribute('type', type);
        
        // Cambiar icono del botón
        const icon = toggleButton.querySelector('i');
        icon.className = type === 'password' ? 'fas fa-eye' : 'fas fa-eye-slash';
    }
    
    // Validación del nombre
    function validateNombre() {
        const nombre = nombreInput.value.trim();
        const isValid = nombre.length >= 3;
        
        if (nombre === '') {
            nombreError.textContent = '';
            nombreInput.classList.remove('valid', 'invalid');
            validationState.nombre = false;
        } else if (isValid) {
            nombreError.textContent = '';
            nombreInput.classList.remove('invalid');
            nombreInput.classList.add('valid');
            validationState.nombre = true;
        } else {
            nombreError.textContent = 'El nombre debe tener al menos 3 caracteres';
            nombreInput.classList.remove('valid');
            nombreInput.classList.add('invalid');
            validationState.nombre = false;
        }
        
        updateValidCount();
        checkAllFieldsValid();
        return isValid;
    }
    
    // Validación del email con expresión regular
    function validateEmail() {
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const isValid = emailRegex.test(email);
        
        if (email === '') {
            emailError.textContent = '';
            emailInput.classList.remove('valid', 'invalid');
            validationState.email = false;
        } else if (isValid) {
            emailError.textContent = '';
            emailInput.classList.remove('invalid');
            emailInput.classList.add('valid');
            validationState.email = true;
        } else {
            emailError.textContent = 'Por favor, ingrese un correo electrónico válido';
            emailInput.classList.remove('valid');
            emailInput.classList.add('invalid');
            validationState.email = false;
        }
        
        updateValidCount();
        checkAllFieldsValid();
        return isValid;
    }
    
    // Validación de la contraseña y cálculo de fuerza
    function validatePassword() {
        const password = passwordInput.value;
        const hasMinLength = password.length >= 8;
        const hasNumber = /\d/.test(password);
        const hasSpecialChar = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/.test(password);
        
        // Calcular fuerza de la contraseña
        let strength = 0;
        let strengthMessage = '';
        let strengthColor = '';
        
        if (password.length === 0) {
            strength = 0;
            strengthMessage = 'Ingrese una contraseña';
            strengthColor = '#e74c3c';
        } else if (password.length < 8) {
            strength = 25;
            strengthMessage = 'Muy débil';
            strengthColor = '#e74c3c';
        } else if (password.length >= 8 && (hasNumber || hasSpecialChar)) {
            strength = 50;
            strengthMessage = 'Moderada';
            strengthColor = '#f39c12';
        } else if (password.length >= 10 && hasNumber && hasSpecialChar) {
            strength = 75;
            strengthMessage = 'Fuerte';
            strengthColor = '#3498db';
        } else if (password.length >= 12 && hasNumber && hasSpecialChar) {
            strength = 100;
            strengthMessage = 'Muy fuerte';
            strengthColor = '#2ecc71';
        }
        
        // Actualizar indicador de fuerza
        strengthFill.style.width = `${strength}%`;
        strengthFill.style.backgroundColor = strengthColor;
        strengthText.textContent = strengthMessage;
        strengthText.style.color = strengthColor;
        
        // Validar requisitos
        const isValid = hasMinLength && hasNumber && hasSpecialChar;
        
        if (password === '') {
            passwordError.textContent = '';
            passwordInput.classList.remove('valid', 'invalid');
            validationState.password = false;
        } else if (isValid) {
            passwordError.textContent = '';
            passwordInput.classList.remove('invalid');
            passwordInput.classList.add('valid');
            validationState.password = true;
        } else {
            let errorMessages = [];
            if (!hasMinLength) errorMessages.push('Mínimo 8 caracteres');
            if (!hasNumber) errorMessages.push('Al menos un número');
            if (!hasSpecialChar) errorMessages.push('Al menos un carácter especial');
            
            passwordError.textContent = errorMessages.join(', ');
            passwordInput.classList.remove('valid');
            passwordInput.classList.add('invalid');
            validationState.password = false;
        }
        
        // Validar también la confirmación si ya tiene valor
        if (confirmPasswordInput.value !== '') {
            validateConfirmPassword();
        }
        
        updateValidCount();
        checkAllFieldsValid();
        return isValid;
    }
    
    // Validación de confirmación de contraseña
    function validateConfirmPassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        const isValid = password === confirmPassword && password !== '';
        
        if (confirmPassword === '') {
            confirmPasswordError.textContent = '';
            confirmPasswordInput.classList.remove('valid', 'invalid');
            validationState.confirmPassword = false;
        } else if (isValid) {
            confirmPasswordError.textContent = '';
            confirmPasswordInput.classList.remove('invalid');
            confirmPasswordInput.classList.add('valid');
            validationState.confirmPassword = true;
        } else {
            confirmPasswordError.textContent = 'Las contraseñas no coinciden';
            confirmPasswordInput.classList.remove('valid');
            confirmPasswordInput.classList.add('invalid');
            validationState.confirmPassword = false;
        }
        
        updateValidCount();
        checkAllFieldsValid();
        return isValid;
    }
    
    // Validación de la edad
    function validateEdad() {
        const edad = parseInt(edadInput.value);
        const isValid = !isNaN(edad) && edad >= 18 && edad <= 120;
        
        if (edadInput.value === '') {
            edadError.textContent = '';
            edadInput.classList.remove('valid', 'invalid');
            validationState.edad = false;
        } else if (isValid) {
            edadError.textContent = '';
            edadInput.classList.remove('invalid');
            edadInput.classList.add('valid');
            validationState.edad = true;
        } else if (edad < 18) {
            edadError.textContent = 'Debe ser mayor o igual a 18 años';
            edadInput.classList.remove('valid');
            edadInput.classList.add('invalid');
            validationState.edad = false;
        } else if (edad > 120) {
            edadError.textContent = 'Por favor, ingrese una edad válida';
            edadInput.classList.remove('valid');
            edadInput.classList.add('invalid');
            validationState.edad = false;
        } else {
            edadError.textContent = 'Por favor, ingrese una edad válida';
            edadInput.classList.remove('valid');
            edadInput.classList.add('invalid');
            validationState.edad = false;
        }
        
        updateValidCount();
        checkAllFieldsValid();
        return isValid;
    }
    
    // Función para mostrar mensaje de éxito
    function showSuccessMessage() {
        statusMessage.textContent = '¡Formulario enviado con éxito! Todos los campos son válidos.';
        statusMessage.classList.remove('success'); // Remover primero para reiniciar animación
        void statusMessage.offsetWidth; // Truco para reiniciar animación
        statusMessage.classList.add('success');
        
        // Ocultar mensaje después de 5 segundos
        setTimeout(() => {
            statusMessage.classList.remove('success');
        }, 5000);
    }
    
    // Función para reiniciar el formulario
    function resetForm() {
        form.reset();
        
        // Limpiar clases de validación
        const inputs = [nombreInput, emailInput, passwordInput, confirmPasswordInput, edadInput];
        inputs.forEach(input => {
            input.classList.remove('valid', 'invalid');
        });
        
        // Limpiar mensajes de error
        const errorMessages = [nombreError, emailError, passwordError, confirmPasswordError, edadError];
        errorMessages.forEach(error => {
            error.textContent = '';
        });
        
        // Resetear indicador de fuerza de contraseña
        strengthFill.style.width = '0%';
        strengthText.textContent = 'Seguridad de la contraseña';
        strengthText.style.color = '#7f8c8d';
        
        // Resetear estado de validación
        Object.keys(validationState).forEach(key => {
            validationState[key] = false;
        });
        
        // Actualizar contador y deshabilitar botón
        updateValidCount();
        submitBtn.disabled = true;
        
        // Ocultar mensaje de éxito si está visible
        statusMessage.classList.remove('success');
        
        // Restaurar iconos de visibilidad de contraseña
        const toggleIcons = document.querySelectorAll('.toggle-password i');
        toggleIcons.forEach(icon => {
            icon.className = 'fas fa-eye';
        });
        
        // Restaurar tipo de input de contraseñas
        passwordInput.setAttribute('type', 'password');
        confirmPasswordInput.setAttribute('type', 'password');
    }
    
    // Event Listeners para validación en tiempo real
    nombreInput.addEventListener('input', validateNombre);
    nombreInput.addEventListener('blur', validateNombre);
    
    emailInput.addEventListener('input', validateEmail);
    emailInput.addEventListener('blur', validateEmail);
    
    passwordInput.addEventListener('input', validatePassword);
    passwordInput.addEventListener('blur', validatePassword);
    
    confirmPasswordInput.addEventListener('input', validateConfirmPassword);
    confirmPasswordInput.addEventListener('blur', validateConfirmPassword);
    
    edadInput.addEventListener('input', validateEdad);
    edadInput.addEventListener('blur', validateEdad);
    
    // Event Listeners para mostrar/ocultar contraseñas
    togglePasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility(passwordInput, togglePasswordBtn);
    });
    
    toggleConfirmPasswordBtn.addEventListener('click', function() {
        togglePasswordVisibility(confirmPasswordInput, toggleConfirmPasswordBtn);
    });
    
    // Event Listener para el botón de reinicio
    resetBtn.addEventListener('click', resetForm);
    
    // Event Listener para el envío del formulario
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        
        // Validar todos los campos una última vez
        const isNombreValid = validateNombre();
        const isEmailValid = validateEmail();
        const isPasswordValid = validatePassword();
        const isConfirmPasswordValid = validateConfirmPassword();
        const isEdadValid = validateEdad();
        
        // Si todos son válidos, mostrar mensaje de éxito
        if (isNombreValid && isEmailValid && isPasswordValid && isConfirmPasswordValid && isEdadValid) {
            showSuccessMessage();
            
            // En un caso real, aquí enviaríamos los datos al servidor
            console.log('Datos del formulario:');
            console.log('Nombre:', nombreInput.value);
            console.log('Email:', emailInput.value);
            console.log('Contraseña:', passwordInput.value);
            console.log('Edad:', edadInput.value);
            
            // Podríamos resetear el formulario después de un tiempo
            // setTimeout(resetForm, 3000);
        }
    });
    
    // Inicializar contador de campos válidos
    updateValidCount();
});