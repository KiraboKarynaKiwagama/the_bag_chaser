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
   (kept running in the background using `nohup` so the app stays alive after disconnecting from ssh)
3. Configured Lb01 using **HAProxy**, editing `/etc/haproxy/haproxy.cfg`
   to load balance between Web01 (`13.49.125.58`) and Web02
   (`54.159.207.54`) using the `roundrobin` algorithm, then restarted
   the service with `sudo systemctl restart haproxy`.
4. 4. Verified traffic was being split between both servers by temporarily
   editing the heading in Web02's `index.html` file so it displayed
   differently from Web01. I initially tried to verify this by watching
   each server's `server.log` file live in the terminal, but ran into
   issues tracking the logs this way. Switching to the visual heading
   difference was a more reliable way to confirm behavior: repeatedly
   refreshing the load balancer's address in Chrome showed the heading
   alternating between the two versions, confirming HAProxy was
   genuinely distributing requests across both servers rather than
   always hitting the same one.

**Live application (via load balancer):** `http://34.227.16.186`

## Challenges faced

The biggest challenge was server access. My originally-assigned Web01
became unreachable partway through the project — SSH connections timed
out entirely, with no response from the server. After confirming this
wasn't a mistake on my end (wrong key, wrong command), I worked around
it by launching a replacement server on AWS EC2, installing the same
dependencies, and pointing the load balancer at its address instead.

I also found that Web02 came with nginx pre-installed and already bound
to port 80, which conflicted with my own app trying to use that same
port. I resolved this by stopping and disabling the nginx service before
starting my own server.

Tracking whether the load balancer was actually splitting traffic
between both servers was tricky at first, since both servers were
running the exact same app and looked identical from the outside. I
solved this by temporarily editing the heading in Web02's HTML file, so
that refreshing the load balancer's address in Chrome would visibly
alternate between the two versions, confirming both servers were
genuinely being used.

I also ran into a confusing moment testing external access from a family
member's laptop: I initially typed "https" instead of "http" in the
address bar by mistake, which made it look like a firewall was blocking
the connection entirely. After realizing the typo and correcting it, I
was able to properly test — and confirmed the load balancer works
correctly from within the school's network, but external requests from
outside networks do time out, which appears to be a network-level
restriction rather than an application issue.

## Demo video

`[LINK TO YOUR DEMO VIDEO]`

## Credits

- Job data: [Remotive](https://remotive.com) via their public API
- Built with Python's standard library and vanilla JavaScript