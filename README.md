# Election security

This repo aims to create a converter from image to text for signed ballot records (islak imzali secim tutanaklari), and it will read an image and return how many votes each candidate got. 

It is not complete, but early result are here: https://github.com/smttsp/secim_experiment/blob/main/tutanak_input-output.zip. I connected to Google Vision API but I didn't like the initial results of how Vision API reads the images. I realized a better tool would be Google Document API.

If I see a little light that opposition is not as useless as they seem, I will work on integrating this tool into other open tools written by bright people for securing the elections.

## Installation

### Prerequisite: `pyenv`

https://github.com/pyenv/pyenv-installer

On macOS you can use [brew](https://brew.sh), but you may need to grab the `--HEAD` version for the latest:

```bash
brew install pyenv --HEAD
```

or

```bash
curl https://pyenv.run | bash
```

And then you should check the local `.python-version` file or `.envrc` and install the correct version which will be the basis for the local virtual environment. If the `.python-version` exists you can run:

```bash
pyenv install
```

This will show a message like this if you already have the right version, and you can just respond with `N` (No) to cancel the re-install:

```bash
pyenv: ~/.pyenv/versions/3.8.6 already exists
continue with installation? (y/N) N
```

### Prerequisite: `direnv`

https://direnv.net/docs/installation.html

```bash
curl -sfL https://direnv.net/install.sh | bash
```

### Developer Setup

If you are a new developer to this package and need to develop, test, or build -- please run the following to create a developer-ready local Virtual Environment:

```bash
direnv allow
python --version
pip install --upgrade pip
pip install poetry
poetry install
```
