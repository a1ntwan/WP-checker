# WP-checker

This is my **WP account checker** made for some affiliate-manager guys, who had tones of lightweight wp-based websites.

The main features of the project are:
- Multithreading;
- POST and XML-RPC checking methods;
- Proxies;
- Url availability threshold;

## HOWTO:

To run the script just python3 wp_checker.py with some keys and arguments:
- __-S__ stays for standard method, it means that the script will use simple POST requests;
- __-X__ stays for XML-RPC based method, that may be effective but only if the appropriate option of the website is turned on;
- __-i__ stays for input file, the syntax should be: url@login:pass;
- __-o__ stays for output file;
- __-p__ stays for proxy file, with syntax appropriate for http/https proxies in python3 requests lib;
- __-t__ stays for response timeout, the default value is 10s;
- __-r__ stays for retry. This will retry the same url with different proxie as many times, as you want, before considering url as unreachable. The default value is 2.

__Requirements__:
- requests

I've also added Ansible playbook for both Debian-based and RH-based (compile from source) Linux distributions as a bonus (hope it still works) :)


