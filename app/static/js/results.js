const resultsContent = document.getElementById("results-content");

const OUTCOME_MESSAGES = {
    "imposter wins": "The imposter got away with it!",
    "players win": "The players caught the imposter!",
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
        resultsContent.appendChild(img);
    }

    const wordEl = document.createElement("p");
    wordEl.textContent = `The word was: ${data.word}`;
    resultsContent.appendChild(wordEl);

    const imposterEl = document.createElement("p");
    imposterEl.textContent = `The imposter was: ${data.imposter_name}`;
    resultsContent.appendChild(imposterEl);

    const outcomeEl = document.createElement("p");
    outcomeEl.textContent = OUTCOME_MESSAGES[data.outcome] || data.outcome;
    resultsContent.appendChild(outcomeEl);
}

loadResults();
