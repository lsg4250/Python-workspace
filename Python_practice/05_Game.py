#게임 만들기
from random import *
import time

attack_unit = []
solder_unit = []
tank_unit = []
stealth_unit = []

def divisionunit(addunit):
    if addunit == "보병":
        solder = Solder()
        solder_unit.append(solder)
    elif addunit == "탱크":
        tank = Tank()
        tank_unit.append(tank)
    elif addunit == "전투기":
        stealth = Stealth()
        stealth_unit.append(stealth)
    else:
        print("잘못 입력하셨습니다. 다시 입력해주세요.")
    

class Unit :
    def __init__(self, name, hp, speed):
        self.name = name
        self.hp = hp
        self.speed = speed
        print("{0} 유닛을 생성했습니다." .format(name))
        
    
    def move(self, location):
        # print("[지상 유닛 이동]")
        print("{0} : {1}시 방향으로 이동합니다. [속도 {2}]" .format(self.name, location, self.speed))

    def damaged(self, damage):
        print("{0} : {1}만큼 피해를 입었습니다." .format(self.name, damage))
        self.hp -= damage
        print("{0} : 현재 체력은 {1}입니다." .format(self.name, self.hp))
        if self.hp <= 0:
            print("{0} : 파괴됐습니다." .format(self.name))
    
    def unohp(self):
        self.nohp = False
        if self.hp <= 0:
            self.nohp = True
            return self.nohp
        else :
            self.nohp = False
            return self.nohp

class AttackUnit(Unit) :
    def __init__(self, name, hp, damage, speed):
        Unit.__init__(self, name, hp, speed)
        self.damage = damage

    def attack(self, location):
        print("{0} : {1}시 방향 적군을 공격합니다. [공격력 {2}]" .format(self.name, location, self.damage))


class Flyable :
    def __init__(self, flying_speed):
        self.flying_speed = flying_speed

    def fly(self, name, location):
        print("{0} : {1}시 방향으로 날아갑니다. [속도 {2}]" .format(name, location, self.flying_speed))

class FlyableAttackUnit(AttackUnit, Flyable):
    def __init__(self, name, hp, damage, flying_speed):
        AttackUnit.__init__(self, name, hp, damage, 0)
        Flyable.__init__(self, flying_speed)

    def move(self, location):
        # print("[공중 유닛 이동]")
        self.fly(self.name, location)

class BuildingUnit(Unit):
    def __init__(self, name, hp, location):
        super().__init__(name, hp, 0)
        self.location

class Solder(AttackUnit):
    def __init__(self):
        AttackUnit.__init__(self, "보병", 100, 10, 1)
    
    def booster(self):
        if self.hp > 10:
            self.hp -= 10
            print("{0} : 강화제를 사용합니다. (HP 10 감소)" .format(self.name))
        else:
            print("{0} : 체력이 부족해 기술을 사용할 수 없습니다." .format(self.name))

class Tank(AttackUnit):
    siege_developed = False

    def __init__(self):
        AttackUnit.__init__(self, "탱크", 350, 35, 3)
        self.siege_mode = False

    def set_siege_mode(self):
        if Tank.siege_developed == False:
            return
        
        if self.siege_mode == False:
            print("{0} : 시지 모드로 전환합니다." .format(self.name))
            self.damage *= 2
            self.siege_mode = True
        else:
            print("{0} : 시지 모드를 해제합니다." .format(self.name))
            self.damage //= 2
            self.siege_mode = False

class Stealth(FlyableAttackUnit):
    def __init__(self):
        FlyableAttackUnit.__init__(self, "전투기", 200, 25, 7)
        self.cloaked = False
    
    def cloaking(self):
        if self.cloaked == True:
            print("{0} : 은폐 모드를 해제합니다." .format(self.name))
            self.cloaked = False
        else:
            print("{0} : 은폐 모드를 설정합니다." .format(self.name))
            self.cloaked = True

