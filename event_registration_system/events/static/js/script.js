// Add your custom JavaScript code here

document.addEventListener("DOMContentLoaded", function() {
    // Example: Adding a confirmation message on event registration
    const registrationForm = document.querySelector('.registration-form');
    if (registrationForm) {
      registrationForm.addEventListener('submit', function(event) {
        const confirmed = confirm('Are you sure you want to register for this event?');
        if (!confirmed) {
          event.preventDefault();
        }
      });
    }
  
    // Add more dynamic features as needed
  });
  