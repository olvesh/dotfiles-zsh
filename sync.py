#!/usr/bin/env python

"""
Dotfiles syncronization.
Makes symlinks for all files: ~/dotfiles/tilde/.bashrc => ~/.bashrc.
Based on https://gist.github.com/490016
"""

import os
import glob
from posixpath import lexists
import shutil

DOTFILES_DIR = os.path.dirname(os.path.realpath(__file__)) 
SOURCE_DIR = DOTFILES_DIR + "/tilde"

IGNORE = ['.DS_Store']

def force_remove(path):
	if os.path.isdir(path) and not os.path.islink(path):
		shutil.rmtree(path, False)
	else:
		os.unlink(path)

def is_link_to(link, dest):
	is_link = os.path.islink(link)
	is_link = is_link and os.readlink(link).rstrip('/') == dest.rstrip('/')
	return is_link

def main():
	os.chdir(os.path.expanduser(SOURCE_DIR))
	for filename in [file for file in glob.glob('.*') if file not in IGNORE]:
		dotfile = os.path.join(os.path.expanduser('~'), filename)
		source = os.path.join(SOURCE_DIR, filename).replace('~', '.')

		# Check that we aren't overwriting anything
		if os.path.lexists(dotfile):
			if is_link_to(dotfile, source):
				continue

			response = input("Overwrite file `%s'? [y/N] " % dotfile)
			if not response.lower().startswith('y'):
				print ("Skipping '%s'..." % dotfile)
				continue

			force_remove(dotfile)

		os.symlink(source, dotfile)
		print ("%s => %s" % (dotfile, source))
	
	# attempt to symlink ~/dotfiles to DOTFFILES_DIR if they are different
	dotfile_dir = os.path.join(os.path.expanduser('~'), "dotfiles")
	install_dir = os.path.abspath(DOTFILES_DIR)
	if dotfile_dir != install_dir:
		if not os.path.lexists(dotfile_dir):
			os.symlink(install_dir, dotfile_dir)
			print ("%s => %s" % (dotfile_dir, install_dir))
		else:
			print ("Skipping symlinking ~/dotfiles already exists")
	else:
		print ("Dotfiles already in correct place")





if __name__ == '__main__':
	main()
