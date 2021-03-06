#!/usr/bin/env python3

import distutils.dir_util
import package_reader
import urllib.request
import urllib.error
import zipfile
import shutil
import json
import os


class PackageManager():
    """
    @archiveExtensions = A list of all valid extensions to check through. If the file ends in one of these
                         an attempt is made to unzip the file
    """

    archiveExtensions = {'zip'}
    vstExtensions = {'exe','dll'}

    def __init__(self, user):
        self.user = user
        self.reader = package_reader.JSONReader()

    def manage_packages(self, package_name):
        """A wrapper that downloads, extracts and moves the
        file"""
        print('Downloading', package_name)
        self.download(package_name)
        print('Unzipping', package_name)
        print('Moving', package_name,'to ',self.user.plugin_path)
        self.unzip(package_name)
        self.user.add_package(package_name)

    def show_packages(self):
        for package in self.reader.get_packages():
            print(package)

    def remove_package(self, package_name):
        """Removes an installed package from the users
        plugin_path. Note that this implementation will 
        probably need to be changed when we are managing
        different versions of the same package"""
        filepath = self.user.plugin_path + package_name
        #file removal here
        print("removed file" + filepath)

    def process_reapfile(self):
        """Installs the packages from a user's reapfile"""
        with open('reapfile.json') as reapfile:
            data = json.load(reapfile)

        for package in data['packages']:
            self.manage_packages(package['name'])

    def download(self, package_name):
        """Downloads @package_name from packages.json"""
        for url in self.reader.get_sources(package_name):
            try:
                urllib.request.urlretrieve(url, package_name)
                break
            except urllib.error.URLError:
                print('Unable to download from source, trying other sources')
            except ValueError : 
                print('Invalid package URL. Please report to package creator') #Give a link to the website when we have one

    def unzip(self, downloaded_file):
        """Creates a directory for the downloaded file, unzips it into that directory and removes
        the leftover file that was downloaded"""
        try :
            directory_name = downloaded_file
            os.mkdir(directory_name)
        except FileExistsError : 
            directory_name = downloaded_file + '_reap_get'
            os.mkdir(downloaded_file + '_reap_get')
        
        unzipper = zipfile.ZipFile(downloaded_file)
        unzipper.extractall(directory_name)
        unzipper.close()
        self.move(directory_name)
        os.remove(downloaded_file)

    def move(self, old_directory):
        """Moves the extracted file(s)
        to the user's plugin path"""
        distutils.dir_util.copy_tree(old_directory, self.user.plugin_path +'\\' + old_directory)


