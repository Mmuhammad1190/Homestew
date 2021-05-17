//Home.html 
const menu_row = $('#menu_row')
const menu_items = ['appetizer', 'bread', 'breakfast', 'dessert', 'main_course', 'salad', 'side', 'soup']


if (menu_row) {
    //if row is visible, remove previously appended elements
    menu_row.empty()
    //for each item in array, make and append html card to row 
    menu_items.forEach((item) => {
        makeHTML(item)
    })
}


function makeHTML(item) {
    //remove underscore from item string; styling for heading text 
    let newItem = removeUnderScore(item)

    //make html card
    let card =
        `<div class="col-sm-6 col-md-3 col-lg-3">
        <a href="/recipes/browse/${item}">
            <div class="d-flex mx-auto align-items-center menu_img justify-content-center" style="background: linear-gradient(#39393b6a, #39393b6a), url('/static/images/${item}.jpg')">
                <p class="text-white h3 text-uppercase">${newItem}</p>
            </div>
        </a>
    </div>`
    menu_row.append(card)
    return card
}

function removeUnderScore(item) {
    //remove underscore from string and replace with space
    return item.split('_').join(' ')
}