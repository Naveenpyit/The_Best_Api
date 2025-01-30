from .dbconnect import Api_db
from .models import Master_Table_List
from .serilaizer import serializer
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
import os,json

class Api_calls:
    @staticmethod
    def get_api(query,table_name,is_post_request=False):
        try:
            master_obj,created=Master_Table_List.objects.get_or_create(Table_name=table_name)

            current_time=timezone.now()
            local_time=timezone.localtime(current_time)

            duration=int(master_obj.Duration)
            if not duration:
                duration=2
            
            file_path=os.path.join(settings.BASE_DIR,'Datas_file',f'{table_name}.txt')

            if created or (local_time - master_obj.Last_update > timedelta(hours=duration)) or is_post_request:
                print("Inga iruken")
                data=Api_db.get_connect(query)

                if data:
                    serial_data=serializer.serial(data)

                    master_obj.Last_update=local_time
                    master_obj.New_update='Yes'
                    master_obj.save()

                    if not os.path.exists(os.path.dirname(file_path)):
                        os.makedirs(os.path.dirname(file_path))

                    with open(file_path,'w')as file:
                        json.dump(serial_data,file,indent=3)
                    
                    success_data={
                        "Result":1,
                        "Message":"Success",
                        "Api-result":serial_data
                    }
                    return success_data
            elif os.path.exists(file_path) and os.path.getsize(file_path)>0:
                print("Illa inga iruken")
                master_obj.New_update='No'
                master_obj.save()

                with open(file_path,'r')as file:
                    data=json.load(file)
                
                success_data={
                    "Result":1,
                    "Message":"Success",
                    "Api-result":data
                }
                return success_data
            else:
                return{"Result":0,"Message":"Fails","Api-result":""}
        except Exception as err:
            return {
                "Result":0,
                "Message":str(err),
                "Api-result":""
            }