# cs422-proj2
This project is for the University of Oregon's CS 422 class. 

Below are the current deployments. Both devvelopement (dev) and production (prod) deployment are automatically triggered upon each git push to this repo.

| Deployment | Description |
| :----------: | :----------: |
| [Dev](https://deploy-cdp-dev-mlyt65mfba-uc.a.run.app) | Initial deployment in pipeline. |
| [Prod](https://deploy-cdp-prod-mlyt65mfba-uc.a.run.app) | Promoted deployment from Dev. |

# Developer Notes

## Local Deployment
This project can be deployed locally in two ways, one being using python to directly launch the Django framework and alternatively using Docker.
It is recommended that all local builds be performed using Docker since it is OS independent.

### Python Deployment
This project can be built and deployed using the Django framework.
The steps listed in this section are steps perform on the Windows OS, the commands may differ slightly for other OSs.

Requirements:
- [Python3](https://www.python.org/downloads/) installed
- [Pip](https://pip.pypa.io/en/stable/installation/) installed

Steps:
1. In the root of the repo install the necessary packages, `pip3 install -r requirements.txt`
2. Enter the "cs_degree_planner" directory, `cd cs_degree_planner`.
3. Migrate the databases, `python manage.py migrate`.
4. Import all courses, `python manage.py import_courses forecast/recommendedcourses.xlsx`.
5. Run the server, `python manage.py runserver`.
By default the server runs at "localhost:8000".

### Docker Container
This project can be built and deployed locally if one does not desire to build it in the cloud.
Below are the steps to perform this build from the root directory of the cloned repository.

Requirements:
- Docker is installed

Steps:
1. Verify Docker is running by typing `docker info` in the terminal.
If docker returns an error then docker needs to be started.
2. In the root of the cloned repo, build an image of the application `docker build -t <tag-name> .`.
3. Run the image using `docker run -d -p <port>:8080 <tag-name>`.

Now your build will be accessible at `localhost:<port>`.

If you wish to stop the instance it can be stopped using `docker stop $(docker ps -q)`.
This over time will lead to a build-up of docker containers that can be cleaned up using `docker rm $(docker ps -qa)`.
NOTE: This will remove all stopped containers including the ones not part of `<tag-name>`, reference the [docker cli](https://docs.docker.com/engine/reference/commandline/cli/) for more information.

## Cloud Deployment
This project was built and deployed using Google Cloud.
Below are the steps to replicate Continuous Integration and Continuous Deployment (CI/CD) utilized in this project.

Requirements:
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
- Google cloud account

Steps:
1. Create a project in google cloud, [ref](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).
2. Create an artifact registry, [ref](https://cloud.google.com/build/docs/build-push-docker-image#create_a_docker_repository_in).
3. Configure Google Cloud Build to trigger from git commits, [ref](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers).
This can be linked to either this repo or this repo can be forked and it can be linked to that one.

Builds and deployents are then automatically performed after each git push to the repo.