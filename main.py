#!/usr/bin/env python
import package_manager
import argparse
import helpers
import user

def run():
    """Runs the whole shebang""" 
   
    parser = argparse.ArgumentParser()
    parser.add_argument('--install', '-i', help='installs a plugin to your plugin path')
    parser.add_argument('--remove', '-r', help='removes the specified plugin')
    parser.add_argument('--setname','-sn', help='Sets the username in the configuration file.')
    parser.add_argument('--setpath','-sp', help='Sets the plugin path for all downloaded packages to be moved to')
    parser.add_argument('--setos','-so', help='Sets the operating system in the configuration file.')
    parser.add_argument('--view', help="View all packages")
    args = parser.parse_args()
    manager = package_manager.PackageManager()
    reap_user = user.User()

    print(reap_user.name)
    print(reap_user.os)
    print(reap_user.plugin_path)
    if args.install:
        manager.manage_packages(args.install)  

    if args.view :
        manager.show_packages()

    if args.setname :
        reap_user.set_name(args.setname)

if __name__ == '__main__':
    run()
