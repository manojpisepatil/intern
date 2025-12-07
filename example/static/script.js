// Handle form submission
document.getElementById('signup-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent the default form submission behavior
  
    const name = document.getElementById('name').value;
    const email = document.getElementById('email').value;
  
    if (name && email) {
      alert(`Thank you for signing up, ${name}! We will send updates to ${email}.`);
      // Clear the form
      document.getElementById('signup-form').reset();
    } else {
      alert('Please fill in all fields.');
    }
  });
  