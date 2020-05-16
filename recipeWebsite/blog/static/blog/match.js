let password = document.getElementById('password')
let password_conf = document.getElementById('password_conf')
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