const login_button = document.getElementById("login-button");
const join_button = document.getElementById("join-button");
const replay_button = document.getElementById("replay-button");
const home_button = document.getElementById("home-button");
const start_button = document.getElementById("start-button");
const results_button = document.getElementById("results-button");
const profile_button = document.getElementById("profile-button");
const profile_back_button = document.getElementById("profile-back-button");
const vote_button = document.getElementById("vote-button");
if (login_button) {
login_button.addEventListener("click", () => {
    window.location.href = "/auth/login";
});
}
function joinLobbyThenNavigate() {
    fetch("/join_lobby", { method: "POST" }).then(() => {
        window.location.href = "/lobby";
    });
}

if (join_button) {
join_button.addEventListener("click", joinLobbyThenNavigate);
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
replay_button.addEventListener("click", joinLobbyThenNavigate);
}
if (home_button) {
home_button.addEventListener("click", () => {
    window.location.href = "/home";
});
}

if (profile_button) {
profile_button.addEventListener("click", () => {
    window.location.href = "/profile";
});
}

if (profile_back_button) {
profile_back_button.addEventListener("click", () => {
    window.location.href = "/home";
});
}

if (vote_button) {
vote_button.addEventListener("click", () => {
    window.location.href = "/vote";
});
}