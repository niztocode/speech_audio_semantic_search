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
The schema of our vector database is located in the python module `sass.db.schema`. To create the schema in the database run: `python -m sass.db.schema`. There is also the option of deleting the schema of the database by providing the previous command with the argument `-d/--delete`. Run `python -m sass.db.schema -d` to delete the current database schema. _Warning_! This will also delete all class object stored in the database!


#### Updating Library
Run `python -m sass.update_library` to process all the audio files in `LIBRARY_PATH` and store to db.

#### Note: Faster-Whisper CTranslate2 bug
Packages `torch`, `funtorch` & `faster-whisper` all use a different copy of the executable `libiomp5.dylib` to run C executables in python. However, during execution multiple instances of this library are initialized and linked to the program.

```
OMP: Error #15: Initializing libiomp5.dylib, but found libiomp5.dylib already initialized.

OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.
```

To avoid the above error and run Faster-Whisper successfully, do the following:
```
find  ~/.local/share/virtualenvs/<virtual_environment_name>/ -name "libiomp5.dylib"

Output:
~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/torch/lib/libiomp5.dylib
~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/ctranslate2/.dylibs/libiomp5.dylib
~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/functorch/.dylibs/libiomp5.dylib
```
```
rm ~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/torch/lib/libiomp5.dylib
rm ~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/functorch/.dylibs/libiomp5.dylib
```
```
ln ~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/ctranslate2/.dylibs/libiomp5.dylib ~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/torch/lib/libiomp5.dylib

ln ~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/ctranslate2/.dylibs/libiomp5.dylib ~/.local/share/virtualenvs/<virtual_environment_name>/lib/python3.10/site-packages/functorch/.dylibs/libiomp5.dylib
```

#### Search
After you have updated your library with your speach audio clips, run `python -m sass.search`. Make text queries to the prompt and retrieve semantically similar context from your audio files' library.