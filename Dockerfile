FROM python:alpine3.8
LABEL version="1.1"

#Copy Working python script into container
COPY . /app
WORKDIR /app
#Install modules
RUN pip install -r requirements.txt 

# Expose and start script
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "git2teams.py" ] 
