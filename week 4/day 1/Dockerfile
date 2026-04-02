# get python
# copy the code

# install python dependencies

# open the port 8000 on the container, because the app.py is configiured to run on port 8000

# run the code

FROM python:3.10-slim

# in the container - which path to store the source code on
WORKDIR /app

# copy the contents from the current directory into the app folder
COPY . /app

# install dependencies
RUN pip install -r requirements.txt

# open port 8000
EXPOSE 8000

# run the code
CMD [ "python", "app.py" ]
