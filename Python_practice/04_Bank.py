#함수를 이용해 입금, 출금, 수수료 부과하기(업그레이드)
#DB연결
import pymysql
lsg = pymysql.connect(host='localhost', user='root', password='0000', db='bankinfo', charset='utf8')

cur = lsg.cursor()

#랜덤 사용
from random import *

#지점 번호
shopnum = "1234"

#계좌 종류 판별 함수
def account_type(type) :
    if (type == 1 or type == 2) :
        YY = "01"
    elif (type == 3) :
        YY = "02"
    elif (type == 4) :
        YY = "25"
    elif (type == 5) :
        YY = "06"
    elif (type == 6) :
        YY = "18"
    elif (type == 7) :
        YY = "37"
    elif (type == 8) :
        YY = "90"
    else :
        print("번호를 잘못 입력하셨습니다.")
    return YY

#계좌 검증번호 생성 함수
def account_security() :
    sec = randint(0,9)
    return sec

#계좌 개설 함수
def open_account(age, IDcard):
    if(age>=17) :
        if(IDcard == "YES" or IDcard == "yes" or IDcard == "Y" or IDcard == "y") :
            print("주민등록번호를 입력해 주세요.(ex.000000-0000000) : ", end="")
            birth, pId = input().split("-")
            sql = "insert into ubirth values(%s,%s)"
            vals = (birth,pId)
            cur.execute(sql,vals)
            print("새로운 계좌를 개설합니다. 잠시만 기다려주세요.")
            print("계좌 종류를 선택해주세요(보통:1, 국고:2, 저축:3, 자유저축:4, 가계당좌:5, 당좌:6, 기업자유:7, 연계:8) : ", end="")
            type = int(input())
            YY = account_type(type)
            sec = account_security()
            sql = "insert into accoinfo values(%s, %s, %s, %s, null, %s)"
            vals = (birth, pId, shopnum, YY, str(sec))
            cur.execute(sql, vals)
            lsg.commit()
            sql = "select num from accoinfo where birth=%s and pId=%s"
            vals = (birth,pId)
            cur.execute(sql,vals)
            row = cur.fetchone()
            acco = shopnum+YY+str((7-len(str(row[0])))*"0")+str(row[0])+str(sec)
            print("계좌 개설을 완료했습니다. 계좌번호는 {0}입니다." .format(acco))
            sql = "insert into account values(null, %s, default)"
            vals = (acco)
            cur.execute(sql,vals)
            lsg.commit()
            print("계좌에 바로 입금하시겠습니까?(YES/NO) : ", end="")
            yn = input()
            if yn == "YES" or yn == "yes" or yn == "Y" or yn == "y" :
                print("입금할 금액을 입력해주세요. : ", end="")
                money = int(input())
                sql = 'select balance from account where acco=%s'
                vals = (acco)
                cur.execute(sql,vals)
                balance = cur.fetchone()
                balance = deposit(acco,balance,money)
                print("다른 업무를 보시겠습니까?(YES/NO) : ", end='')
                other = input()
                if other == 'YES' or other == 'yes' or other == 'Y' or other == 'y' :
                    bank()
                else :
                    print('은행 서비스를 종료합니다. 좋은 하루 보내세요.')
            else :
                print("다른 업무를 보시겠습니까?(YES/NO) : ", end='')
                other = input()
                if other == 'YES' or other == 'yes' or other == 'Y' or other == 'y' :
                    bank()
                else :
                    print('은행 서비스를 종료합니다. 좋은 하루 보내세요.')
            lsg.commit()
        else :
            print("주민등록증이 있어야 계좌개설이 가능합니다. 다른 업무를 보시겠습니까?(YES/NO) : ", end='')
            agin = input()
            if agin == 'YES' or agin == 'yes' or agin == 'Y' or agin == 'y':
                bank()
            else :
                print("은행 서비스를 종료합니다. 좋은 하루 보내세요.")
    else :
        print("17세 이상부터 계좌개설이 가능합니다. 다른 업무를 보시겠습니까?(YES/NO) : ", end='')
    # lsg.close()

#입력받은 계좌 정보 검색
def search(account) :
    Snum = account[0:4]
    Atype = account[4:6]
    Cnum = account[6:13]
    secu = account[13]
    sql = "select * from accoinfo where shopnum=%s and type=%s and num=%s and sec=%s"
    vals = (Snum,Atype,Cnum,secu)
    cur.execute(sql,vals)
    info = cur.fetchone()
    lsg.commit()
    return info

