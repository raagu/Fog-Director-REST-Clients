"""
Copyright 2016 Ashok Kanagarsu

These are sample functions for the Cisco Fog Director REST API.
get all the log files of the app from device details page and download them



See: 

http://www.cisco.com/c/en/us/td/docs/routers/access/800/software/guides/iox/fog-director/reference-guide/1-0/fog_director_ref_guide.html

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""
#from functions import *
import requests
import json
import base64
def get_token(ip,username,password):
    #print(ip)
    url = "https://%s/api/v1/appmgr/tokenservice" % ip
    print(url)

    r = requests.post(url,auth=(username,password),verify=False)
    token=''
    if  r.status_code == 202:
        print(r.json())
        token = r.json()['token']
        #print(token)
    else:
        print("ERROR")
        print "Status code is "+str(r.status_code)
        print r.text
    return(token)


def view_all_app_logs_from_device_details_page(ip,token):
  device_ip=raw_input("enter the ip address of the device:")
  deployed_app=raw_input("enter the name of the app installed on that device:")
  
  #get device id using the device ip address . search by device ip and get the device id of it 
  url = "https://%s/api/v1/appmgr/devices?limit=10000&offset=0&searchByIp=%s" % (ip,device_ip)
  headers = {'x-token-id':token,'content-type': 'application/json'}
  r=requests.get(url,headers=headers,verify=False)
  print(r.status_code)
  print("devices which are matching the ip address on your  FD")
  devices=json.loads((json.dumps(r.json())))
  for index in range(len(devices['data'])):
      device_id=devices['data'][index]['deviceId']
      ip_addr=devices['data'][index]['ipAddress']
      if ip_addr==device_ip:
        device_id_confirmed=str(device_id)
        

  #get the my app id of the deployed app . 
  url = "https://%s/api/v1/appmgr/myapps?searchByName=%s" % (ip,deployed_app)
  headers = {'x-token-id':token,'content-type': 'application/json'}
  r=requests.get(url,headers=headers,verify=False)
  print("Status code of fethcing MYAPPID REST request %d") % r.status_code
  myappinfo=json.loads((json.dumps(r.json())))
  myappid=myappinfo['myappId']


   
  #view all logs for the app on this device 
  print("view all logs for the app %s on device %s") % (deployed_app,str(ip_addr))
  url3="https://%s/api/v1/appmgr/devices/%s/apps/%s/logs" % (ip,device_id_confirmed,myappid)
  
  r = requests.get(url3,headers=headers,verify=False)
  print("Status code on getting the log files of app on device %s where this app is deployed: %d") % (str(ip_addr),r.status_code)
  logfiles=json.loads((json.dumps(r.json())))
  for index in range(len(logfiles)):
    print("logfile name:%s  logfile size:%s logfile URL:%s") % (logfiles[index]['filename'],logfiles[index]['size_bytes'],logfiles[index]['_link']['href'])
    url4="https://%s%s" % (ip,str(logfiles[index]['_link']['href']))
    r = requests.get(url4,headers=headers,verify=False)
    logcontent=json.loads((json.dumps(r.json())))
    print(logcontent)
    print("log_content_download_status:%s") % logcontent['message']
    print("log_content_size:%s") % logcontent['size']
    print("content of the log file:%s") % logcontent['content']
  
def delete_token(ip, token):
    url = "https://%s/api/v1/appmgr/tokenservice/%s" % (ip, token)
  
    headers = {'x-token-id':token,'content-type': 'application/json'}
    
    r = requests.delete(url,headers=headers,verify=False)

    if  r.status_code == 200:
        print(r.json())
    else:
        print("ERROR")
        print "Status code is "+str(r.status_code)
        print r.text 
app_mgr_ip=raw_input("Enter app manager ip address")
username=raw_input("enter the username of your FD:")
password=raw_input("enter the password of your FD:")
print "loging to FD and fetch an TOKEN"
token_id=get_token(app_mgr_ip,username,password)
print "editing resources for an app installed on a particular device "
view_all_app_logs_from_device_details_page(app_mgr_ip,token_id)
print "Logging out of Fog Director"
delete_token(app_mgr_ip, token_id)

