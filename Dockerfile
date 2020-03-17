FROM python:alpine3.7
LABEL version="1.0" maintainer="TOC A/D toc-automationanddevelopment@digitalriver.com"

#Copy Working python script into container
COPY . /app
WORKDIR /app
#Install modules
RUN pip install -r requirements.txt 

# Expose and start script
EXPOSE 5000
ENTRYPOINT [ "python" ] 
CMD [ "git2teams.py" ] 
