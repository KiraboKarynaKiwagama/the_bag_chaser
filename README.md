# Remote Job Finder

A simple web app that lets users search, filter, and sort live remote job
listings, pulled in real time from the Remotive job board API. Built as a
practical tool for actually finding remote work.

## Why this project

Job searching across scattered listing sites is tedious. This app pulls
real, current remote job postings into one place and lets the user narrow
them down by keyword and category, and sort by what matters to them
(newest first, company name, or job title).

## Features

- Live search by job title/keyword
- Filter by job category (software dev, design, marketing, etc.)
- Sort results by date posted, company name, or job title
- Clear error messages if the job listings service is slow, down, or
  returns no matches — the app never just shows a blank or broken page

## Tech stack

- **Backend:** Python, using only the standard library (`http.server`,
  `urllib`, `json`). no external frameworks or installs required
- **Frontend:** plain HTML, CSS, and JavaScript
- **Data source:** [Remotive API](https://remotive.com/api/remote-jobs)

## API used and credit

This project uses the **Remotive API** (https://remotive.com), a free,
public API for remote job listings, maintained by Remotive.
Documentation: https://github.com/remotive-com/remote-jobs-api

**This API does not require an API key or any authentication** — it's
fully open, so there are no credentials to provide for this project.

## Running it locally

No installation step is needed — the backend uses only Python's built-in
libraries.

1. Clone this repository:
   ```
   git clone https://github.com/KiraboKarynaKiwagama/the_bag_chaser.git
   cd the_bag_chaser
   ```
2. Make sure you have Python 3 installed (`python3 --version` to check).
3. Run the server:
   ```
   python3 server.py
   ```
4. Open your browser and go to:
   ```
   http://localhost:5000
   ```
5. Search for a job title (e.g. "developer"), optionally pick a category,
   and hit Search.

## Project structure

```
.
├── server.py           # Backend: serves the page and calls the Remotive API
├── public/
│   ├── index.html       # The page itself
│   ├── style.css        # Styling
│   └── script.js        # Handles search, sorting, and rendering results
└── .gitignore
```

## Deployment

<!--
Fill this section in once deployment is done. Suggested structure below —
replace the placeholders with what you actually did.
-->

The application is deployed on two web servers (Web01 and Web02) behind a
load balancer (Lb01), which distributes incoming traffic between them.

**Steps taken:**
1. Pushed the code to this GitHub repository.
2. On both Web01 and Web02, connected via SSH and ran:
   ```
    
    git clone https://github.com/KiraboKarynaKiwagama/the_bag_chaser.git

   cd the_bag_chaser
   python3 server.py
   ```
   (kept running in the background using `[TOOL YOU USED, e.g. pm2 / nohup / systemd]`)
3. Configured Lb01 (`[Nginx / HAProxy]`) to forward incoming traffic evenly
   between Web01 (`[IP ADDRESS]`) and Web02 (`[IP ADDRESS]`).
4. Verified traffic was being split between both servers by
   `[HOW YOU VERIFIED — e.g. checking each server's logs while refreshing
   the load balancer's address repeatedly]`.

**Live application (via load balancer):** `[LOAD BALANCER URL]`

## Challenges faced

<!--
Write 2-4 sentences here, specific to what actually happened to you.
For example, mention the SSH "public key" / connection timeout issue you
ran into, and how you resolved it. Specific, real details here will make
this section stronger than generic statements.
-->

## Demo video

`[LINK TO YOUR DEMO VIDEO]`

## Credits

- Job data: [Remotive](https://remotive.com) via their public API
- Built with Python's standard library and vanilla JavaScript