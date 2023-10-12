import subprocess as sp
import re
import time
import pandas as pd

lista_lon = []
lista_lat = []
df_track = pd.DataFrame()

accuracy = 3
i=0

while True and i<10:    
    time.sleep(5)
    pshellcomm = ['powershell']
    pshellcomm.append(
        'add-type -assemblyname system.device; '\
        '$loc = new-object system.device.location.geocoordinatewatcher;'\
        '$loc.start(); '\
        'while(($loc.status -ne "Ready") -and ($loc.permission -ne "Denied")) '\
        '{start-sleep -milliseconds 100}; '\
        '$acc = %d; '\
        'while($loc.position.location.horizontalaccuracy -gt $acc) '\
        '{start-sleep -milliseconds 100; $acc = [math]::Round($acc*1.5)}; '\
        '$loc.position.location.latitude; '\
        '$loc.position.location.longitude; '\
        '$loc.position.location.horizontalaccuracy; '\
        '$loc.stop()' %(accuracy))

    p = sp.Popen(pshellcomm, stdin = sp.PIPE, 
                 stdout = sp.PIPE, stderr = sp.STDOUT, text=True)
    
    (out, err) = p.communicate()
    out = re.split('\n', out)

    lat = float(out[0].split(',')[0]+'.'+out[0].split(',')[1])
    long = float(out[1].split(',')[0]+'.'+out[1].split(',')[1])
    lista_lat.append(lat)
    lista_lon.append(long)
    
    i=i+1
    print("LOCALIZAÇÃO "+str(i)+":"+"\n"+"Latitude:"+str(lat)+", "+"Longitude:"+str(long)+"\n")
    

df_track['Latitude'] = pd.DataFrame(lista_lat)
df_track['Longitude'] = pd.DataFrame(lista_lon)
display(df_track)
