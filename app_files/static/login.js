//BOOK A MEETING form validation

function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
}
  
// Defining a function to validate form
  
function validateForm() {
    // Retrieving the values of form elements
    var name = document.contactForm.username.value;
    var psw = document.contactForm.password.value;
  
    // Defining error variables with a default value
    var nameErr = pswErr = true;

    // Validate name
    if (name == "") {
        printError("nameErr", "Please enter a username");
    } else {
        printError("nameErr", "");
        nameErr = false;        
    }
  
    //Validate password 
    if (psw == "") {
        printError("pswErr", "Please enter a password");
    } else {
        printError("pswErr", "");
        pswErr = false;
    }
 
    // Prevent the form from being submitted if there are any errors
    if ((nameErr || pswErr) === true) {
      return false;
    }
}