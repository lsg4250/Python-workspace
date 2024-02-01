#문자열을 입력받아 첫글자 대문자로 변환

write = input()

Upper = write[0].upper()
lower = write[1:].lower()
print(Upper+lower)