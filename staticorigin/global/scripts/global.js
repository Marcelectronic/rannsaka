// Event listener for the language select element
let select_ln = document.getElementById("language_select");
if (select_ln)
    select_ln.addEventListener("change", (e) => {
        document.getElementById("language_form").submit();
    } );
// Event listener for the dark mode element
let night_sw = document.getElementById("night-switch");
if (night_sw)
    night_sw.addEventListener("click", (e) => {
        document.getElementById("night_form").submit();
    } );
// Event listener for the colapsed menu btn
let select_menubtn = document.getElementById("menu-btn");
if (select_menubtn)
    select_menubtn.addEventListener("click", (e) => {
        document.getElementById("extra-btns").classList.toggle("hide-menu-btns")
    } );
