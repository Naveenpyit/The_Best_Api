from .models import Master_Table_List
from datetime import date
from rest_framework.serializers import ModelSerializer # type: ignore

class serializer:
    @staticmethod
    def serial(data):
        if isinstance(data,list):
            return [serializer.serial(item)for item in data]
        elif isinstance(data,dict):
            return {key:serializer.serial(value)for key,value in data.items()}
        elif isinstance(data,date):
            return data.isoformat()
        return data
    

class master_serial(ModelSerializer):
    class Meta:
        model=Master_Table_List
        fields='__all__'    