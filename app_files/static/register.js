// form validation

function printError(elemId, hintMsg) {
    document.getElementById(elemId).innerHTML = hintMsg;
}
  
// Defining a function to validate form
  
function validateForm() {
    // Retrieving the values of form elements
    var name = document.contactForm.username.value;
    var psw = document.contactForm.password.value;
    var confirm = document.contactForm.confirmation.value;
  
    // Defining error variables with a default value
    var nameErr = pswErr = confirmErr = true;

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
        if (psw.match(/[a-z]/g) && psw.match(/[A-Z]/g) && psw.match(/[0-9]/g) && psw.length >= 8){ //&& psw.match(/[^a-zA-Z\d]/g) for special characters
            printError("pswErr", "");
            pswErr = false;
        } else {
            printError("pswErr", "A password must contain minimum 8 characters: at least 1 uppercase, 1 lowercase, 1 digit, 1 special character.")
        } 
    }

    //Validate password confirmation
    if (confirm == "") {
        printError("confirmErr", "Please confirm your password");
    } else {
        if (confirm != psw) {
            printError("confirmErr", "Your passwords do not match");
        } else {
            printError("confirmErr", "");
            confirmErr = false; 
        }
    }
  
    // Prevent the form from being submitted if there are any errors
    if ((nameErr || pswErr || confirmErr) === true) {
      return false;
    }
}