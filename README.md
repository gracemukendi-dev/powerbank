# NOTE: This repo doesn't have any releases just yet. Still under development. 

# PowerBank

PowerBank is simply a 'box' (A Vagrant Box to be exact) assembled to help fellow engineers with spinning up resources locally for development needs and eventually remotely. 

The idea is really to allow an engineer to focus on the project at hand while leaving it to the box to put together all needed resources.

## Hashiqube

The majority of PowerBank has been forked from the [Hashiqube repository](https://github.com/servian/hashiqube) and will tromendously aid in getting us there faster than it would have been without.

# Prerequisites

The following have to be installed on your machine:
### A Hypervisor eg: VirtualBox
### [Vagrant](https://www.vagrantup.com/downloads.html)
### Git

You will also need access to an [AWS Account](https://aws.amazon.com/console/). It is important for you to create a user with cli access to your account and rights to spin up the resources you forsee you might make use of. Please see [this tutorial](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users_create.html) for a walkthrough on how to create users with cli access.

PowerBank requires the following ENVS to be configured:
```
PB_CONFIG_FILE_LOCATION #will contain the location of your configit@github.com:gracemukendi-dev/powerbank.gitg file, which contains the list of resources needed for your project. This is a json file.
AWS_PROFILE #for remote deployment of resources

```

# Usage

The config file mentioned above should have the following format. 

```json
{
  "remote_repo_url" : {
    "git:github.com:piccachiou/mynewapp.git"
  },
  "local_repo_path" : {
    "/Users/piccachiou/dev/repos/mynewapp"
  },
  "resources" : {
    "s3", "mongo","redis"
  },
  "service_type" : {
    "lambda", "docker" 
  }
}
```

## Local Run
```bash
git clone git@github.com:gracemukendi-dev/powerbank.git & cd $_ #clone this repo and cd into it
vagrant up --provision-with powerlocal #startup your box
```
This will start up a Vagrant box which will share a directory with the host. The shared directory will be that of your project.

## Remote Run
```bash
vagrant up --provision-with powerremote #deploy your resources
```
This will synchronise with your remote git repo and create github actions to deploy to your aws account. 



