#! /usr/bin/python3
import subprocess
import json

def notif(msg):
    cmd = ["notify-send", '-t', '4000', 'debug-info', msg]
    subprocess.run(cmd)

def run(*args):
    return subprocess.check_output(args)

def find_focused(tree):
    if tree['focused']:
        return tree
    for node in tree['nodes']:
        x = find_focused(node)
        if x:
            return x
    for node in tree['floating_nodes']:
        x = find_focused(node)
        if x:
            return x
    return None

def get_size_hint(text):
    for line in text.split('\n'):
        # if line.startswith('WM_NORMAL_HINTS(WM_SIZE_HINTS):'):
        line = line.strip()
        if (line.startswith('program specified size:') or 
            line.startswith('program specified minimum size:')):
            tmp = (line.split(':')[1]).strip().split(' by ')
            tmp = [int(t) for t in tmp]
            return tmp
    return None


def main():
    # notif('hello')
    tree = json.loads(run('i3-msg', '-t', 'get_tree').decode())
    focused = find_focused(tree)
    if focused is None:
        return

    is_a_float = '_on' in focused['floating']
    if is_a_float:
        run('i3-msg', '-t', 'command', 'floating', 'disable')
    else:
        window_id = focused['window']
        tmp = run('xprop', '-id', str(window_id)).decode()
        hint_size = get_size_hint(tmp)
        min_size = [1920 // 4, 1080 // 3]
        if hint_size is None:
            size = min_size
        else:
            size = [max(a,b) for a,b in zip(hint_size, min_size)]
        run('i3-msg', '-t', 'command', 'floating', 'enable',
            'resize', 'set', str(size[0]), str(size[1]))

if __name__ == '__main__':
    main()
