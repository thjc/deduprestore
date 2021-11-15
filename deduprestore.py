#!/bin/python3

import os
import sys
import hashlib

primary_files = {}

def populate_primary_names(primary_store):
    for dirName, _, fileList in os.walk(primary_store):
        print('Searching primary directory: %s' % dirName)
        for fname in fileList:
            primary_files.setdefault(fname, []).append([os.path.join(dirName, fname), None])

def hash_file(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(1000000), b""):
            hash_md5.update(chunk)
    return hash_md5.digest()

def remove_duplicates_from_incoming(incoming_store, dupe_store, dry_run=False):
    for dirName, _, fileList in os.walk(incoming_store):
        print('Searching incoming directory: %s' % dirName)
        for fname in fileList:
            print(fname)
            if fname in primary_files:
                for item in primary_files[fname]:
                    if not item[1]:
                        item[1] = hash_file(item[0])
                    full_name = os.path.join(dirName, fname)
                    if hash_file(full_name) == item[1]:
                        if dry_run:
                            print("Remove Dup {}".format(full_name))
                        else:
                            print("Remove Dup {}".format(full_name))
                            dest_name = os.path.join(dupe_store, full_name)
                            if not os.path.exists(os.path.dirname(dest_name)):
                                os.makedirs(os.path.dirname(dest_name))
                            os.rename(full_name, dest_name)
                        break
                    else:
                        print("Not matching hash {} -> {}".format(full_name, item[0]))
            else:
                print("Not matching filename {}".format(fname))


def main(primary_store, incoming_store, dupe_dump):
    populate_primary_names(primary_store)
    remove_duplicates_from_incoming(incoming_store, dupe_dump)


if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: {} <primary> <incoming> <dupe>".format(sys.argv[0]))
        sys.exit(1)

    main(sys.argv[1], sys.argv[2], sys.argv[3])