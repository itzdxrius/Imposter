function rebuildPlayerTable(players) {
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    players.forEach((player) => {
        const row = document.createElement("tr");

        const pictureCell = document.createElement("td");
        const img = document.createElement("img");
        img.src = player.picture || "";
        img.alt = "Profile Picture";
        pictureCell.appendChild(img);

        const nameCell = document.createElement("td");
        nameCell.textContent = player.name;

        row.appendChild(pictureCell);
        row.appendChild(nameCell);
        playerList.appendChild(row);
    });
}

function fetchPlayers() {
    fetch(`/get_players/${ROOM_ID}`)
        .then((res) => res.json())
        .then((data) => rebuildPlayerTable(data.players))
        .catch(() => {});
}

fetchPlayers();
setInterval(fetchPlayers, 2500);
