#!/bin/sh

cd `dirname $0`
VPN_NAME=$1
service openvpn start $VPN_NAME 