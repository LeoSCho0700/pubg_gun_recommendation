import requests
import pymysql
import json
from bs4 import BeautifulSoup
import re

def get_itemcode():
    liste = []
    url = "http://battlegrounds.inven.co.kr/dataninfo/item/"
    html = requests.get(url)
    soup = BeautifulSoup(html.text, 'html.parser')
    result1=soup.find_all('td', class_='title text_left')

    for i in result1:
        if int(i.find('a').attrs["href"].split("=")[1])>2000:
            pass
        else:
            liste.append(int(i.find('a').attrs["href"].split("=")[1]))

    return list(set(liste))


def crawler(itemcode):
    a=[]
    b=[]
    url = "http://battlegrounds.inven.co.kr/dataninfo/item/detail.php?itemcode=" + str(itemcode)
    html = requests.get(url)
    soup= BeautifulSoup(html.text,'html.parser')
    result1=soup.find('table', class_='detail_info').find_all('td')
    result2=soup.find_all('span', class_='bar')
    for i in result1:
        a.append(i.get_text())
    for i in result2:
        b.append(i["style"])

    name = a[0]
    ammunition = (a[3])
    type = a[1].split('(')[0]
    if type == 'Melee' or type == 'MISC' or type == 'Throwables':
        return 0
    else:
        recoil = int(b[2].split(':')[1].replace('%',''))
        if a[4]=='-':
            muzzleVelocity = -1
        else:
            muzzleVelocity = int(a[4].split()[0])
        magCapacity = int(re.findall("\d+", a[9])[0])
        deal = int(a[2])
        if a[7].count("초")==1:
            rateOfFire = a[7].replace('초','')
        elif a[7] == '-':
            rateOfFire = -1
        else:
            rateOfFire = a[7].replace('초', '').split()[1].split(')')[1]
    if type=='AR' or type == 'SMG':
        difficulty = float((recoil*5)/(muzzleVelocity*magCapacity*3*deal*2))
    elif type=='LMG':
        difficulty = float((recoil*4)/(muzzleVelocity*deal*3))
    elif type == 'DMR':
        difficulty = float((recoil*3)/(muzzleVelocity*3*magCapacity*deal*5))
    elif type == 'SG':
        difficulty = float((recoil*float(rateOfFire))/(magCapacity*deal*4))
    else:
        difficulty = float(100/(muzzleVelocity*5*magCapacity*deal*6))

    tuple = (name,ammunition,type,recoil,muzzleVelocity,magCapacity,deal,rateOfFire,float(difficulty*100000))

    return tuple

final = []
for i in get_itemcode():
    if i == 1106 or i>=1900 or (i>=1700 and i<1800) or (i>=1400 and i<1500):
        pass
    else:
        final.append(crawler(i))

for i in final:

    user_db = pymysql.connect(user='root',password='*****',host='127.0.0.1',db='user',charset='utf8')

    sql="INSERT INTO user.PUBG(gun_name,gun_ammunition,gun_type,gun_recoil,gun_muzzleVelocity,gun_magCapacity,gun_deal,gun_rateOfFire,gun_difficulty)VALUES('%s','%s','%s',%s,%s,%s,%s,%s,%s);" % i

    cursor = user_db.cursor()
    cursor.execute(sql)
    user_db.commit()

# difficulty = (recoil*rate of fire)/(ammo*muzzleVelocity*magCapacity*deal)

