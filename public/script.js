// script.js
// This file runs in the user's browser. Its job:
//   1. Wait for the user to click "Search"
//   2. Call OUR OWN backend (/api/jobs) — not Remotive directly
//   3. Take the jobs we get back and display them
//   4. Apply sorting based on the dropdown, entirely in the browser

// Grab references to the HTML elements we'll need to read from / write to
const searchInput = document.getElementById("searchInput");
const categorySelect = document.getElementById("categorySelect");
const sortSelect = document.getElementById("sortSelect");
const searchButton = document.getElementById("searchButton");
const statusMessage = document.getElementById("statusMessage");
const resultsContainer = document.getElementById("resultsContainer");

// Keep the most recent set of jobs in memory so we can re-sort them
// without re-fetching from the server every time the sort dropdown changes.
let currentJobs = [];

//to let users search by pressing enter and also by clicking the search button
searchButton.addEventListener("click", fetchJobs);
searchInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        fetchJobs();
    }
});

//re-sort instantly when the sort dropdown changes with no need to re-fetch
sortSelect.addEventListener("change", () => {
    renderJobs(sortJobs(currentJobs));
});

async function fetchJobs() {
    const search = searchInput.value.trim();
    const category = categorySelect.value;

    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (category) params.append("category", category);

    statusMessage.textContent = "Loading jobs...";
    resultsContainer.innerHTML = "";

    try {
        const response = await fetch(`/api/jobs?${params.toString()}`);
        const data = await response.json();

        if (!data.success) {
            statusMessage.textContent = data.error || "Something went wrong.";
            return;
        }

        currentJobs = data.jobs;

        if (currentJobs.length === 0) {
            statusMessage.textContent = "No jobs found. Try a different search.";
            return;
        }

        statusMessage.textContent = `Found ${currentJobs.length} job(s).`;
        renderJobs(sortJobs(currentJobs));

    } catch (error) {
        //this runs if the network request itself failed entirely
        statusMessage.textContent = "Could not connect to the server. Please try again.";
    }
}

function sortJobs(jobs) {
    const sorted = [...jobs];
    const sortBy = sortSelect.value;

    if (sortBy === "company") {
        sorted.sort((a, b) => (a.company || "").localeCompare(b.company || ""));
    } else if (sortBy === "title") {
        sorted.sort((a, b) => (a.title || "").localeCompare(b.title || ""));
    } else {
        // Default: newest first
        sorted.sort((a, b) => new Date(b.date) - new Date(a.date));
    }

    return sorted;
}

function renderJobs(jobs) {
    resultsContainer.innerHTML = "";

    jobs.forEach((job) => {
        const card = document.createElement("div");
        card.className = "job-card";

        card.innerHTML = `
            <h3>${escapeHtml(job.title || "Untitled role")}</h3>
            <div class="meta">
                ${escapeHtml(job.company || "Unknown company")}
                &middot; ${escapeHtml(job.location || "Location not specified")}
                &middot; ${job.date ? new Date(job.date).toLocaleDateString() : ""}
            </div>
            <a href="${job.url}" target="_blank" rel="noopener">View listing &rarr;</a>
        `;

        resultsContainer.appendChild(card);
    });
}

//small safety helper prevents job titles/companies containing HTML-like text from breaking the page or injecting unexpected code into it.
function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}