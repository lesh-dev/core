#!/usr/bin/env python

import httplib
import urllib
import os
import sys
import re
import time
import socket
import signal

timeInterval = 60
GShutdown = False

cSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""
/api/autodns.cfm
id={your hostname}
&pw={your hostname's password}
&client=dd-wrt
"""


def SignalHandler(signum, frame):
    print "Signal handler called with signal", signum
    GShutdown = True
    cSock.close()
    sys.exit(3)


def Log(msg):
    try:
        f = open("dtdns-updater.log", "a")
        f.write(TimeStamp() + " " + msg + "\n")
        f.close()
    except IOError:
        print "Cannot log operation. "


def ParseResp(text):
    m = re.search("Host [A-Za-z0-9\.]+ now points to ([0-9]+\.[0-9]+\.[0-9]+\.[0-9]+)", text)
    if not m:
        Log("Cannot parse response. ")
        raise RuntimeError("Unknown server resonse text")
    ip = m.group(1)
    return ip


def GetMyIp():
    # socket.gethostbyname(hostName)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.connect(("ya.ru", 80))
    ip = sock.getsockname()[0]
    sock.close()
    return ip


def UpdateHost(hostName, passwd):
    try:
        conn = httplib.HTTPSConnection("www.dtdns.com")
        request = {
            "id":     hostName,
            "pw":     passwd,
            "client": "curl"
        }

        # print "Request params: ", params

        params = urllib.urlencode(request)
        conn.request("GET", "/api/autodns.cfm?" + params)

        resp = conn.getresponse()
        Log("Server resonse: " + str(resp.status) + ", " + resp.reason)
        if resp.status == 200:
            Log("Request OK")
        elif resp.status == 302:
            Log("Got 302 (redirect), reading new location. ")
            loc = resp.getheader("location")
            Log("Location: " + loc)
            loc = loc.replace("http://", "")
            slash = loc.index('/')
            base = loc[:slash]
            url = loc[slash:]
            conn = httplib.HTTPConnection(base)
            conn.request("GET", url)
            resp = conn.getresponse()
            if resp.status != 200:
                raise RuntimeError("Redirect failed.")
        else:
            raise RuntimeError("Request failed. HTTP error code: " + str(resp.status) + ", reason: " + resp.reason)

        Log("Response details: ")
        respText = resp.read().strip()
        Log(respText)
        return ParseResp(respText)
    except IOError:
        raise RuntimeError("Connection to dtdns.com timed out. ")


def TimeStamp():
    return time.strftime("%Y-%d-%m %H:%M:%S ", time.localtime())


def RunDaemon(hostName, passwd):
    Log("Running periodic update for host " + hostName)
    # update once and save ip.
    remoteIp = "0.0.0.0"
    try:
        remoteIp = UpdateHost(hostName, passwd)
        Log("Initial remote ip set: " + remoteIp)
    except IOError as e:
        Log("Initial host update failed. " + str(e))

    cnt = 0
    while True:
        cnt = (cnt + 1) % 60
        try:
            currentIp = GetMyIp()
            # Log("Host resolved to: " + currentIp)
            if currentIp != remoteIp:
                Log("Current ip " + currentIp + " is not matching, updating. ")
                remoteIp = UpdateHost(hostName, passwd)
            else:
                pass
                # if cnt == 0:
        except IOError as (code, text):
            Log("IO Error occured during update: " + text)
        except RuntimeError as e:
            Log("Generic Error occured during update: " + str(e))
        except Exception as e:
            Log("Generic exception in RunDaemon. " + str(e))

        if cnt == 0:
            Log("Host is up-to-date: " + currentIp)
        time.sleep(timeInterval)
        if GShutdown:
            Log("Shutdown signal received")
            break


if __name__ == '__main__':

    signal.signal(signal.SIGTERM, SignalHandler)

    args = sys.argv[:]

    daemonMode = False

    if "-d" in args or "--daemon" in args:
        args = filter(lambda x: x != "-d" and x != "--daemon", args)
        daemonMode = True

    if len(sys.argv) < 3:
        print "Wrong parameters. Syntax:"
        print " dtdns-update.py [-d|--daemon] <dtdns-hostname> <password>"
        sys.exit(1)

    hostName = args[1]
    passwd = args[2]

    if daemonMode:
        try:
            cSock.bind(("127.0.0.1", 6444))
            cSock.listen(1)
        except IOError:
            Log("Another instance is running, exiting. ")
            sys.exit(1)

        try:
            RunDaemon(hostName, passwd)
        except KeyboardInterrupt:
            Log("Keyboard interrupt received, exiting")

        cSock.close()
    else:
        UpdateHost(hostName, passwd)
