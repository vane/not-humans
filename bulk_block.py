#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse


def run_reject(address, existing=None, prefix='reject', plan=True, zone='FedoraWorkstation'):
    if not existing:
        existing = []
    rule = f"""rule family="ipv4" source address="{address}" log prefix="{prefix}" level="notice" reject"""
    if rule in existing:
        return False
    cmd = f"""sudo firewall-cmd --zone={zone} --add-rich-rule='{rule}'"""
    print(rule)
    if not plan:
        os.system(cmd)
    return True


def read_firewall_cmd_rules():
    fs = os.popen("firewall-cmd --list-all --zone=FedoraWorkstation")
    res = fs.read()
    rich_rules = []
    is_rich_section = False
    for line in res.split("\n"):
        if line.strip() == "rich rules:":
            is_rich_section = True
            continue
        if not is_rich_section:
            continue
        rich_rules.append(line.strip())
    return rich_rules


def read(fpath):
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
            out.append((line.strip('\n'), prefix))
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--plan', '-p', type=bool, default=True, action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    address_to_block = read('firewall/README.md')
    address_blocked = read_firewall_cmd_rules()
    stats = {'skipped': 0, 'executed': 0}
    for address, prefix in address_to_block:
        executed = run_reject(address, address_blocked, prefix, args.plan)
        if executed:
            stats['executed'] += 1
        else:
            stats['skipped'] += 1
    print(stats)
