# Flask ChatGPT

A customizable web interface for the OpenAI ChatGPT API.  Users and Conversations are stored in a postgresql database and not stored by a third party.  (OpenAi does store API requests for 30 days.  Azure OpenAI does not store request history).

## Prerequisites.

You will need Docker Desktop to run locally.

An API KEY for OpenAI API or Azure OpenAI service API

## Getting Started

To deploy locally on docker rename the dot-env.txt file to .env and add your OpenAI API Key to the file.

If using Azure OpenAI, set the additional environment variables specified.

To build and deploy the docker containers run the following command within the project folder
```
    docker compose up --build
```

To use Microsoft OpenAI service additional parameters will neet to be set in app/routes.py.
Types of Contributions

## Contribution 

Flask-ChatGPT is an open source project and is open to any contributions that can inprove it. Whether you're experienced with coding, UX design, or simply want to suggest a bug fix or a new feature, I'm open to your ideas.  Please feel free to reach out via [Discord](https://discord.gg/KASqpEWmDb) if you have contributions you want to discuss.

For specific areas of contribution see the Issues Tracker.