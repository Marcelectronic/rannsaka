let formpopup = document.getElementById("date_popup");

formpopup.addEventListener('submit', (e)=>{
    let divpopup = document.getElementById("select_date");
    let myModal = bootstrap.Modal.getInstance(divpopup);
    myModal.hide();
})