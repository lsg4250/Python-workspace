import re
from tabulate import *
import time

n = re.compile('\D')
menu_list = [["오 리 지 널ㅤ",16000,"BEST"],["볼 케 이 노ㅤ",18000,"HOT🌶️"],["오븐 바사삭",17000,"BEST"],["고추 바사삭",18000,"HOT🌶️"],["맵단짠 칩킨",20000,"HOT🌶️"]]
original = 10
ocnt = 0
volcano = 10
vcnt = 0
oven_B = 10
ovcnt = 0
pepper_B = 10
pcnt = 0
SSS_chip = 10
scnt = 0
waiting = 1

class SoldOutError(Exception):
    def __init__(self, msg):
        self.msg = msg
    
    def __str__(self):
        return self.msg

try :
    def chickentype(chicken_type, amount):
        if chicken_type == "오리지널":
            global ocnt, original
            if ocnt > 1:
                original = amount
            ocnt += 1
            return original
        elif chicken_type == "볼케이노":
            global vcnt, volcano
            if vcnt > 1:
                volcano = amount
            vcnt += 1
            return volcano
        elif chicken_type == "오븐 바사삭":
            global ovcnt, oven_B
            if ovcnt > 1:
                oven_B = amount
            ovcnt += 1
            return oven_B
        elif chicken_type == "고추 바사삭":
            global pcnt, pepper_B
            if pcnt > 1:
                pepper_B = amount
            pcnt += 1
            return pepper_B
        elif chicken_type == "맵단짠 칩킨":
            global scnt, SSS_chip
            if scnt > 1:
                SSS_chip = amount
            scnt += 1
            return SSS_chip
        else:
            raise ValueError
    print("Welcome to the Oven Universe 환영합니다. 굽네치킨입니다.")
    menu = input("치킨 종류를 확인하시겠습니까?(YES/NO) : ")
    if menu == "YES" or menu == "yes" or menu == "Y" or menu == "y":
        print("{:>7} {:>20} {:>8}".format("Menu", "Price(원)", "Note"))
        for v in menu_list:
            menu, price, note = v
            print("{:<15} {:<12} {:<10}".format(menu, price, note))
        time.sleep(6)
        chicken_type = input("어떤 치킨을 주문하시겠습니까? : ")
        amount = chickentype(chicken_type, 10)
    while True:
        order = int(input("{0} 을 몇 마리 주문하시겠습니까? : ".format(chicken_type)))
        if order == n or order < 1 or order > 10 :
            raise ValueError
        else:
            if order > amount:
                raise SoldOutError("남은 치킨은 {0} 마리 입니다.".format(amount))
            else:
                print("[대기번호 {0}] {1} 마리를 주문했습니다.".format(waiting, order))
                waiting += 1
                amount -= order
                chickentype(chicken_type, amount)
                # print("[남은 치킨 : {0}]".format(amount))
                yn = input("치킨을 더 주문하시겠습니까?(YES/NO) : ")
                if yn == "YES" or yn == "yes" or yn == "Y" or yn == "y":
                    chicken_type = input("어떤 치킨을 주문하시겠습니까? : ")
                    amount = chickentype(chicken_type, amount)
                else:
                    break
except ValueError:
    print("값을 잘못 입력했습니다.")
except SoldOutError as err:
    print("재료가 소진돼 더 이상 주문을 받지 않습니다.")
    print(err)
finally:
    print("굽네치킨을 이용해주셔서 감사합니다.")