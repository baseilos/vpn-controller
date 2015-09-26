#!/bin/awk -f

# Parses VPN list
# Expected input is:
# VPN 'France' (non autostarted) is not running ... failed!
# VPN 'Germany' (non autostarted) is not running ... failed!
# VPN 'UK-London' (non autostarted) is not running ... failed!
# VPN 'US-SiliconValley' is running.
#
# Output is:
# France,0;
# Germany,0;
# UK-London,0;
# US-SiliconValley,1; 

{
   if ($1 == "VPN") { # Take only lines starting with VPN
      vpnName = $2;
      gsub(/\'/,"",vpnName); # Remove ' from VPN name
      isRunning = $0 !~ /failed/;
      printf "%s,%d;", vpnName, isRunning;
   }
}