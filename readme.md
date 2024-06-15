Building of the Docker Container.

The process typically starts with the creation of a dockerfile, which serves as a set of instructions for building the container image. The dockerfile includes commands for updating packages, copying content to the container, creating a working directory, setting up a virtual environment for Python 3, installing the required libraries specified in the requirements file, and defining the entry point for the application.

Therefore, dockerfile is set to contain the following commands:
FROM python:3.10-slim

COPY . /root

WORKDIR /root

RUN pip install flask gunicorn pandas pathlib joblib catboost pyarrow flask_wtf

The Docker container is to be based on the ubuntu image. What the code does, firstly, is to update all the packages to the latest versions. Then, it copies all the content to the container (excluding the files specified in the dockerignore file). Inside another directory, it sets up a virtual environment for python3 and installs all the required libraries specified in the requirements.txt file. Finally, it starts an application called run.py.

The client should use Postman to create an HTTP request. It is crucial to ensure that the parameters in the request match the application’s requirements to avoid errors. This approach ensures that the model is used in a business context. The stakeholders do not need to run Python scripts or have special technical knowledge to use Jupyter notebooks or process data. They are only responsible for collecting data in a proper format that can be easily understood by the business (because data is obtained from Amplitude, which business unit is acquainted with). As a result, the business unit can immediately receive predictions that will positively impact the decision-making process and speed up operations.
