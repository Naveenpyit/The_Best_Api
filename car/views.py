from django.shortcuts import render
from django.http.response import JsonResponse
from .apicalls import Api_calls
from rest_framework import status # type: ignore
from rest_framework.decorators import api_view,authentication_classes # type: ignore
from .authentication import apikeycheck
from .dbconnect import Api_db

@api_view(['GET'])
@authentication_classes([apikeycheck])
def get_ph_business(request,table_name):
    try:
        query=f'Select * from {table_name}'
        data=Api_calls.get_api(query,table_name)

        if isinstance (data,dict) and data.get('Result')==0:
            return JsonResponse(data,safe=False,status=204)
        return JsonResponse(data,safe=False,status=200)
    except Exception as err:
        return JsonResponse({
            "Result":0,
            "Message":str(err),
            "Api-result":""
        },safe=False,status=500)


@api_view(['POST'])
@authentication_classes([apikeycheck])
def post_ph_business(request):
    try:
        code=request.data.get('code')
        name=request.data.get('name')
        user=request.data.get('user')
        date=request.data.get('date')

        if not code or not name or not user or not date:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to submit",
                "Api-result":"Missing Fileds!"
            },safe=False,status=400)

        query=f"Insert into ph_business(buscode,busname,adduser,adddate,deleted) values({code},'{name}',{user},'{date}','N');"
        data=Api_db.post_common(query)

        if "Error" in data:
            return JsonResponse({
                "Result":0,
                "Message":"Fail to post",
                "Api-result":data["Error"]
            },safe=False,status=204)
        query_select = f"SELECT * FROM ph_business " 
        result = Api_calls.get_api(query_select, 'ph_business', is_post_request=True)
        
        return JsonResponse({
            "Result":1,
            "Message":"Success",
            "Api-result":"Data Submitted Successfully"
        },safe=False,status=201)
    except Exception as err:
        return JsonResponse({
            "Result":0,
            "Message":str(err),
            "Api-result":""
        })
    

        



