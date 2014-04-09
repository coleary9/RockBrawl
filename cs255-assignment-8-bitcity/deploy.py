#!/usr/bin/env python
# BitCity Studios:
# Cameron O'Leary <coleary9@jhu.edu>
# Steve Griffin  <sgriff27@jhu.edu>
# Jeremy Dolinko <j.dolinko@gmail.com>
# Jonathan Rivera <jriver21@jhu.edu>
# Michael Shavit  <shavitmichael@gmail.com>


import os
from subprocess import call, check_output
import argparse
import mmap

# Deploys an assignment.
# Cleans trash dirs and archives from previous deployments,
# autopep8s all python files or complains if not possible,
# checks for the presence of team member names/emails in python files,
# maintains whitelists of allowed files and file extensions and
# a blacklist of banned directories, copies all necessary files and folders
# into a new directory, makes the archive from the new directory,
# and runs the game from the new directory to make sure all needed files were
# copied over.

# Note: Relies heavily on hacky Unix command line calls. Will likely not work
# outside of Linux, Mac, or BSD-based operating systems.

# To deploy assignment 6:
# ./deploy.py 6

# Dependencies:
# pep8
# autopep8
# python 2.7
# *nix-based OS.

# Used to determine name for .tar.gz archive.
TEAM_NAME = 'bitcity'

# The main file to launch to test the deployment.
MAIN_FILE = 'main.py'

# Names and/or emails of team members. These are checked
# for presence in each .py file.
TEAM_MEMBERS = [
    "Cameron O'Leary <coleary9@jhu.edu>",
    "Steve Griffin  <sgriff27@jhu.edu>",
    "Jeremy Dolinko <j.dolinko@gmail.com>",
    "Jonathan Rivera <jriver21@jhu.edu>",
    "Michael Shavit  <shavitmichael@gmail.com>"
]

# Any directories whose names CONTAIN these strings will not
# be copied over.
bannedDirs = [
    ".",
    TEAM_NAME,
    "UNTITLED"
]

# Any files of these extensions will be copied over.
allowedFileExtensions = (
    ".py",
    ".png",
    ".jpg",
    ".ogg",
    ".mp3",
    ".wav",
    ".TTF",
    ".ttf",
    ".tmx"
)

# Any other files whose names ARE these strings will also be copied over.
allowedFiles = ["README"]

# Command and options for autopep8 on your system.
apep8 = ['autopep8', '--in-place', '--aggressive']


def main(**kwargs):
    newDirNum = kwargs['assignNumber'][0]
    try:
        deploy(newDirNum)
    except Exception as e:
        print 'Deployment failed.'
        print e
    else:
        print 'Deployment complete. There should be a new .tar.gz file'
        print 'and a new folder.'


def deploy(newDirNum):
    """Launches the deployment."""
    cwd = os.getcwd()
    removeTrash(cwd, newDirNum)

    # Make the new directory.
    newDir = getDirName(newDirNum)
    newDirFullName = getDirFullName(newDirNum)
    call(['mkdir', newDirFullName])

    # autopep8 and copy over the relevant files.
    for root, dirs, files in os.walk(cwd):
        # Don't copy directories that contain banned words.
        for bannedDir in bannedDirs:
            for dir in dirs:
                if bannedDir in dir:
                    dirs.remove(dir)
        print 'Working on ' + root
        relDir = os.path.relpath(root, cwd)
        newRelDir = os.path.join(newDirFullName, relDir)
        if not os.path.exists(newRelDir):
            call(['mkdir', newRelDir])
        for file in files:
            fullFile = os.path.join(root, file)
            if file.endswith('.py'):
                doPythonChecks(file, fullFile)
            # Copy over any allowed files.
            if file.endswith(allowedFileExtensions) or \
                    os.path.basename(file) in allowedFiles:
                relPath = os.path.relpath(fullFile, cwd)
                newPath = os.path.join(newDirFullName, relPath)
                call(['cp', fullFile, newPath])
                print '\t' + file
    # Compress the folder.
    call(['tar', '-czf', newDir + '.tar.gz', newDir])
    # Launch the game to make sure it works.
    # You'll need to change this if you launch from a bash script
    # or with some other command.
    call(['python', os.path.join(newDirFullName, MAIN_FILE)])


def removeTrash(cwd, newDirNum):
    """
    Remove any trash directores and .tar.gz
    from previous deployments if they exist.
    """
    for i in xrange(0, newDirNum + 1):
        dirFullName = getDirFullName(i)
        if os.path.exists(dirFullName):
            call(['rm', '-r', dirFullName])
        tarName = dirFullName + '.tar.gz'
        if os.path.exists(tarName):
            call(['rm', tarName])


def doPythonChecks(file, fullFile):
    """Do python file specific checks."""
    doPep8Checks(file, fullFile)
    doNameChecks(file, fullFile)


def doPep8Checks(file, fullFile):
    """Autopep8 any python files."""
    # Unfortunately ugly, but faster to pep8 twice. autopep8 doesn't
    # check to make sure it isn't already pep8'ed.
    try:
        check_output(['pep8', fullFile])
    except Exception:
        call([apep8[0], apep8[1], apep8[2], fullFile])
    try:
        check_output(['pep8', fullFile])
    except Exception:
        print 'MANUAL PEP8 OF ' + file + ' NECESSARY!'


def doNameChecks(file, fullFile):
    """Check that all team members' names/emails are in the file."""
    fileObj = open(fullFile)
    stringifiedFile = mmap.mmap(
        fileObj.fileno(), 0,
        access=mmap.ACCESS_READ)
    for name in TEAM_MEMBERS:
        if stringifiedFile.find(name) == -1:
            print name + ' is not in ' + file + '!'


def getDirFullName(num):
    directory = getDirName(num)
    return os.path.join(os.getcwd(), directory)


def getDirName(num):
    return 'cs255-assignment-' + str(num) + '-' + TEAM_NAME

if __name__ == '__main__':
    # Command line argument handling.
    parser = argparse.ArgumentParser(description='Deploy files', version='1.0')
    parser.add_argument('assignNumber', nargs='+',
                        type=int, help='Number of assignment')
    args = parser.parse_args()
    main(**vars(args))
