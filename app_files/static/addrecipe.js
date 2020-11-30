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
      const image = document.getElementById("recipe_image");
      image.src = URL.createObjectURL(event.target.files[0]);
    }
    
}

//Add new imput field for ingredients and remove button for each

function removeElement(e) {
    let button = e.target;
    let field = button.previousSibling;
    let div = button.parentElement;
    let br = button.nextSibling;
    div.removeChild(button);
    div.removeChild(field);
    div.removeChild(br);
    
    let allElements = document.getElementById("ingredients");
    let inputs = allElements.getElementsByTagName("input");
    for(i = 0; i < inputs.length; i++){
    	inputs[i].setAttribute('id', 'ingredients' + (i+1));
    	inputs[i].setAttribute('placeholder', "Enter Ingredient");
      inputs[i].nextSibling.setAttribute('id', 'ingredients_r' + (i+1));
    }
}
  
function add() {
    let allElements = document.getElementById("ingredients");
    let ingredients_id = allElements.getElementsByTagName("input").length;
    
    ingredients_id++;
    
    //create textbox
    let input = document.createElement('input');
    input.type = "text";
    input.setAttribute("class", "input_inline");
    input.setAttribute('id', 'ingredients' + ingredients_id);
    input.setAttribute('placeholder', "Enter Ingredient");
    input.setAttribute("name", 'recipeIngredients')
    let ingredients = document.getElementById("ingredients");
    
    //create remove button
    let remove = document.createElement('button');
    remove.setAttribute('id', 'ingredients_r' + ingredients_id);
    remove.setAttribute('class', 'btn btn-danger ml-2 remove-button');
    remove.onclick = function(e) {
        removeElement(e);
    };
    remove.setAttribute("type", "button");
    remove.innerHTML = "x";
    
    //append elements
    ingredients.appendChild(input);
    ingredients.appendChild(remove);
    let br = document.createElement("br");
    ingredients.appendChild(br);
}


//Add new imput field for categories and remove button for each

function removeCategory(e) {
  let button_cat = e.target;
  let field_cat = button_cat.previousSibling;
  let div_cat = button_cat.parentElement;
  let br = button_cat.nextSibling;
  div_cat.removeChild(button_cat);
  div_cat.removeChild(field_cat);
  div_cat.removeChild(br);
 
  let allElementsCategories = document.getElementById("categories");
  let inputsCat = allElementsCategories.getElementsByTagName("input");
  for(i=0;i<inputs.length;i++){
    inputsCat[i].setAttribute('id', 'categories' + (i+1));
    inputsCat[i].setAttribute('placeholder', "Enter Category");
    inputsCat[i].nextSibling.setAttribute('id', 'categories_r' + (i+1));
  }
}

function add_category() {
  let allElementsCategories = document.getElementById("categories");
  let category_id = allElementsCategories.getElementsByTagName("input").length;
  
  category_id++;
  
  //create textbox
  let input_cat = document.createElement('input');
  input_cat.type = "text";
  input_cat.setAttribute("class", "input_inline");
  input_cat.setAttribute('id', 'categories' + category_id);
  input_cat.setAttribute('placeholder', "Enter Category");
  input_cat.setAttribute("name", 'recipeCategory')
  let categories = document.getElementById("categories");
  
  //create remove button
  let remove_cat = document.createElement('button');
  remove_cat.setAttribute('id', 'categories_r' + category_id);
  remove_cat.setAttribute('class', 'btn btn-danger ml-2 remove-button');
  remove_cat.onclick = function(e) {
      removeCategory(e);
  };
  remove_cat.setAttribute("type", "button");
  remove_cat.innerHTML = "x";
  
  //append elements
  categories.appendChild(input_cat);
  categories.appendChild(remove_cat);
  let br = document.createElement("br");
  categories.appendChild(br);
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
  var ingredient0 = document.recipeForm.ingredient0.value;
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
  let rNameErr = rShortErr = rPrepErr = rCookingErr = rPortionsErr = rIngredientErr = rDirectionsErr = true;

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

  // Validate first ingredient
  if (ingredient0 == "") {
      printError("rIngredientErr", "Please enter ingredient");
  } else {
      printError("rIngredientErr", "");
      rIngredientErr = false;  
  }

  // Validate first ingredient
  if (recipeDirections == "") {
      printError("rDirectionsErr", "Please enter ingredient");
  } else {
      printError("rDirectionsErr", "");
      rDirectionsErr = false;  
  }


  // Prevent the form from being submitted if there are any errors
  if ((rNameErr || rShortErr || rPrepErr || rCookingErr || rPortionsErr || rIngredientErr || rDirectionsErr || rIngredErr || rCategErr) === true) {
    return false;
  }
}