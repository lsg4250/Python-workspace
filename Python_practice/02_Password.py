#웹 주소를 받아서 웹 주소의 비밀번호 생성

web = input()

cut = web[web.find("/")+2:web.find(".")]
pw = cut[0:3] + str(len(cut)) + str(cut.count("e")) + "!"

print(web + "의 비밀번호는 " + pw + "입니다.")