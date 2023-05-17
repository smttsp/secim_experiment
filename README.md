# Automated Training Pipeline 

This repository provides an automated training pipeline that simplifies the process of training and updating deep learning models with new data.

The pipeline takes a common dataset from `torchvision.Dataset` (such as MNIST or FashionMNIST) and a configuration file in YAML format. 
It then automatically trains a simple CNN model on the specified data, compares its performance to the previous best model,
and saves the new model if it performs better.


## Motivation

One of the major things in AI/DL is the data. Often, we have a model and once we have "better" data, we retrain our 
models with the new data. However, this process may be cumbersome as 

- Have a VM instance (or local machine) and set up the environment (I admit, I do this manually too!) 
- We need to download the new data
- Train the model with the "better" data
- Get metrics, visualizations etc
- Save/Load/Verify if the model is functional/working fine
- Dockerize
- Deploy on cloud or where ever we want (I won't do this step)

So this repo will do the whole thing automatically. 


## Spoiler

Since I am not gonna collect more data, I will first get part of the data (say 50%) and do the training, save, dockerize etc. 
Then, I will gradually increase the amount of the data. Once certain conditions are met (e.g., the data size increase by x% 
or something like that), the code will do retraining. 

Users can change these conditions, for example, get the hash of the previous data. If the hash has changed, then retrain. 
One of the use case might be that the number of images may not change but the quality of it may change. So, user might wanna
run every midnight or once a week etc. This step is really not the most crucial aspect of the project


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
(I couldn't figure out how to install `wandb` with poetry, it just breaks the poetry when installed that way :see_no_evil:)

After installation, you need to do the following step:

```bash
wandb login
```
and enter API key obtained from `https://wandb.ai/quickstart` after logging in/signing up in the Weights & Biases webpage

## Poor man's Jira

1. :heavy_check_mark: Setting up the repo
2. :heavy_check_mark: Data downloader for a bunch of classification tasks
3. :heavy_check_mark: Simple CNN Model for classification
4. :heavy_check_mark: Dataloaders (train, val, test)
5. :heavy_check_mark: Full Training Pipeline (for a specific task)
6. :heavy_check_mark: Metric
7. :heavy_check_mark: Visualizations 
8. :heavy_check_mark: Save/load model
9. :heavy_check_mark: Integrating YAML 
10. Automated training (From 50% of the data to 100% of the data)
11. Visualization export using plotly (Accuracy, Confusion metrics etc)
12. :heavy_check_mark: Making the training fully functional by only selecting project (MNIST/FashionMNIST etc)
13. Ray[Tune] integration 
14. :heavy_check_mark: Device-agnostic code (not tested for now as I have only cpu)
15. Adding more visualization functions:
    - :heavy_check_mark: input visualization
    - :heavy_check_mark: data distribution in each of train, val, test
    - :heavy_check_mark: output visualization (errors, true predictions etc)
    - confusion matrix, accuracy etc
    - activation visualization?
16. Automate other parameters from yaml file (this will allow us for using raytune)
    - model details (we should be able to update model details from the config)
    - model name (be able to use some common models, resnet18, 50, vgg16 etc)
17. :heavy_check_mark: integrate `weights and biases` and `neptune`. Automatically track experiments
18. integrate `timm` library for model architectures
19. 