def createunit():
    print("어떤 유닛을 생성하시겠습니까? (보병, 탱크, 전투기) : ", end="")
    addunit = input()
    add = divisionunit(addunit)
    attack_unit = solder_unit+tank_unit+stealth_unit


def game_start():
    print("[알림] 새로운 게임을 시작합니다.")
    print("유닛을 생성하시겠습니까?(YES/NO) : ", end="")
    yorn = input()
    while yorn == "YES" or yorn == "yes" or yorn == "Y" or yorn == "y":
        createunit()
        print("유닛을 더 생성하시겠습니까?(YES/NO) : ", end="")
        yorn = input()
    scount = len(solder_unit)
    tcount = len(tank_unit)
    stcount = len(stealth_unit)
    print("현재 생성된 유닛은 총 {0}개로 보병 : {1}개, 탱크 : {2}개, 전투기 : {3}개 입니다." .format(scount+tcount+stcount, scount, tcount, stcount))

    print("전투를 시작하시겠습니까?(YES/NO) : ", end="")
    yn = input()
    if yn == "YES" or yn == "yes" or yn == "Y" or yn == "y":
        print("적의 위치를 탐색중입니다...")
        time.sleep(1)
        point = randint(1, 12)
        print("적이 {}시 방향에 있습니다. 공격하시겠습니까?(YES/NO) : " .format(point), end="")
        yn = input()
        while yn == "NO" or yn == "no" or yn == "N" or yn == "n":
            print("위치를 다시 탐색합니다...")
            point = randint(1, 12)
            time.sleep(1)
            print("적이 {}시 방향에 있습니다. 공격하시겠습니까?(YES/NO) : " .format(point), end="")
            yn = input()
        
        for unit in solder_unit:
            unit.move(point)
            time.sleep(0.5)
        for unit in tank_unit:
            unit.move(point)
            time.sleep(0.5)
        for unit in stealth_unit:
            unit.move(point)
            time.sleep(0.5)
        
        if tcount > 0:
            print("이동 중 탱크의 시지모드를 개발하시겠습니까?(YES/NO) : ", end="")
            yn = input()
            if yn == "YES" or yn == "yes" or yn == "Y" or yn == "y":
                print("개발을 시작합니다.")
                time.sleep(5)
                Tank.siege_developed = True
                print("[알림] 탱크의 시지모드 개발이 완료되었습니다.")
            else :
                pass
        else:
            pass

        print("공격 장소에 전 유닛이 집결했습니다.")
        print("공격을 위한 준비를 시작해주세요.(S:준비 시작/T:대기) : ", end="")
        st = input()
        while st == "T" or st == "t":
            print('공격 대기중입니다. 공격 준비를 시작하시겠습니까?(S:준비 시작/T:대기) : ', end="")
            st = input()
        
        for unit in solder_unit:
            unit.booster()
            time.sleep(1)
        for unit in tank_unit:
            unit.set_siege_mode()
            time.sleep(1)
        for unit in stealth_unit:
            unit.cloaking()
            time.sleep(1)
        time.sleep(1)
        print("공격을 위한 준비를 완료했습니다.")
        time.sleep(1)
        print("공격을 시작합니다.")
        for unit in solder_unit:
            while unit.unohp() == False:
                for unit in solder_unit:
                    if unit.unohp() == True:
                        continue
                    else:
                        unit.attack(point)
                        time.sleep(0.5)
                        unit.damaged(randint(5,20))
                        time.sleep(1)
                for unit in tank_unit:
                    if unit.unohp() == True:
                        continue
                    else:
                        unit.attack(point)
                        time.sleep(0.5)
                        unit.damaged(randint(20,50))
                        time.sleep(1)
                for unit in stealth_unit:
                    if unit.unohp() == True:
                        continue
                    else:
                        unit.attack(point)
                        time.sleep(0.5)
                        unit.damaged(randint(5,20))
                        time.sleep(1)
            break

def game_over():
    print("Player : Good Game")
    print("[Player] 님이 게임에서 퇴장했습니다.")

game_start()
game_over()
