# Speech Audio Semantic Text Search

A library system to search through the context of audio clips in text terms.

## Table of Contents

- [Speech Audio Semantic Text Search](#project-name)
  - [About](#about)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [Acknowledgments](#acknowledgments)

## About

Provide a brief introduction and overview of your project. Explain its purpose and what problem it aims to solve.

## Getting Started

Get the project up and running.

### Prerequisites

* python 3.10
* pipenv
* docker
* VSCode ( preferred editor )

### Installation

#### Application Virtual Environment
To install the necessary packages and dependencies of the python virtual envrionment run `pipenv install`. Run `pipenv install --dev` to include, also, development packages for developments purposes. Run `pipenv shell` to activate the environment.

#### Weaviate Database Containers
Our Weaviate DBMS runs in a docker containerized enviroment. Run `docker compose up -d` to start the database services:
* Weaviate db @ http://localhost:8080
* text2vector-transformer @ http://localhost:8082
* reranker-transformer @ http://localhost:8081

## Usage

#### Environment Variables
* `WEAVIATE_DB_URL`: url of Weaviate DB accessible url ( e.g. http://localhost:8080 )
* `WHISPER_PATH`: path a Whisper model for speech-to-text transorfmation ( e.g. models/whisper-small ) 
* `LIBRARY_PATH`: path to folder that contains audio files ( e.g. audio_clips/)

#### DB Schema
The schema of our vector database is located in the python module `sass.schema`. To create the schema in the database run: `python -m sass.schema`. There is also the option of deleting the schema of the database by providing the previous command with the argument `-d/--delete`. Run `python -m sass.schema -d` to delete the current database schema. _Warning_! This will also delete all class object stored in the database!

#### Updating Library
Run `python -m sass.update_library` to process all the audio files in `LIBRARY_PATH` and store to db.

#### Search
After you have updated your library with your speach audio clips, run `python -m sass.search`. Make text queries to the prompt and retrieve semantically similar context from your audio files' library.