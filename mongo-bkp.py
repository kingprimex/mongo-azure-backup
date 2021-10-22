import os,subprocess,datetime,json,requests

def create_bkp():
    try:
        if os.environ.get('MONGO_REPLICASET',None):
            if os.environ.get('MONGO_URI',None):
                if os.environ.get('MONGO_USER',None) and os.environ.get('MONGO_PASS',None):
                    query = "mongodump --uri="+os.environ['MONGO_URI'] +" -u "+os.environ['MONGO_USER']+" -p " +os.environ['MONGO_PASS']+" --gzip --archive=dump.archive"
                else:
                    query = "mongodump --uri="+os.environ['MONGO_URI']+" --gzip --archive=dump.archive"
                cur_date = datetime.datetime.now().strftime("%d-%m-%y")
                cur_time = datetime.datetime.now().strftime("%H:%M:%S")
 #               file_name = os.environ['FILENAME']+"_"+cur_date+"_"+cur_time+".zip"
                file_name_init = "dump.archive"
                file_name = file_name_init+"_"+cur_date+"_"+cur_time
                res = os.system(query)
                if res == 0:
                    os.system("mv "+file_name_init+" "+file_name)
                    upload_bkp(file_name,cur_date)
                else:
                    print("Error while creating mongo backup")
            else:
                print("MONGO_URI not defined: Ex. MONGO_URI=mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myReplicaSetName")
#mongodump --uri="mongodb://mongodb0.example.com:27017,mongodb1.example.com:27017,mongodb2.example.com:27017/?replicaSet=myReplicaSetName"
        if os.environ.get('MONGO_HOST',None) and not os.environ.get('MONGO_REPLICASET',None):
            if os.environ.get('MONGO_USER',None) and os.environ.get('MONGO_PASS',None):
                query = "mongodump -h"+os.environ['MONGO_HOST'] +" -u "+os.environ['MONGO_USER']+" -p " +os.environ['MONGO_PASS']+" --gzip --archive=dump.archive"
            else:
                query = "mongodump -h"+os.environ['MONGO_HOST']+" --gzip --archive=dump.archive"
            cur_date = datetime.datetime.now().strftime("%d-%m-%y")
            cur_time = datetime.datetime.now().strftime("%H:%M:%S")
            file_name_init = "dump.archive"
            file_name = file_name_init+"_"+cur_date+"_"+cur_time
            res = os.system(query)
            if res == 0:
               # os.system("zip -r "+file_name+" dump")
                os.system("mv "+file_name_init+" "+file_name)
                upload_bkp(file_name,cur_date)
            else:
                print("Error while creating mongo backup")
        else:
            print("No host")
    except Exception as e:
        print(e)

def upload_bkp(file_name,cur_date):
    try:
        query = "az storage blob upload --container-name "+os.environ['CONTAINER_NAME']+" -f "+file_name+" --name "+os.environ['BACKUP_FOLDER']+"/"+cur_date+"/"+file_name+" --account-name "+os.environ['ACCOUNT_NAME']+" --account-key "+os.environ['ACCOUNT_KEY']
        upstatus = os.system(query)
        if upstatus == 0:
            os.system("rm "+file_name)
            print("Upload finished sucessfully")
        else:
            print("Upload failed and status = "+upstatus)
    except Exception as e:
        print("Error: "+str(e))

create_bkp()      
