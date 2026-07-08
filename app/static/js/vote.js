const voteButtons = document.querySelectorAll(".vote-button");
const skipButton = document.getElementById("skip-button");
const voteStatus = document.getElementById("vote-status");

let pollTimer = null;

function lockVoting(message) {
    voteButtons.forEach((button) => (button.disabled = true));
    skipButton.disabled = true;
    voteStatus.textContent = message;
}

async function submitVote(votedForId) {
    lockVoting("Vote submitted. Waiting for other players...");
    try {
        await fetch(`/submit_votes/${ROUND_ID}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ voted_for_id: votedForId }),
        });
    } catch (err) {
        voteStatus.textContent = "Failed to submit vote. Please try again.";
        voteButtons.forEach((button) => (button.disabled = false));
        skipButton.disabled = false;
        return;
    }
    pollForResults();
}

function pollForResults() {
    pollTimer = setInterval(async () => {
        const response = await fetch(`/get_round_results/${ROUND_ID}`);
        const data = await response.json();
        if (data.outcome) {
            clearInterval(pollTimer);
            window.location.href = "/results";
        }
    }, 2000);
}

voteButtons.forEach((button) => {
    button.addEventListener("click", () => {
        submitVote(button.dataset.playerId);
    });
});

skipButton.addEventListener("click", () => {
    submitVote(null);
});
