let password = document.getElementById('id_new_password1')
let password_conf = document.getElementById('id_new_password2')
function validate_password(){
    if (password.value !== password_conf.value){
        password_conf.setCustomValidity("Your passwords don't match")
    }
    else{
        password_conf.setCustomValidity('')
    }
}
password.onchange = validate_password
password_conf.onkeyup = validate_password