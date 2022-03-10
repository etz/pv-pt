import requests
for i in range(0,11000):
    url = "https://pvaz.net/" + str(i)
    try:
        r = requests.head(url)
        print("Testing URL: " + url, r.status_code, end="")
        if r.status_code == 301:
            log = print(" REDIR:", r.headers['Location'] + "\n")
            with open("redirlog.txt", "a") as myfile:
                myfile.write(r.headers['Location'])
        else:
            print("")
    except requests.ConnectionError:
        print("Error, failed connection")
