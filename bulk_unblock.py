#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse

def read(fpath):
    with open(fpath) as f:
        lines = f.readlines()
    out = []
    for line in lines:
        if line.startswith('###'):
            pass
        elif line.startswith(('#', '`', '\n')):
            pass
        elif line:
            out.append(line.strip('\n'))
    return out

def remove(plan = True, zone='FedoraWorkstation', file=None):
    only_ips = None
    if file:
        only_ips = read(fpath=file)
    rules = os.popen(f'firewall-cmd --list-all --zone={zone}').read()
    started = False
    for r in rules.split('\n'):
        if not r or not started:
            if r.strip() == 'rich rules:':
                started = True
            continue
        if only_ips:
            found = False
            for ip in only_ips:
                if ip in r:
                    found = True
            if not found:
                continue
        cmd = f"""sudo firewall-cmd --zone={zone} --remove-rich-rule='{r}'"""
        if plan:
            print(cmd)
        else:
            os.system(cmd)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', '-p', type=bool, default=True, action=argparse.BooleanOptionalAction)
    parser.add_argument('--zone', '-z', type=str, default="FedoraWorkstation")
    parser.add_argument('--file', '-f', type=str, default="firewall/README.md")
    args = parser.parse_args()
    remove(args.plan, args.zone, args.file)
