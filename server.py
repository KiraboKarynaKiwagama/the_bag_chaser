import http.server
import socketserver
import urllib.request
import urllib.parse
import urllib.error
import json
import functools

 
PORT = 5000
PUBLIC_FOLDER = "public"  #where index.html, style.css, script.js live

REMOTIVE_API_URL = "https://remotive.com/api/remote-jobs"
 
 
class RequestHandler(http.server.SimpleHTTPRequestHandler):
   
    def do_GET(self):
        #self.path is whatever the browser asked for
        parsed_url = urllib.parse.urlparse(self.path)
 
        if parsed_url.path == "/api/jobs":
            self.handle_jobs_request(parsed_url)
        else:
            super().do_GET()
 
    def handle_jobs_request(self, parsed_url):
        """
        Reads ?search=...&category=... from the URL the browser called,
        asks Remotive for matching jobs, and sends the result back as JSON.
        """
        # parse_qs turns "search=developer&category=design" into a dictionary
        query_params = urllib.parse.parse_qs(parsed_url.query)
        search_term = query_params.get("search", [""])[0]
        category = query_params.get("category", [""])[0]
 
        # Build the URL used to actually call on Remotive's side
        api_params = {}
        if search_term:
            api_params["search"] = search_term
        if category:
            api_params["category"] = category
 
        request_url = REMOTIVE_API_URL
        if api_params:
            request_url += "?" + urllib.parse.urlencode(api_params)
 
        try:
            req = urllib.request.Request(
                request_url,
                headers={"User-Agent": "job-finder-app"}
            )
 
            with urllib.request.urlopen(req, timeout=10) as response:
                raw_data = response.read()
                data = json.loads(raw_data)
 
            # We only keep the fields our page actually displays, trimmed down from everything Remotive sends us.
            jobs = []
            for job in data.get("jobs", []):
                jobs.append({
                    "title": job.get("title"),
                    "company": job.get("company_name"),
                    "location": job.get("candidate_required_location"),
                    "category": job.get("category"),
                    "date": job.get("publication_date"),
                    "url": job.get("url"),
                })
 
            self.send_json_response({"success": True, "jobs": jobs}, status=200)
 
        except urllib.error.URLError:
            #covers no internet, Remotive is down, DNS failure, timeout,.
            self.send_json_response({
                "success": False,
                "error": "Could not reach the job listings service right now. Please try again shortly."
            }, status=502)
 
        except json.JSONDecodeError:
            #covers Remotive responded, but not with valid JSON.
            self.send_json_response({
                "success": False,
                "error": "Received an unexpected response from the job listings service."
            }, status=502)
 
        except Exception:
            self.send_json_response({
                "success": False,
                "error": "Something went wrong on our end. Please try again."
            }, status=500)
 
    def send_json_response(self, data, status=200):
        """Small helper: turns a Python dictionary into a proper JSON HTTP response."""
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
 
    def log_message(self, format, *args):
        #keeps the terminal output clean while the server runs.
        print(f"[{self.address_string()}] {format % args}")
 
 
#functools.partial "pre-fills" the directory argument, so our handler always serves files from the "public" folder specifically
Handler = functools.partial(RequestHandler, directory=PUBLIC_FOLDER)
 
if __name__ == "__main__":
    #ThreadingTCPServer lets the server handle more than one visitor at the same time, instead of making people wait in line one by one.
    with socketserver.ThreadingTCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Server running: http://localhost:{PORT}")
        print("Press Ctrl+C to stop.")
        httpd.serve_forever()