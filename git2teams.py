# Git2Teams
# Created by bgartamaker 03/10/2020

from flask import Flask, request
import json
import requests

app = Flask(__name__)

@app.route('/hook',methods=['POST'])
def intake():
    def msteams(teams_url, post_body):
        requests.post(url = teams_url, json = post_body )  # Sends data to teams
    data = json.loads(request.data) # Gets json body
    web_url = request.args.get('url') # Gets webhook url

    # Parses body to determine if Merge,Issue, or Push event
    if "object_kind" in data: # This parses the json body for Merge/Issue events
        object_type = data["object_kind"]
        activity_subtitle = data["object_attributes"]["title"]
        state = data["object_attributes"]["state"]
        description = data["object_attributes"]["description"]
        created_at = data["object_attributes"]["created_at"]
        updated_at = data["object_attributes"]["updated_at"]
        activity_title = object_type + ": " + state
        body = { "@type": "MessageCard", "@context": "http://schema.org/extensions", "themeColor": "0076D7", "summary": activity_title, "sections": [{ "activityTitle": activity_title, "activitySubtitle": activity_subtitle, "facts": [{ "name": "Description", "value": description }, { "name": "Created at", "value": created_at }, { "name": "Updated at", "value": updated_at }, { "name": "Status", "value": state }], "markdown": "true" }] }
        msteams(web_url, body)
    else: # The code assumes that if it is not a Merge/Issue, that the body is a Push event.
        repo_name = data["repository"]["name"]
        project_url = data["repository"]["homepage"]
        after = data["after"]
        purl = None
        message = None
        timestamp = None
        author = None
        for x in data["commits"]:
            if after == x["id"]:
                purl = x["url"]
                message = x["message"]
                timestamp = x["timestamp"]
                author = x["author"]["name"]
        
        body = { "@context": "https://schema.org/extensions", "@type": "MessageCard", "potentialAction": [ { "@type": "OpenUri", "name": "View Most recent Commit", "targets": [ { "os": "default", "uri": purl } ] },{ "@type": "OpenUri", "name": "Go to Project", "targets": [ { "os": "default", "uri": project_url } ] } ], "sections": [ { "activityTitle": "New Push Event on " + repo_name, "activitySubtitle": "Last commit details", "facts": [ { "name": "Commit Timestamp:", "value": timestamp }, { "name": "Commit Author", "value": author }, { "name": "Commit Message", "value": message } ], "markdown": "true" } ], "summary": "New Post event", "themeColor": "0072C6", }
        msteams(web_url, body)
    return "OK"

# Health Check for ELB if needed
@app.route('/health',methods=['GET'])
def healthcheck():
    return "UP"

if __name__ == '__main__':
   app.run(host='0.0.0.0')