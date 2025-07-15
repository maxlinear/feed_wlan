#
# What is the purpose of this script? This script is meant to be used with feeds that target MxL
# repositories that are based on an open-source project. It helps setting up a feed for external
# release to our customers (and the inverse process, for internal release to our developers). See
# more in the README located at the root of this repository.
#
# What does this script?
#
# If the tool is configured for external release it will:
#
#   - Copy all patches located in "patches" folder to "patches_external".
#
#   - Modify the Makefile to point to "patches_external" in order to apply those patches on top of
#     the open-source repository (PATCH_DIR variable).
#
#   - Modify the Makefile to point to the open-source repository at a specific reference (tag or
#     hash) (OS_REPO_URL and OS_FORK_REF variables)
#
# If the tool is configured for internal release it will:
#
#   - Remove previously copied patches from "patches" folder in "patches_external".
#
#   - Modify the Makefile to point to "patches" in order to apply only internal patches (PATCH_DIR
#     variable).
#
#   - Modify the Makefile to point to the internal MxL fork of the open-source repository at a
#     specific reference (tag or hash) (OS_REPO_URL and OS_FORK_REF variables)
#

import os
import glob
import shutil
import argparse
import fileinput
import sys


####################################################################################################
# Constants
####################################################################################################

INTERNAL_PATCH_MINIMUM_INDEX = 9000
OSS_PKG_SOURCE_URL           = "https://w1.fi/hostap.git"
OSS_PKG_SOURCE_VERSION       = "033634019ddf8a2a12ad9c367d82cce6275804a5"
REVIEWER_PATCH_TO_REMOVE     = ["0113-WLANRTSYS-59677-Add-REVIEWERS.txt-to-all-WLAN-repos.patch"]
PATCH_DIR                    = "./patches_external"

####################################################################################################
# Auxiliary functions
####################################################################################################

def search_var_value(line: str, key: str):
    clean_line = line.lstrip("#")
    clean_line = clean_line.lstrip(" ")

    if not ":=" in clean_line:
        return None

    line_key, line_value = clean_line.split(":=")

    return line_value if key == line_key else None


def set_makefile_var(makefile_path: str, key: str, value):
    with fileinput.FileInput(makefile_path, inplace=True) as makefile:
        for line in makefile:
            line_has_key = search_var_value(line, key)
            final_line = line

            if line_has_key:
                final_key   = final_line.split(':=')[0]
                final_value = str(value).rstrip("\n")
                final_line  = f"{final_key}:={final_value}\n"

                print(f"Setting <{final_key}> to <{final_value}>...", file=sys.stderr)

            print(final_line, end="")


def read_makefile_var(makefile_path: str, key: str):
    with open(makefile_path) as makefile:
        for line in makefile:
            value = search_var_value(line, key)

            if value:
                return value


####################################################################################################
# Main code
####################################################################################################

parser = argparse.ArgumentParser(description="Set the release mode of a feed. This process updates the Makefile and sets up correctly the patches to use.")
parser.add_argument("feed_dirname", help="directory name of the feed. E.g. iwlwav-hostap-ng-uci")
parser.add_argument("release_mode", choices=["external", "internal"], help="release mode")
parser.add_argument("-psv", "--pkg-source-version", help="only if in internal release mode, PKG_SOURCE_VERSION value to use")

args = parser.parse_args()
is_external_release = args.release_mode == "external"
is_internal_release = not is_external_release

if is_external_release and args.pkg_source_version:
    print("Ignoring --pkg-source-version argument. Not used in external release mode.")

if is_internal_release and not args.pkg_source_version:
    print("ERROR: --pkg-source-version argument is required if internal release mode is selected.")
    exit(-1)

feed_path               = os.path.join(os.getcwd(), "wlan_wave_feed", args.feed_dirname)
patches_path            = os.path.join(feed_path, "patches")
patches_external_path   = os.path.join(feed_path, "patches_external")
makefile_path           = os.path.join(feed_path, "Makefile")

print(f"Switching <{args.feed_dirname}> to {args.release_mode} release mode...\n")

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Set Makefile variables
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if is_external_release:
    set_makefile_var(makefile_path, "PKG_SOURCE_URL",       OSS_PKG_SOURCE_URL)
    set_makefile_var(makefile_path, "PKG_SOURCE_VERSION",   OSS_PKG_SOURCE_VERSION)
    set_makefile_var(makefile_path, "PKG_REV",              OSS_PKG_SOURCE_VERSION)
    set_makefile_var(makefile_path, "PATCH_DIR",            PATCH_DIR)
else:
    pkg_source_url      = "$(CONFIG_UGW_PKG_SOURCE_URL)/$(PKG_PROJECT)/$(PKG_SOURCE_NAME)"
    pkg_source_version  = args.pkg_source_version
    patch_dir           = "./patches"

    set_makefile_var(makefile_path, "PKG_SOURCE_URL",       pkg_source_url)
    set_makefile_var(makefile_path, "PKG_SOURCE_VERSION",   pkg_source_version)
    set_makefile_var(makefile_path, "PATCH_DIR",            patch_dir)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Copy or remove patches
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if is_external_release:
    readme_to_remove     = os.path.join(patches_external_path, "README")

    if os.path.isfile(readme_to_remove):
        os.remove(readme_to_remove)

    for patch_to_be_removed in REVIEWER_PATCH_TO_REMOVE:
        junk_patch_to_remove =  os.path.join(patches_external_path, patch_to_be_removed)

        if os.path.isfile(junk_patch_to_remove):
            os.remove(junk_patch_to_remove)
else:
    external_dir_patches = glob.glob(os.path.join(patches_external_path, "*.patch"))
    patches_to_remove = []

    # Searching patches that were copied previously from "patches" folder. The patches to remove are
    # the ones whose index is equal or higher than the constant INTERNAL_PATCH_MINIMUM_INDEX.
    for patch_path in external_dir_patches:
        filename = os.path.basename(patch_path)     # E.g. 0001-WLANRTSYS-45977-OneWiFi(...)
        patch_index = int(filename.split("-")[0])   # E.g. 0001
        is_internal_patch = patch_index >= INTERNAL_PATCH_MINIMUM_INDEX

        if is_internal_patch:
            patches_to_remove.append(patch_path)

    for patch_path in patches_to_remove:
        print(f"Removing <{patch_path}>...")
        os.remove(patch_path)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Finish
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

print("\nSUCCESS")
