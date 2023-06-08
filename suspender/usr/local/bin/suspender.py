import subprocess
import pathlib
import sys
import time
import os
import syslog
import argparse

SLEEP_TIMEOUT = 10

POWER_STATE_PATH = pathlib.Path('/sys/power/state')
POWER_STATE = 'mem'

LID_PATH = pathlib.Path('/proc/acpi/button/lid')

BRIGHTNESS_PATH = pathlib.Path('/sys/class/backlight')
BRIGHTNESS_LIMIT = 0.5


def print_msg(msg):
    syslog.syslog(msg)


def run_shell(cmd: str, line: int = None, print_output=True):
    print_msg(cmd)
    output = subprocess.check_output(cmd, shell=True, text=True)
    if line is not None:
        output = output.splitlines()[line]
    if print_output:
        print_msg(output)
    return output


# mem suspend
def set_power_state():
    script_dir = pathlib.Path(__file__).parent

    run_shell(str(script_dir / 'mem_susp.sh'))


def reset_screens():
    time.sleep(1)
    print_msg('fix dual monitor black screen bug')
    os.environ['DISPLAY'] = ':0.0'
    run_shell('xset dpms force off')
    time.sleep(0.3)
    run_shell('xset dpms force on')


def reset_brightness():
    time.sleep(1)
    for device in BRIGHTNESS_PATH.iterdir():
        try:
            with (device / 'max_brightness').open('r') as f:
                max_level = int(f.readline())
            with (device / 'actual_brightness').open('r') as f:
                cur_level = int(f.readline())

            limit_level = int(BRIGHTNESS_LIMIT * max_level)

            print_msg('br level: max_level {} cur_level {} limit_level {}'.format(max_level, cur_level, limit_level))
            if cur_level > limit_level:
                break

            with (device / 'brightness').open('w') as f:
                print_msg('set level {}'.format(limit_level))
                f.write(str(limit_level))

            break

        except:
            continue


def reset_network():
    run_shell('nmcli networking off')
    time.sleep(0.3)
    run_shell('nmcli networking on')
    time.sleep(1)


def loginctl(lock: bool):
    if lock:
        run_shell('loginctl lock-sessions')
    else:
        run_shell('loginctl unlock-sessions')
    time.sleep(0.8)


def do_suspend():
    # bug: freeze on suspend when a sessions is locked.
    loginctl(False)

    # suspend
    set_power_state()

    # after suspend

    loginctl(True)

    reset_screens()
    reset_brightness()
    reset_network()

    # reset show actual time
    run_shell('systemctl restart systemd-timesyncd.service')
    time.sleep(1)


def need_suspend() -> bool:
    for led in LID_PATH.iterdir():
        state_file = led / 'state'
        with state_file.open('r') as f:
            state_line = f.readline()
            opened = state_line.find('open') != -1
            return not opened
    return False


def loop():
    while True:
        time.sleep(SLEEP_TIMEOUT)
        if need_suspend():
            time.sleep(5)
            if need_suspend():
                do_suspend()
        else:
            print_msg('no suspend')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--once', action='store_true')
    args = parser.parse_args()
    if args.once:
        do_suspend()
        sys.exit(0)

    loop()
