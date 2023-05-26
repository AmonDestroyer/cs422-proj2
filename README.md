# cs422-proj2
This project is for the University of Oregon's CS 422 class. 

Below are the current deployments. The developement (dev) deployment is the initial deployment manually triggered to deploy by the developer. Upon successful deployment and validation the developer is able to promote said deployment to production (prod).

| Deployment | Description |
| :----------: | :----------: |
| (Dev)[https://deploy-cdp-dev-mlyt65mfba-uc.a.run.app] | Initial deployment in pipeline. |
| (Prod)[https://deploy-cdp-prod-mlyt65mfba-uc.a.run.app] | Promoted deployment from Dev. |

# Developer Notes

## Docker Container Deployment
This project can be build and deployed locally if one does not desire to build it in the cloud.
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
NOTE: This will remove all stopped containers including the ones not part of `<tag-name>`, reference the (docker cli)[https://docs.docker.com/engine/reference/commandline/cli/] for more information.

## Cloud Deployment
This project was built and deployed using Google Cloud.
The steps to replicate deployment and implement continuous integration are listed here.
Continuous deployment is a goal of this projectso both Continuous Integration and Continuous Deployment (CI/CD) is implemented, but at this time only Continuous Integration is discussed and has been implemented.

Requirements:
- (Google Cloud CLI)[https://cloud.google.com/sdk/docs/install-sdk]
- Google cloud account

After downloading this repo follow the below steps to deploy the project to google cloud.
1. Create a project in google cloud, (ref)[https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project].
2. Create an artifact registry, (ref)[https://cloud.google.com/build/docs/build-push-docker-image#create_a_docker_repository_in].
3. Configure Google Cloud Build to trigger from git commits, (ref)[https://cloud.google.com/build/docs/automating-builds/create-manage-triggers].
4. Setup and deploy to pipeline using (Google Cloud Deploy)[https://cloud.google.com/deploy/docs/deploy-app-run].

Deployments can then be updated through new released after the automated builds complete.
References (Create a release)[https://cloud.google.com/deploy/docs/deploy-app-run#create_a_release] for how to make the new released.
