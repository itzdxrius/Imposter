const socket = new WebSocket(`ws://${location.hostname}:8765`);

socket.addEventListener("open", () => {
    socket.send(JSON.stringify({ type: "join", room_id: ROOM_ID, user_id: USER_ID }));
});

socket.addEventListener("message", (event) => {
    const data = JSON.parse(event.data);
    if (data.type !== "player_list_update") return;

    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    data.players.forEach((player) => {
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
});
