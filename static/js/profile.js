//Profile.html

const editBtn = $('#edit_btn');
const profileBtn = $('#profile_btn');
const saveBtn = $('#save_btn');
const deleteBtn = $('#delete_btn')
const showSection = $('#show_section');
const editSection = $('#edit_section');
const profileSection = $('#profile_section');
const saveSection = $('#recipes_section')
const deleteSection = $('#delete_section')
const deleteAccount = $('#btn_delete')



$(document).ready(function () {
    //on page load, show profile card
    hideAll()
    profileSection.show()
})


saveBtn.on('click', (e) => {
    hideSections(e)
    //show saved recipes section
    saveSection.show()
})


editBtn.on('click', (e) => {
    hideSections(e)
    //show edit profile section 
    editSection.show();
})


profileBtn.on('click', (e) => {
    hideSections(e)
    //show profile card
    profileSection.show()
})


deleteBtn.on('click', (e) => {
    hideSections(e)
    //show delete account section 
    deleteSection.show()
})



function hideSections(e) {
    //hide all sections and stop default event behavior
    e.preventDefault();
    showSection.hide()
    editSection.hide()
    profileSection.hide()
    saveSection.hide()
    deleteSection.hide()
}


function hideAll() {
    //hide all sections 
    showSection.hide()
    editSection.hide()
    profileSection.hide()
    saveSection.hide()
    deleteSection.hide()
}


$("#menu-toggle").click(function (e) {
    //Stop event behavior and toggle menu btn;
    // on click show/hide side wrapper 
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
});