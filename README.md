# Gitlab 2 Teams

## Introduction

The current gitlab we are running for IT is version 7.0. MS Teams is not supported until version 11. I have since created a webhook interpreter to parse the data coming from our gitlab instance to send to teams.

## Requirements

This application was developed using python 3.6 and using the following pips:

- flask
- json
- requests

Port 5000 also needs to be available and open to be successful.

## Building/Running the docker file

```bash
docker build -f Dockerfile -t git2teams:v1 .
docker run -d --name git2teams -p 5000:5000 git2teams:v1
```

## Accepted HTTP requests

### /hook

In order to actually translate the git data to teams, you need to point the web hook at hostname:5000/hook and provide a uri parameter of url. See below for example.

```bash
some-host.com:5000/hook?url=http://outlook.office.com/webhook/pathtowebhookdetails
```

The /hook only accepts POST methods and expects the url parameter to be parsed.
