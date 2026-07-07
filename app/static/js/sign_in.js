function handleLogin() {
    window.location.href = "/auth/login";
}
const login_button = document.getElementById("login-button");
login_button.addEventListener("click", handleLogin);