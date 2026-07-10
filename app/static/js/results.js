const resultsContent = document.getElementById("results-content");

const OUTCOME_MESSAGES = {
    "imposter wins": "Imposter Wins!",
    "players win": "Civilians Win!",
    tie: "It was a tie — no one was voted out.",
    "everyone skipped": "Everyone skipped — no one was voted out.",
    "No votes cast": "No votes were cast.",
};

async function loadResults() {
    const response = await fetch(`/get_round_results/${ROUND_ID}`);
    const data = await response.json();

    if (!data.outcome) {
        resultsContent.textContent = "Waiting for the round to finish...";
        return;
    }

    resultsContent.innerHTML = "";

    if (data.reveal_image_url) {
        const img = document.createElement("img");
        img.src = data.reveal_image_url;
        img.alt = data.word;
        img.classList.add("result-reveal-image");
        resultsContent.appendChild(img);
    }

    const wordEl = document.createElement("p");
    wordEl.textContent = `The word was: ${data.word}`;
    wordEl.classList.add("body-text", "result-word");
    resultsContent.appendChild(wordEl);

    if (data.voted_out_name) {
        const votedOutEl = document.createElement("p");
        votedOutEl.textContent = `${data.voted_out_name} was voted out.`;
        votedOutEl.classList.add("body-text", "result-voted-out");
        resultsContent.appendChild(votedOutEl);
    }

    const outcomeEl = document.createElement("p");
    outcomeEl.textContent = OUTCOME_MESSAGES[data.outcome] || data.outcome;
    outcomeEl.classList.add("body-text", "result-outcome");
    resultsContent.appendChild(outcomeEl);
}

loadResults();
