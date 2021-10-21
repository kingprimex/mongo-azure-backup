FROM python:3.9-slim
RUN apt-get update --fix-missing && pip install requests
RUN apt-get -y install curl zip && curl -O https://fastdl.mongodb.org/tools/db/mongodb-database-tools-debian10-x86_64-100.5.1.deb && dpkg -i mongodb-database-tools-debian10-x86_64-100.5.1.deb && rm -f mongodb-database-tools-debian10-x86_64-100.5.1.deb && curl -sL https://aka.ms/InstallAzureCLIDeb | bash
ADD mongo-bkp.py /
CMD python mongo-bkp.py
