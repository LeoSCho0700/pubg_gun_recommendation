import curses
import time
import sys
import pymysql
import pandas
from pandas import Series
from pandas import Series, DataFrame




def intro_code():
    print("*" * 42)
    print("*" + "PUBG Mobile 유저들을 위한 상황별 총기 추천 프로그램" + "*")
    print("*" + "\t" * 10 + "*")
    print("*  " + "\t\t\tcode by Leo Cho" + "\t\t\t\t*")
    print("*" + "\t" * 10 + "*")
    print("*  " + "키워드 입력을 통해서 찾으려면 1번" + "\t\t\t\t*")
    print("*  " + "키워드 선택을 통해서 찾으려면 2번" + "\t\t\t\t*")
    print("*  " + "\t\t\t종료하려면 0번" + "\t\t\t\t\t*")
    print("*" + "\t" * 10 + "*")
    print("*" * 42)


def prog_code():
    a = int(input("Type Here : "))
    if a==1:
        samplehashtag = input()

        def function1(hashtags):
            m = hashtags.split("/")

            conn = pymysql.connect(host='localhost', user='root', password='*****!', db='user', charset='utf8')
            curs = conn.cursor()

            n = """SELECT * FROM user.PUBG WHERE"""
            for i in m:
                j = """ gun_hashtag like '%%%s%%'""" % i
                n = n + j

            curs.execute(n)

            rows = curs.fetchall()
            rows_list = list(rows)

            return rows_list

        print(function1(samplehashtag))
        prog_code()

    elif a==2:

        list=""

        print("************")
        print("* 사 녹 : 1 *")
        print("* 미라마 : 2 *")
        print("* 비켄디 : 3 *")
        print("* 에란겔 : 4 *")
        print("************")



        map= int(input())
        if map==1:
            list = """SELECT * FROM user.PUBG WHERE gun_sanhok=1"""
        elif map==2:
            list = """SELECT * FROM user.PUBG WHERE gun_miramar=1"""
        elif map==3:
            list = """SELECT * FROM user.PUBG WHERE gun_vikendi=1"""
        elif map==4:
            list = """SELECT * FROM user.PUBG WHERE gun_erangel=1"""
        else:
            print("wrong input")


        distance = int(input("거리를 입력하세요: "))
        if distance>=100:
            list=list+(" and gun_hashtag like '%%장거리%%'")
        elif distance <100 and distance >20:
            list=list+(" and gun_hashtag like '%%중거리%%'")
        else:
            list=list+(" and gun_hashtag like '%%근거리%%'")

        print("************")
        print("* 평지전 : 1 *")
        print("* 산악전 : 2 *")
        print("* 시가전 : 3 *")
        print("* 빼꼼전 : 4 *")
        print("* 차량전 : 5 *")
        print("************")

        a=int(input())
        if a==1:
            list=list+(" and gun_hashtag like '%%평지전%%'")
        elif a==2:
            list=list+(" and gun_hashtag like '%%산악전%%'")
        elif a==3:
            list=list+(" and gun_hashtag like '%%시가전%%'")
        elif a==4:
            list=list+(" and gun_hashtag like '%%빼꼼전%%'")
        elif a==5:
            list=list+(" and gun_hashtag like '%%차량전%%'")
        else:
            print("invalid")

        print("***************")
        print("*     9mm : 1 *")
        print("*  7.62mm : 2 *")
        print("*  5.56mm : 3 *")
        print("* .45 ACP : 4 *")
        print("* 12 게이지 : 5 *")
        print("***************")


        b=int(input())

        if b==1:
            list = list + (" and gun_ammunition ='9mm'")
        elif b==2:
            list = list + (" and gun_ammunition ='7.62mm'")
        elif b==3:
            list = list + (" and gun_ammunition ='5.56mm'")
        elif b==4:
            list = list + (" and gun_ammunition ='.45 ACP'")
        elif b==5:
            list = list + (" and gun_ammunition ='12 게이지'")
        else:
            print("invalid")

        conn = pymysql.connect(host='localhost', user='root', password='*****!',db='user', charset='utf8')
        curs = conn.cursor()

        curs.execute(list)

        rows = curs.fetchall()

        for i in rows:
            print("name: "+i[0]+" ammo: "+i[1]+" type: "+i[2]+" muzzle velocity: "+str(i[3])+" recoil: "+str(i[4])+" mag capacity: "+str(i[5])+" deal: "+str(i[6])+" rate of fire: "+str(i[7])+" difficulty: "+str(i[8])+"3 hashtag: "+str(i[-1]))
        prog_code()
    elif a==0:
        exit()
    else:
        print("선택지중에 다시 고르시오 휴먼")
        intro_code()
        prog_code()

intro_code()
prog_code()

