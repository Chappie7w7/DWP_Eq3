document.addEventListener('DOMContentLoaded', function () {
    var recoveryMethod = document.getElementById('recoveryMethod');
    var emailForm = document.getElementById('emailForm');
    var phoneForm = document.getElementById('phoneForm');
    var questionsForm = document.getElementById('questionsForm');
    var forgotPasswordForm = document.getElementById('forgotPasswordForm');

    // Obtén las URLs desde los atributos data-*
    var emailUrl = forgotPasswordForm.getAttribute('data-email-url');
    var phoneUrl = forgotPasswordForm.getAttribute('data-phone-url');
    var questionsUrl = forgotPasswordForm.getAttribute('data-questions-url');

    recoveryMethod.addEventListener('change', function () {
        var selectedMethod = this.value;

        if (selectedMethod === 'email') {
            emailForm.style.display = 'block';
            phoneForm.style.display = 'none';
            questionsForm.style.display = 'none';
            forgotPasswordForm.action = emailUrl; // Usa la URL para correo
        } else if (selectedMethod === 'phone') {
            phoneForm.style.display = 'block';
            emailForm.style.display = 'none';
            questionsForm.style.display = 'none';
            forgotPasswordForm.action = phoneUrl; // Usa la URL para teléfono
        } else if (selectedMethod === 'preguntas') {
            questionsForm.style.display = 'block';
            emailForm.style.display = 'none';
            phoneForm.style.display = 'none';
            forgotPasswordForm.action = questionsUrl; // Usa la URL para preguntas de seguridad
        } else {
            emailForm.style.display = 'none';
            phoneForm.style.display = 'none';
            questionsForm.style.display = 'none';
        }
    });
});
