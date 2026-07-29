let totalVotes = 0;

document.addEventListener("DOMContentLoaded", () => {

    // ==========================
    // TRIP TITLE LOGIC
    // ==========================
    const tripTitleBtn = document.getElementById("tripTitleBtn");

    tripTitleBtn.addEventListener("click", () => {

        const input = document.createElement("input");
        input.className = "trip-title-input";
        input.placeholder = "Enter trip title";

        tripTitleBtn.replaceWith(input);

        input.focus();

        input.addEventListener("blur", () => {

            if (input.value.trim() === "") {
                input.focus();
                return;
            }

            const title = document.createElement("div");
            title.className = "trip-title-display";
            title.textContent = input.value.trim();

            input.replaceWith(title);
        });

    });


    // ==========================
    // POLL OPTION LOGIC
    // ==========================
    const addBtn = document.getElementById("addLocationBtn");
    const pollOptions = document.getElementById("poll-options");

    addBtn.addEventListener("click", () => {

        const existingInput = document.querySelector(".location-input");

        if (existingInput && existingInput.value.trim() === "") {
            existingInput.focus();

            existingInput
                .closest(".location-content")
                .classList.add("invalid");

            return;
        }

        const option = document.createElement("div");
        option.classList.add("poll-option");

        option.innerHTML = `
            <div class="option-top">

                <input type="radio" name="location" class="location-radio">

                <div class="location-content">

                    <input
                        type="text"
                        class="location-input"
                        placeholder="Enter location"
                    >

                    <div class="error-msg">
                        Location name can't be empty
                    </div>

                </div>

                <div class="vote-container hidden">
                    <div class="vote-bar">
                        <div class="vote-fill"></div>
                    </div>
                    <span class="vote-percent">0%</span>
                </div>

            </div>

            <div class="location-details">

                <div class="details-box">

                    <div class="detail-line">
                        Distance: --
                    </div>

                    <div class="detail-line">
                        Avg. Cost: --
                    </div>

                    <div class="summary-line">
                        <strong>Summary:</strong>
                        <p class="summary-text">Loading...</p>
                    </div>

                </div>

            </div>
        `;

        pollOptions.appendChild(option);

        const radio = option.querySelector(".location-radio");
        const locationInput = option.querySelector(".location-input");
        const locationContent = option.querySelector(".location-content");

        locationInput.focus();

        // ==========================
        // Voting
        // ==========================
        radio.addEventListener("change", () => {

            totalVotes++;

            option.dataset.votes =
                (parseInt(option.dataset.votes || 0) + 1);

            document.querySelectorAll(".poll-option").forEach(opt => {

                const voteContainer = opt.querySelector(".vote-container");

                const votes = parseInt(opt.dataset.votes || 0);

                const percentage =
                    totalVotes > 0
                        ? Math.round((votes / totalVotes) * 100)
                        : 0;

                opt.querySelector(".vote-fill").style.width = `${percentage}%`;
                opt.querySelector(".vote-percent").textContent = `${percentage}%`;

                if (votes > 0)
                    voteContainer.classList.remove("hidden");

                opt.classList.remove("selected");
            });

            option.classList.add("selected");

        });

        // ==========================
        // Fetch city info
        // ==========================
        locationInput.addEventListener("blur", async () => {

            if (locationInput.value.trim() === "") {
                locationContent.classList.add("invalid");
                return;
            }

            locationContent.classList.remove("invalid");

            const locationName = locationInput.value.trim();

            // <-- NEW: read vibe from the top input
            const preference =
                document.getElementById("vibe").value.trim();

            try {

                const response = await fetch(
                    "http://127.0.0.1:8000/location_info",
                    {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            name: locationName,
                            current_city: document.getElementById("startLocation").value.trim(),
                            preference: preference
                        })
                    }
                );

                if (!response.ok) {
                    alert("Failed to fetch travel information.");
                    return;
                }

                const data = await response.json();

                console.log("Backend response:", data);

                const locationNameDiv = document.createElement("div");
                locationNameDiv.className = "location-name";
                locationNameDiv.textContent = locationName;

                locationInput.replaceWith(locationNameDiv);

                option.querySelector(".detail-line:nth-child(1)").textContent =
                    `Distance: ${data.distance}`;

                option.querySelector(".detail-line:nth-child(2)").textContent =
                    `Avg. Cost: ${data.avg_cost}`;

                option.querySelector(".summary-text").textContent =
                    data.summary || "No summary available.";

            } catch (err) {

                console.error(err);

                option.querySelector(".summary-text").textContent =
                    "Failed to load summary.";

            }

        });

    });

});