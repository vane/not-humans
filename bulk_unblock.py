#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse

def remove(plan = True, zone='FedoraWorkstation'):
    rules = os.popen(f'firewall-cmd --list-all --zone={zone}').read()
    started = False
    for r in rules.split('\n'):
        if not r or not started:
            if r.strip() == 'rich rules:':
                started = True
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
    args = parser.parse_args()
    remove(args.plan, args.zone)
