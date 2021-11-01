const typeHandler = () => {
    let type = document.getElementById("form_run_type").value;
    let period = document.getElementById("div_id_period");
    let end = document.getElementById("div_id_end");
    switch(type) {
        case "Once":
            if (!period.classList.contains('myform-hidden'))
                period.classList.add('myform-hidden');
            if (!end.classList.contains('myform-hidden'))
                end.classList.add('myform-hidden');
            break;
        case "Unlimited":
            if (period.classList.contains('myform-hidden'))
                period.classList.remove('myform-hidden');
            if (!end.classList.contains('myform-hidden'))
                end.classList.add('myform-hidden');
            break;
        case "Until":
            if (period.classList.contains('myform-hidden'))
                period.classList.remove('myform-hidden');
            if (end.classList.contains('myform-hidden'))
                end.classList.remove('myform-hidden');
            break;
    }
}
