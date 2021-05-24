import psutil

def health():
    status = f"CPU: {psutil.getloadavg()[0]}% \
RAM: {psutil.virtual_memory().percent}% \
Disk: {psutil.disk_usage('/').percent}%"
    return status


if __name__ == "__main__":
    main()
