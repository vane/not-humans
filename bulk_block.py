#!/usr/bin/env python
import os
import argparse


def run_reject(address, prefix='reject', plan=True, zone='FedoraWorkstation'):
    print(prefix, address)
    cmd = f"""sudo firewall-cmd --zone={zone} --add-rich-rule='rule family="ipv4" source address="{address}" log prefix="{prefix}" level="notice" reject'"""
    if plan:
        print(cmd)
    else:
        os.system(cmd)


def read(fpath, plan):
    with open(fpath) as f:
        lines = f.readlines()
    prefix = ''
    out = []
    for line in lines:
        if line.startswith('###'):
            prefix = line[3:].strip('\n')
        elif line.startswith(('#', '`', '\n')):
            pass
        elif line:
            out.append((line.strip('\n'), prefix, plan))
    return out


# -*- coding: utf-8 -*-
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', '-p', type=bool, default=True, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    cmd_args = read('firewall/README.md', args.plan)
    for cmd in cmd_args:
        run_reject(*cmd)
