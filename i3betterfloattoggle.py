#! /usr/bin/python3
import os
import subprocess
import json
import sqlite3

class DB:
    """
    Abstract away the persistance mechanism
    """
    instance =  None

    @classmethod
    def get_instance(cls):
        if DB.instance is None:
            DB.instance = DB()
        return DB.instance

    def __init__(self):
        if DB.instance is not None:
            raise Exception('multiple intances of DB class not allowed')

        user = os.environ.get('USER')
        if user is None:
            state_file_path = '/tmp/i3betterfloattoggle_state.db'
        else:
            confdir = '/home/{0}/.config'.format(user)
            if not os.path.isdir(confdir):
                os.mkdir(confdir)
            confdir = os.path.join(confdir, 'i3betterfloattoggle')
            if not os.path.isdir(confdir):
                os.mkdir(confdir)
            state_file_path = os.path.join(confdir, 'state.db')

        self.con = sqlite3.connect(state_file_path)
        self._check_require_init()

    def __del__(self):
        if hasattr(self, 'con'):
            self.con.close()

    def _check_require_init(self):
        """
        Check if we have just created the database and need to create the
        tables
        """
        cur = self.con.cursor()
        cmd = """SELECT name FROM sqlite_master
            WHERE type='table' AND name='window_size';"""
        res = cur.execute(cmd)
        if res.fetchone() is not None:
            # We are set
            return
        # Create the table
        cmd = """CREATE TABLE window_size (
            win_name TEXT PRIMARY KEY,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL);"""
        cur.execute(cmd)

    def store(self, win_name, width, height):
        cur = self.con.cursor()
        cmd = """INSERT OR REPLACE INTO window_size VALUES ('{0}',{1},{2});"""
        cmd = cmd.format(win_name, width, height)
        # print(cmd)
        cur.execute(cmd)
        self.con.commit()

    def lookup(self, win_name):
        cur = self.con.cursor()
        cmd = """SELECT * FROM window_size
            WHERE win_name = '{0}';"""
        cmd = cmd.format(win_name)
        # print(cmd)
        res = cur.execute(cmd)
        x = res.fetchone()
        if x is None:
            return None
        # print('res:', x)
        return x[1], x[2]

# Global instance to database
db = DB.get_instance()

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

def remember_win_size(win):
    user_defined_size = win['window_rect']
    name = win['window_properties']['instance']
    db.store(name, user_defined_size['width'], user_defined_size['height'])

def main():
    # notif('hello')
    tree = json.loads(run('i3-msg', '-t', 'get_tree').decode())
    focused = find_focused(tree)
    if focused is None:
        return
    # print(focused)

    is_a_float = '_on' in focused['floating']
    if is_a_float:
        remember_win_size(focused)
        run('i3-msg', '-t', 'command', 'floating', 'disable')
    else:
        win_name = focused['window_properties']['instance']
        res = db.lookup(win_name)
        if res is None:
            # We do not have a configuration stored for this app. Look at the
            # hints for fallback to a minimum value
            window_id = focused['window']
            tmp = run('xprop', '-id', str(window_id)).decode()
            hint_size = get_size_hint(tmp)
            min_size = [1920 // 4, 1080 // 3]
            if hint_size is None:
                size = min_size
            else:
                size = [max(a,b) for a,b in zip(hint_size, min_size)]
        else:
            # We have size preference for the window
            size = res
        run('i3-msg', '-t', 'command', 'floating', 'enable',
            'resize', 'set', str(size[0]), str(size[1]))

if __name__ == '__main__':
    main()
