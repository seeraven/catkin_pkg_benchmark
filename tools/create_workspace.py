#!/usr/bin/env python3
"""
Copy the layout of an existing workspace into an anonymous one.

Copyright (c) 2020 by Clemens Rabe <clemens.rabe@clemensrabe.de>
All rights reserved.
This file is part of catkin_pkg_benchmark and is released under the
"BSD 3-Clause License". Please see the LICENSE file that is included
as part of this package.
"""


# -----------------------------------------------------------------------------
# Module Import
# -----------------------------------------------------------------------------
import argparse
import os
from xml.dom import minidom


# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------
DESCRIPTION = """
Copy the layout of an existing workspace into an anonymous one.
"""

PARSER = argparse.ArgumentParser(description = DESCRIPTION,
                                 formatter_class = argparse.RawDescriptionHelpFormatter)
PARSER.add_argument('-d', '--copy-directory-structure',
                    action = 'store_true',
                    default = False,
                    help = 'Copy the directory structure.')
PARSER.add_argument('-c', '--add-buildtool-catkin',
                    action = 'store_true',
                    default = False,
                    help = 'Add a buildtool_depend on catkin.')
PARSER.add_argument('source',
                    action = 'store',
                    help = 'The source directory.')
ARGS   = PARSER.parse_args()


# -----------------------------------------------------------------------------
# Build package cache
# -----------------------------------------------------------------------------

DEPEND_KEYS = ['depend', 'buildtool_depend', 'build_depend',
               'build_export_depend', 'exec_depend',
               'test_depend', 'doc_depend']

# We store for every found package the following information:
#  'dir':      directory of the package
#  depend_key: The depend key.
PACKAGE_CACHE = {}
FOUND_DIRS    = []

for root, _dirs, files in os.walk(ARGS.source):
    # Deleting dirs did not work, so we have to exclude subdirectories here
    FOUND = False
    for d in FOUND_DIRS:
        if root.startswith(d):
            FOUND = True
            break
    if FOUND:
        continue

    if 'package.xml' in files and 'CMakeLists.txt' in files:
        package_dom  = minidom.parse(os.path.join(root, 'package.xml'))
        package_name = package_dom.getElementsByTagName('name')[0].childNodes[0].data
        PACKAGE_CACHE[package_name] = {'dir':  root}
        for dep_key in DEPEND_KEYS:
            PACKAGE_CACHE[package_name][dep_key] = []
            for item in package_dom.getElementsByTagName(dep_key):
                PACKAGE_CACHE[package_name][dep_key].append(item.childNodes[0].data)

        FOUND_DIRS.append(root + '/')

print("Found %d packages." % len(PACKAGE_CACHE))


# -----------------------------------------------------------------------------
# Generate anonymized package names
# -----------------------------------------------------------------------------
NEW_PACKAGE_NAMES = {}
PKG_NR = 1
for package_name in PACKAGE_CACHE:
    if package_name not in NEW_PACKAGE_NAMES:
        NEW_PACKAGE_NAMES[package_name] = 'package%08d' % PKG_NR
        PKG_NR += 1

        for dep_key in DEPEND_KEYS:
            for dep_name in PACKAGE_CACHE[package_name][dep_key]:
                if dep_name in PACKAGE_CACHE and dep_name not in NEW_PACKAGE_NAMES:
                    NEW_PACKAGE_NAMES[dep_name] = 'package%08d' % PKG_NR
                    PKG_NR += 1


# -----------------------------------------------------------------------------
# Generate anonymized directory structure
# -----------------------------------------------------------------------------
NEW_PACKAGE_DIRS = {}
NEW_DIR_NAMES = {}
DIR_NR = 1
if not ARGS.copy_directory_structure:
    for package_name in PACKAGE_CACHE:
        NEW_PACKAGE_DIRS[package_name] = 'src/%s' % package_name
else:
    for package_name in PACKAGE_CACHE:
        # Extract directories between ARGS.source and package name
        SUBDIR = os.path.dirname(os.path.relpath(PACKAGE_CACHE[package_name]['dir'],
                                                 ARGS.source))
        NEW_SUBDIR = []
        for item in SUBDIR.split('/'):
            if item not in NEW_DIR_NAMES:
                NEW_DIR_NAMES[item] = 'dir%08d' % DIR_NR
                DIR_NR += 1
            NEW_SUBDIR.append(NEW_DIR_NAMES[item])

        if NEW_SUBDIR:
            NEW_PACKAGE_DIRS[package_name] = 'src/%s/%s' % ('/'.join(NEW_SUBDIR),
                                                            NEW_PACKAGE_NAMES[package_name])
        else:
            NEW_PACKAGE_DIRS[package_name] = 'src/%s' % NEW_PACKAGE_NAMES[package_name]


# -----------------------------------------------------------------------------
# Save packages
# -----------------------------------------------------------------------------
os.system("rm -rf src")
os.system("mkdir src")

for package_name in PACKAGE_CACHE:
    new_package_name = NEW_PACKAGE_NAMES[package_name]
    os.system("mkdir -p %s" % NEW_PACKAGE_DIRS[package_name])
    with open(os.path.join(NEW_PACKAGE_DIRS[package_name], 'package.xml'), "w") as f:
        f.write('<?xml version="1.0"?>\n')
        f.write('<package format="2">\n')
        f.write('  <name>%s</name>\n' % new_package_name)
        f.write('  <version>1.0.0</version>\n')
        f.write('  <description>Sample package for benchmark</description>\n')
        f.write('  <maintainer email="someone@somewhere.there">Some User</maintainer>\n')
        f.write('  <license>BSD</license>\n')

        if ARGS.add_buildtool_catkin:
            f.write('  <buildtool_depend>catkin</buildtool_depend>\n')

        for dep_key in DEPEND_KEYS:
            for dep_name in PACKAGE_CACHE[package_name][dep_key]:
                if dep_name in NEW_PACKAGE_NAMES:
                    f.write('  <%s>%s</%s>\n' % (dep_key, NEW_PACKAGE_NAMES[dep_name], dep_key))

        f.write('</package>\n')


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
