import tkinter as tk
from tkinter import messagebox
from minio import Minio
from minio.error import S3Error
import os

# MinIO 연결 설정
MINIO_ENDPOINT = "gmilk.kr:9010"     # 혹은 gmilk.kr:9000 같은 도메인
ACCESS_KEY = "tadtium"
SECRET_KEY = "tadtium1234"
BUCKET_NAME = "tadtium"
FILE_PATH = "generated.zip"

# MinIO 클라이언트 생성
client = Minio(
    MINIO_ENDPOINT,
    access_key=ACCESS_KEY,
    secret_key=SECRET_KEY,
    secure=False  # HTTPS 사용 시 True
)

# 업로드 함수
def upload_to_minio():
    if not os.path.exists(FILE_PATH):
        messagebox.showerror("오류", "generated.zip 파일이 존재하지 않습니다.")
        return

    try:
        # 파일 이름 = MinIO에서 저장될 오브젝트 이름
        object_name = os.path.basename(FILE_PATH)

        # 업로드
        client.fput_object(
            BUCKET_NAME,
            object_name,
            FILE_PATH,
            content_type='application/zip'
        )

        messagebox.showinfo("성공", f"{object_name} 업로드 성공!")

    except S3Error as e:
        messagebox.showerror("MinIO 오류", str(e))

# tkinter GUI
root = tk.Tk()
root.title("MinIO 업로더")

upload_button = tk.Button(root, text="generated.zip MinIO에 업로드", command=upload_to_minio)
upload_button.pack(pady=20, padx=20)

root.mainloop()