#계좌에 돈 입금 후 잔액 확인
def deposit(account, balance, money) :
    sql = "insert into deposit values(null, %s, %s)"
    vals = (account, money)
    cur.execute(sql, vals)
    sql = "update account set balance = %s where acco = %s"
    vals = (sum(balance,money), account)
    cur.execute(sql,vals)
    lsg.commit()
    print("{0}원을 입금했습니다. 잔액은 {1}원 입니다.".format(money, sum(balance,money)))
    lsg.commit()
    return balance

#계좌에 돈 출금 후 잔액 확인
def withdraw(account, balance, money) :
    sql = "select hour(curtime())"
    cur.execute(sql)
    time = cur.fetchone()
    time = int(str(time[0]))
    if time >= 9 and time < 18 :
        if int(str(balance[0])) >= int(money) :
            sql = "insert into withdraw values(null, %s, %s)"
            vals = (account, money)
            cur.execute(sql, vals)
            balance = int(str(balance[0]))
            sql = "update account set balance = %s where acco = %s"
            vals = (balance-money, account)
            cur.execute(sql,vals)
            lsg.commit()
            print("{0}원을 출금했습니다. 잔액은 {1}원 입니다.".format(money, balance-money))
        else :
            print("잔액이 부족합니다. 잔액은 {0}원 입니다.".format(int(str(balance[0]))))
    else :
        if int(str(balance[0])) >= int(money) :
            char = charge(money)
            money = money+char
            sql = "insert into withdraw values(null, %s, %s)"
            vals = (account, money)
            cur.execute(sql, vals)
            balance = int(str(balance[0]))
            sql = "update account set balance = %s where acco = %s"
            vals = (balance-money, account)
            cur.execute(sql,vals)
            lsg.commit()
            print("영업시간 외 {0}원을 출금했습니다. 수수료 {1}원이 부과됩니다. 잔액은 {2}원 입니다.".format(money, char, balance-money))
        else :
            print("잔액이 부족합니다. 잔액은 {0}원 입니다.".format(int(str(balance[0]))))
    lsg.commit()
    return balance

#수수료 부과
def charge(money) :
    if int(money) <= 100000 :
        char = 250
    else :
        char = 500
    return char

def bank() :
    print("은행에 오신것을 환영합니다. 해야하는 업무를 선택해주세요. (계좌개설:1, 입금:2, 출금:3) : ", end="")
    work = int(input())
    if (work == 1) :
        #계좌 개설에 필요한 정보 입력
        print("계좌를 개설하시려면 나이와 주민등록증 소지 여부(YES/NO)를 입력해주세요.(ex. 20,YES) : ", end="")
        age, IDcard = input().split(",")
        age = int(age)
        IDcard = str(IDcard)
        open_account(age, IDcard)
    elif (work == 2) :
        #입금에 필요한 정보 입력
        print("입금할 계좌를 입력해주세요(ex.1234567891234) : ", end="")
        account = input()
        info = search(account)
        if(info == None) :
            print("계좌를 찾을 수 없습니다. 다시 하시겠습니까?(YES/NO) : ", end="")
            agin = input()
            if agin == 'YES' or agin == 'yes' or agin == 'Y' or agin == 'y':
                bank()
            else :
                print("은행 서비스를 종료합니다. 좋은 하루 보내세요.")
        else :
            print("입금할 금액을 입력해주세요. : ", end="")
            money = int(input())
            sql = 'select balance from account where acco=%s'
            vals = (account)
            cur.execute(sql,vals)
            balance = cur.fetchone()
            balance = deposit(account,balance,money)
            print("다른 업무를 보시겠습니까?(YES/NO) : ", end="")
            agin = input()
            if agin == 'YES' or agin == 'yes' or agin == 'Y' or agin == 'y':
                bank()
            else :
                print("은행 서비스를 종료합니다. 좋은 하루 보내세요.")
    elif (work == 3) :
        #출금에 필요한 계좌 입력
        print("출금할 계좌를 입력해주세요(ex.1234567891234) : ", end='')
        account = input()
        info = search(account)
        if(info == None) :
            print("계좌를 찾을 수 없습니다. 다시 하시겠습니까?(YES/NO) : ", end="")
            agin = input()
            if agin == 'YES' or agin == 'yes' or agin == 'Y' or agin == 'y':
                bank()
            else :
                print("은행 서비스를 종료합니다. 좋은 하루 보내세요.")
        else :
            print("출금할 금액을 입력해주세요. : ", end="")
            money = int(input())
            sql = 'select balance from account where acco=%s'
            vals = (account)
            cur.execute(sql,vals)
            balance = cur.fetchone()
            balance = withdraw(account,balance,money)
            print("다른 업무를 보시겠습니까?(YES/NO) : ", end="")
            agin = input()
            if agin == 'YES' or agin == 'yes' or agin == 'Y' or agin == 'y':
                bank()
            else :
                print("은행 서비스를 종료합니다. 좋은 하루 보내세요.")
        lsg.close()

bank()