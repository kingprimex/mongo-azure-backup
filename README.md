# mongodb-backup
A solution to automate MongoDB Backup
* https://hub.docker.com/u/kingprimex

# How it works 
* There is a python script ```mongo-bkp.py``` which connects to mongo db and takes mongo dump.
* After the execution of the mongo dump , it zip's the folder by appending current datetime and uploads to azure blob storage.
    * It is saved in azure blob as ```containername/date/backup_date.zip```
* It accepts following environment variables
    * ```MONGO_HOST```: Mongo host url.
    * ```MONGO_USER```: Mongo user is required if mongo is secured with user credentials
    * ```MONGO_PASS```: Mongo user's password
    * ```BACKUP_FOLDER```: Name of the root folder to be uploaded in blob storage
    * ```FILENAME```: zip folder name appended with date and uploaded under backup_folder in blob storage
    * ```CONTAINER_NAME```: Azure container name
    * ```ACCOUNT_NAME```: Azure storage account name
    * ```ACCOUNT_KEY```: Azure storage account key

# How to execute
* ```docker pull kingprimex/mongo-azure-backup:4.0 ```
*  ```docker run --net=host --rm -e MONGO_HOST="localhost" -e BACKUP_FOLDER="mongo" -e FILENAME="backup" -e CONTAINER_NAME="mongo" -e ACCOUNT_NAME="storageblobaccount" -e ACCOUNT_KEY="blobkey" -it kingprimex/mongo-azure-backup:4.0```
    * When the container runs , it connects to mongo , takes a gzipped and archived dump and uploads to blob storage.

# Restoring
* ```mongorestore --gzip --archive=/tmp/test.archive_22-10-21_11%3a31%3a04  --host=127.0.0.1 -u=root -p=example```
    * The restore has to be done manually by using the mongorestore command.

## Note : Preffered method of using this docker image effectively is by running it through a schedular or cron jobs
