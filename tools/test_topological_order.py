#!/usr/bin/env python3
"""
Test the topological order of catkin_pkg using a workspace.

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
import time


# -----------------------------------------------------------------------------
# Parser
# -----------------------------------------------------------------------------
DESCRIPTION = """
Test the topological order of catkin_pkg.
"""

PARSER = argparse.ArgumentParser(description = DESCRIPTION,
                                 formatter_class = argparse.RawDescriptionHelpFormatter)
PARSER.add_argument('source',
                    action = 'store',
                    help = 'The source directory.')
ARGS   = PARSER.parse_args()


# -----------------------------------------------------------------------------
# Import catkin_pkg
# -----------------------------------------------------------------------------
try:
    from catkin_pkg.packages import find_packages
    from catkin_pkg.topological_order import topological_order_packages
except ImportError as exception:
    raise ImportError('Please adjust your PYTHONPATH before running this test: %s' % str(exception))


# -----------------------------------------------------------------------------
# Find all packages
# -----------------------------------------------------------------------------
START_TIME = time.time()
WORKSPACE_PACKAGES = find_packages(ARGS.source, exclude_subspaces=True, warnings=[])
print("Found %d packages in %.1f s" % (len(WORKSPACE_PACKAGES), time.time() - START_TIME))


# -----------------------------------------------------------------------------
# Determine topological order
# -----------------------------------------------------------------------------
START_TIME = time.time()
ORDERED_PACKAGES = topological_order_packages(WORKSPACE_PACKAGES)
print("Topological order took %.1f s" % (time.time() - START_TIME,))


# -----------------------------------------------------------------------------
# EOF
# -----------------------------------------------------------------------------
