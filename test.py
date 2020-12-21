#!/usr/bin/env python3

import sys
from signal import signal, SIGINT
import os
import pwd
import subprocess
import shlex


def main():
    name = "hoeg"
#    r=run(f"bash -c 'DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus notify-send beckapp starting'", user_name="simon")
#    r=run("notify-send bla bla", user_name="simon", DBUS_SESSION_BUS_ADDRESS="unix:path=/run/user/1000/bus", log=print)
    r=notify("bla", "bla", user_name="simon", log=print)
    print(r)

def notify(title, message, user_name, log=None):
    """https://stackoverflow.com/questions/54640352"""
    pw_record = pwd.getpwnam(user_name)
    uid = pw_record.pw_uid
    dbus_address = f"unix:path=/run/user/{uid}/bus"
    run(f"notify-send '{title}' '{message}'",
        user_name=user_name, DBUS_SESSION_BUS_ADDRESS=dbus_address, log=log)

def run(command, user_name=None, log=None, **kwargs):
    """ https://janakiev.com/blog/python-shell-commands/ """
    blue = "\033[94m"
    endcolor = "\033[0m"
    log(f"Running '{blue}{' '.join(shlex.split(command))}{endcolor}' as '{user_name}'")
    env = os.environ.copy()
#    env = {}
    if user_name is not None:
        pw_record = pwd.getpwnam(user_name)
        if pw_record.pw_uid == os.getuid():
            demote = lambda *_: None
        else:
            env["HOME"] = pw_record.pw_dir
            env["LOGNAME"] = pw_record.pw_name
            env["USER"] = pw_record.pw_name
            def demote():
                os.setgid(pw_record.pw_gid)
                os.setuid(pw_record.pw_uid)
    else:
        demote = lambda *_: None
    for key, value in kwargs.items():
        env[key] = value
    try:
        print(env)
        process = subprocess.Popen(
            shlex.split(command),
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,
            preexec_fn=demote, env=env
        )
    except subprocess.SubprocessError as _:
        raise RuntimeError(f"Could not get the user permissions for user {user_name}")
    return _surveil_process(process, print)

def _surveil_process(process, log):
    # https://stackoverflow.com/questions/2996887/
    # how-to-replicate-tee-behavior-in-python-when-using-subprocess
    outstring = ""
    while process.poll() is None:
        line = process.stdout.readline()
        if line.strip():
            log(line.strip())
            outstring += line
    rest = process.stdout.read()
    if rest.strip():
        log(rest.strip())
        outstring += rest
    return process, outstring, process.returncode


def sigint_handler(signal_received, frame):
    print("\nExiting...")
    sys.exit()
    

if __name__ == "__main__":
    signal(SIGINT, sigint_handler)
    main()

