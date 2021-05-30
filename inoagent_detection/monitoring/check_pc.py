import psutil
# from speedtest import Speedtest

def health():
    status = f"CPU: {psutil.getloadavg()[0]}% \
RAM: {psutil.virtual_memory().percent}% \
Disk: {psutil.disk_usage('/').percent}%"
    return status


def main():
    # st = Speedtest()
    # print(st.download())
    # print(st.upload())
    pass


if __name__ == "__main__":
    main()

#pip install speedtest-cli
