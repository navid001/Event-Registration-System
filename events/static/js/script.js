
document.addEventListener("DOMContentLoaded", function () {
  const togglePasswordIcons = document.querySelectorAll('.toggle-password');
  togglePasswordIcons.forEach(icon => {
      icon.addEventListener('click', function () {
          const targetInput = document.querySelector(icon.getAttribute('toggle'));
          if (targetInput.type === 'password') {
              targetInput.type = 'text';
          } else {
              targetInput.type = 'password';
          }
          icon.classList.toggle('fa-eye');
          icon.classList.toggle('fa-eye-slash');
      });
  });

  const password2Input = document.getElementById('id_password2');
  if (password2Input) {
      password2Input.addEventListener('keyup', function () {
          const password1 = document.getElementById('id_password1').value;
          const password2 = this.value;
          const passwordMatchError = document.getElementById('password-match-error');
          if (password1 !== password2) {
              passwordMatchError.style.display = 'block';
          } else {
              passwordMatchError.style.display = 'none';
          }
      });
  }

  const usernameInput = document.getElementById('id_username');
  if (usernameInput) {
      usernameInput.addEventListener('keyup', function () {
          const username = this.value;
          const uniqueUsernameError = document.getElementById('unique-username-error');
      });
  }

});

const registrationForm = document.querySelector('.registration-form');
if (registrationForm) {
  registrationForm.addEventListener('submit', function (event) {
      const confirmed = confirm('Are you sure you want to register for this event?');
      if (!confirmed) {
          event.preventDefault();
      }
  });
}
