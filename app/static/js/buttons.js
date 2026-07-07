const login_button = document.getElementById("login-button");
const join_button = document.getElementById("join-button");
const replay_button = document.getElementById("replay-button");
const home_button = document.getElementById("home-button");
const start_button = document.getElementById("start-button");
const results_button = document.getElementById("results-button");
if (login_button) {
login_button.addEventListener("click", () => {
    window.location.href = "/auth/login";
});
}
if (join_button) {
join_button.addEventListener("click", () => {
    window.location.href = "/lobby";
});
}
if (start_button) {
start_button.addEventListener("click", () => {
    window.location.href = "/game";
});
}
if (results_button) {
results_button.addEventListener("click", () => {
    window.location.href = "/results";
});
}
if (replay_button) {
replay_button.addEventListener("click", () => {
    window.location.href = "/lobby";
});
}
if (home_button) {
home_button.addEventListener("click", () => {
    window.location.href = "/home";
});
}