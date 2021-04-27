//Search.html

const searchForm = $('#search_form')
const resetBtn = $('.btn_delete')
const resultSpan = $('#result_span')
const searchQuery = $('#query')
const loadBtn = $('#load_btn')
const baseURL = 'https://api.spoonacular.com/recipes/'
let offset = 101;//used to load the next 100 recipes
let formData;


searchForm.on('submit', function (e) {
  // prevent page from refreshing
  e.preventDefault();

  //clear appeneded data
  $(".result_row").empty()

  // grab the data inside the form fields; set the number of results returned 
  formData = extractFormData()
  formData["number"] = 100
  console.log(formData)

  //send form data to route; call API to append search results
  axios.post('/search', formData)
    .then(function (res) {
      const recipes = res.data.results
      generateCardHTML(recipes)
      loadBtn.show()
      appendResultCount(res)
    }).catch(function (err) {
      console.log(err)
    })
})

resetBtn.on('click', (e) => {
  //reset all form inputs
  e.preventDefault()
  searchForm.trigger("reset")
})

searchQuery.keypress((e) => {
  //if enter key is pressed in search query, submit search form
  if (e.which === 13) {
    e.preventDefault()
    searchForm.submit()
  }
})

loadBtn.on('click', (e) => {
  //hide loadBtn
  loadBtn.hide()

  //append offset k,v pair to FormData obj
  formData["offset"] = offset
  offset += 100;

  //send API request with the same parameters, now including offset value
  axios.post('/search', formData)
    .then(function (res) {
      const recipes = res.data.results
      generateCardHTML(recipes)
      loadBtn.show()
      appendResultCount(res)
    }).catch(function (err) {
      console.log(err)
    })
})

const appendResultCount = function (res) {
  //append search results to page
  resultSpan.text(res.data.totalResults)
}


const extractFormData = function () {
  //tranform form data into array; append k,v pairs
  //to formData obj as parameters to call API
  let form = searchForm.serializeArray()
  let formData = {}

  form.forEach(field => {
    formData[field.name] = field.value
  });
  return formData
}


const generateCardHTML = function (recipes) {
  //generate html for each recipe in search results
  for (let i in recipes) {
    let card = `<div class="col-lg-3 col-md-4 col-sm-6">
             <div style=" background: linear-gradient(#39393b80,#39393b80), url(${recipes[i].image}) center center/cover no-repeat;"
             id="${recipes[i].id}" class="recipe_card">
                 <div class="text-center mt-4">
                     <h5 class=" recipe_card_title">${recipes[i].title}</h5>
                     <div class="mt-4 overlay_button"><a href="/search/recipes/${recipes[i].id}">VIEW RECIPE</a></div>
                 </div>
             </div>
         </div>`

    $('.result_row').append(card)
  }

}