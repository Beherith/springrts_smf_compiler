import sys

# Update this string to indicate the version of the current release.
# In case of minor updates or bug-fixes, bump the PATCH
# In case of new features which are backwards compatible with the old version, bump the MINOR
# In case of breaking changes, bump the MAJOR
__VERSION__ = "0.5.3"

# Update this string to add some notes to the GitHub release.
__VERSION_DESC__ = """
    - Fix Compressonator CLI arguments to produce appropriately-sized files
"""

if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "--version"

    if action == "--description":
        print(__VERSION_DESC__.lstrip("\n").rstrip())
    elif action == "--version":
        print(__VERSION__)
