import customtkinter
import requests
import time
import os
import zipfile

url = "http://depeso.kro.kr/game/tatum/vi/rot/vi.txt"
url3 = "http://depeso.kro.kr/game/tatum/vi/rot/vi2.txt"
url2 = "http://depeso.kro.kr/game/tatum/vi/rot/u.txt"
def run():
    e = open("config/what.txt","r")
    what = e.readline() # 맥 윈도우 구분
    e.close()
    if what == "windows":
        response2 = requests.get(url3)
        response.raise_for_status()
        os.system("main-game/",response2)
    exit()
def e():
    label2 = customtkinter.CTkLabel(master=app,text="다운로드 중입니다.. 프로그램을 끄지 말아주세요")
    label2.grid(row=0,column=0,padx=10,pady=30)
    app.after(1000,button_pressed)
def button_pressed():
    label2 = customtkinter.CTkLabel(master=app,text="압축해제 중입니다.. 프로그램을 끄지 말아주세요")
    label2.grid(row=0,column=0,padx=10,pady=30)
    e = open("config/what.txt","r")
    what = e.readline() # 맥 윈도우 구분
    e.close()
    e = open("config/link.txt","r")
    link = e.readlines()
    maclink=link[0].strip()
    windowslink = link[1].strip()
    e.close
    print("맥인가 윈도운가:",what)
    print("다운로드를 시작합니다.")
    f = open("config/vis.txt","w")
    f.write(vis)
    f.close
    if what == "mac":
        download = requests.get(maclink)
        with open("game.zip", "wb") as f:
            f.write(download.content)

    else:
        download = requests.get(windowslink)
        with open("game.zip", "wb") as f:
            f.write(download.content)
    with zipfile.ZipFile("game.zip", "r") as zip_ref:
        zip_ref.extractall("main-game")
    label2 = customtkinter.CTkLabel(master=app,text="임시 파일을 삭제중입니다.. 프로그램을 끄지 말아주세요")
    label2.grid(row=0,column=0,padx=10,pady=30)
    os.remove("game.zip")
    if what == "windows":
        response2 = requests.get(url3)
        response.raise_for_status()
        os.system("main-game/",response2)
        app.after(2000,exit)
    else:
        app.after(2000,exit)
def chack():
    button.grid(row=1,column=1,padx=30,pady=30)
app = customtkinter.CTk()
app.title("자동 업데이트")
app.geometry("593,236")
button = customtkinter.CTkButton(app, text="Download",command=e)
response = requests.get(url)
response.raise_for_status()  # 요청에 실패하면 예외 발생
print("최신버전:",response.text)
vis = response.text # requests한 텍스트를 구함
f = open("config/vis.txt","r")
line = f.readline() # 현제 클라이언트의 버전 가져오기
print("현제 클라이언트의 버전:",line)
# ㅈㅁ 이름이 Rot_2025_05f이야?어우
if line != vis:
    print("최신 버전 발견!")
    label = customtkinter.CTkLabel(master=app,text="최신 버전이 있습니다!")
    label.grid(row=0,column=0,padx=10,pady=30)
    chack()
else:
    label = customtkinter.CTkLabel(master=app,text="이미 최신버전입니다. 5초후 게임이 실행됩니다!")
    label.grid(row=0,column=0,padx=10,pady=30)  
    app.after(5000,run)
f.close()
app.mainloop()