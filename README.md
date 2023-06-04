# cs422-proj2
This project is for the University of Oregon's CS 422 class. 

Below are the current deployments. Initially the deployment was done in continers, devvelopement (dev) and production (prod), as this was easy to implement. It was later found out that since containers were being spun up and down and the database was part of the web applciation then users and their courses were nto being saved. So a third instance on a VM was created that would maintain the database until a new push was made to the database.

| Deployment | Description |
| :----------: | :----------: |
| [VM](http://34.36.192.16) | Web applicaiton deployment on virtual machine. |
| [Dev](https://deploy-cdp-dev-mlyt65mfba-uc.a.run.app) | Initial deployment in pipeline. |
| [Prod](https://deploy-cdp-prod-mlyt65mfba-uc.a.run.app) | Promoted deployment from Dev. |

# Future Improvements
In the future the below improvements should be made to the project.
- Separate the DB from the web app so new version pushes of the app don't result in the database being reset.
- Full containerization of the web application so a VM isn't required.
- Addition of UO majors.
- Addition of UO minors.
- Addition of all UO courses.
- Dynamic pull of UO courses through the [UO API Developer Portal](https://developer.uoregon.edu/).

# Developer Notes
This applicaiton has a default admin login with the below credentials. This is mainly for testing purposes and not intended for all users to use.
This can also be changed after initial deployment, but each reset will contain these crednetials unless removed from the `import_courses.py` file where the user is initially loaded in.

Username: admin

Password: admin

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
3. Run the image using `docker run -d -p <port>:80 <tag-name>`.

Now your build will be accessible at `localhost:<port>`.

If you wish to stop the instance it can be stopped using `docker stop $(docker ps -q)`.
This over time will lead to a build-up of docker containers that can be cleaned up using `docker rm $(docker ps -qa)`.
NOTE: This will remove all stopped containers including the ones not part of `<tag-name>`, reference the [docker cli](https://docs.docker.com/engine/reference/commandline/cli/) for more information.

## Cloud Deployment
This project was built and deployed using Google Cloud.
Below are the steps to replicate Continuous Integration and Continuous Deployment (CI/CD) utilized in this project.
Both methods for cloud run deployment and VM deployment are explained.

NOTE: For proper deployment explained in both instances some diviation from provided resources/tutorials will need to be performed.
These diviations are not explained in the steps and it is highly encouraged that the command inputs mean.

### General Setup
Requirements:
- [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
- Google cloud account

Steps:
1. Create a project in google cloud, [ref](https://cloud.google.com/resource-manager/docs/creating-managing-projects#creating_a_project).
2. Create an artifact registry, [ref](https://cloud.google.com/build/docs/build-push-docker-image#create_a_docker_repository_in).

### Cloud Run Deployament
Steps:
1. Modify `cloudbuild.yaml`.
    1. Remove or comment out the [VM] sections.
    2. Update the image to reference the appropriate region, repo, and image from the created artifact registry.
    3. If needed, update the region.
2. Configure Google Cloud Build to trigger from git commits, [ref](https://cloud.google.com/build/docs/automating-builds/create-manage-triggers).
This can be linked to either this repo or this repo can be forked and it can be linked to the clone repository.
NOTE: Ensure the `cloudbuild.yaml` file is used with the file location at `/cloud/cloudbuild.yaml`.

Builds and deployents are then automatically performed after each git push to the repo.

### VM Deployment
Steps:
1. Create a VM instance connected to a load balancer, [ref](https://cloud.google.com/load-balancing/docs/health-checks).
2. Modify the `cloudbuild.yaml`.
    1. Remove or commend out all [Cloud Run] sections.
    2. Update the image to reference the appropriate container image.
    3. Update the app to reference the appropriate VM.
    4. Update the zone to reference the approrpiate zone.

It is recommended that a service account is created to manage auto deployment, [ref](https://cloud.google.com/iam/docs/service-accounts-create).
If this is done the build trigger will need to be updated with the created account.
Reperform the build and if permissions are required update the service account with the appropriate permissions.