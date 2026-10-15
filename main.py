import platform, subprocess, os
from CLI import CL_Interface

password="25"
video_path = "startMeme.mp4"
current_os = platform.system()
s=""

while True:
    s=input("Enter password:\n>> ")
    if (s==password):
        print("Good job bro.")
        break
    
    try:
        if current_os == "Windows": #Windows
            if (os.path.exists(video_path)):
                os.startfile(video_path)
            else:
                print("Starting video doesn't exist.")
                break
        elif current_os == "Darwin":  #macOS
            subprocess.run(["open", video_path], check=True)
        else:  #linux
            subprocess.run(["xdg-open", video_path], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi mở file: {e}")
    except FileNotFoundError:
        print("Không tìm thấy lệnh mở file trên hệ điều hành này.")


S=CL_Interface()