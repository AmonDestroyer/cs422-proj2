FROM python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8080
MAINTAINER Adam Case "adamrichcase@gmail.com"
RUN apt-get update -y
RUN apt-get install -y python3-pip python-dev build-essential python3-nose
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
WORKDIR /app/cs_degree_planner
ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8080"]
