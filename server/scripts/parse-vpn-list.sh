#!/bin/sh

# Parses VPN list by calling 'service openvpn status' and parses output using awk script

cd `dirname $0`
cat test.data | awk -f parse-vpn-list.awk