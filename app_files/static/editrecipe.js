// Replace img field with the uploaded file

function loadFile(event) {
    printError("rImageErr", "");
    // Check the size of the file to be under 1MB
    const file = document.getElementById("file_upload");
    if (file.files[0].size > 5242880) {
      printError("rImageErr", "Your image size has to be under 5MB.");
      file.value = "";
    } else {
      // Load the file on the page
      const image = document.getElementById("image-display");
      image.src = URL.createObjectURL(event.target.files[0]);
    }
    
}

//Add new imput field for ingredients and remove button for each

function removeElement(e) {

    let button

    if(e.target)
        button = e.target
    else
        button = e
    let field = button.previousElementSibling;
    let div = button.parentElement;

    div.removeChild(button);
    div.removeChild(field);
}
  
function add() {
    
    //create textbox
    let input = document.createElement('input');
    input.type = "text";
    input.setAttribute("class", "input_inline");
    input.setAttribute('placeholder', "Enter Ingredient");
    input.setAttribute("name", 'recipeIngredients')
    let ingredients = document.getElementById("ingredients");
    
    //create remove button
    let remove = document.createElement('button');
    remove.setAttribute('class', 'btn btn-danger ml-2 remove-button');
    remove.onclick = function(e) {
        removeElement(e);
    };
    remove.setAttribute("type", "button");
    remove.innerHTML = "x";
    
    //append elements
    ingredients.appendChild(input);
    ingredients.appendChild(remove);
}


//Add new imput field for categories and remove button for each

function removeCategory(e) {
  let button_cat = e.target;
  let field_cat = button_cat.previousElementSibling;
  let div_cat = button_cat.parentElement;
  let br = button_cat.nextSibling;
  div_cat.removeChild(button_cat);
  div_cat.removeChild(field_cat);
}

function add_category() {  
  //create textbox
  let input_cat = document.createElement('input');
  input_cat.type = "text";
  input_cat.setAttribute("class", "input_inline");
  input_cat.setAttribute('placeholder', "Enter Category");
  input_cat.setAttribute("name", 'recipeCategory')
  let categories = document.getElementById("categories");
  
  //create remove button
  let remove_cat = document.createElement('button');
  remove_cat.setAttribute('class', 'btn btn-danger ml-2 remove-button');
  remove_cat.onclick = function(e) {
      removeCategory(e);
  };
  remove_cat.setAttribute("type", "button");
  remove_cat.innerHTML = "x";
  
  //append elements
  categories.appendChild(input_cat);
  categories.appendChild(remove_cat);
}

// Form validation

function printError(elemId, hintMsg) {
  document.getElementById(elemId).innerHTML = hintMsg;
}

// Defining a function to validate form

function validateForm() {
  // Retrieving the values of form elements
  var recipeName = document.recipeForm.recipeName.value;
  var recipeShort = document.recipeForm.recipeShort.value;
  var recipePrepTime = document.recipeForm.recipePrepTime.value;
  var recipeCookingTime = document.recipeForm.recipeCookingTime.value;
  var recipePortions = document.recipeForm.recipePortions.value;
  var recipeDirections = document.recipeForm.recipeDirections.value;

  // Retrevieng the value of the ingredients added dynamically
  let allIngredients = document.getElementById("ingredients");
  let ingredientsNr = allIngredients.getElementsByTagName("input").length;
  let ingredientList = allIngredients.getElementsByTagName("input")

  let rIngredErr = false;
  for (let i = 0; i < ingredientsNr; i++) {
    if (ingredientList[i].value == ""){
      rIngredErr = true;
      printError("rIngredErr", "Please enter ingredient for each field or remove the field")      
      break;
    } else {
      printError("rIngredErr", "");
      rIngredErr = false;
    }

  }

   // Retrevieng the value of the categories added dynamically
   let allCategories = document.getElementById("categories");
   let categoriesNr = allCategories.getElementsByTagName("input").length;
   let categoryList = allCategories.getElementsByTagName("input")
 
   let rCategErr = false;
   for (let i = 0; i < categoriesNr; i++) {
     if (categoryList[i].value == ""){
       rCategErr = true;
       printError("rCategErr", "Please enter category name for each field or remove the field")      
       break;
     } else {
       printError("rCategErr", "");
       rCategErr = false;
     }
 
   }

  
  // Defining error variables with a default value
  let rNameErr = rShortErr = rPrepErr = rCookingErr = rPortionsErr = rDirectionsErr = true;

  // Validate recipe name
  if (recipeName == "") {
      printError("rNameErr", "Please enter a recipe name");
  } else {
      printError("rNameErr", "");
      rNameErr = false;        
  }

  // Validate recipe Short Description 
  if (recipeShort == "") {
      printError("rShortErr", "Please enter a short description");
  } else {
      printError("rShortErr", "");
      rShortErr = false;   
  }

  // Validate recipe Prep Time
  if (recipePrepTime == "") {
      printError("rPrepErr", "Please enter prep time");
  } else {
      printError("rPrepErr", "");
      rPrepErr = false;  
  }

  // Validate recipe Cooking Time
  if (recipeCookingTime == "") {
      printError("rCookingErr", "Please enter cooking time");
  } else {
      printError("rCookingErr", "");
      rCookingErr = false;  
  }

  // Validate recipe portions
  if (recipePortions < 1) {
      printError("rPortionsErr", "Please enter a valid number of portions");
  } else {
      printError("rPortionsErr", "");
      rPortionsErr = false;  
  }

  // Validate directions
  if (recipeDirections == "") {
      printError("rDirectionsErr", "Please enter directions");
  } else {
      printError("rDirectionsErr", "");
      rDirectionsErr = false;  
  }


  // Prevent the form from being submitted if there are any errors
  if ((rNameErr || rShortErr || rPrepErr || rCookingErr || rPortionsErr || rDirectionsErr || rIngredErr || rCategErr) === true) {
    return false;
  }
}