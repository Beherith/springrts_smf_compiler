import argparse
import hashlib
from itertools import zip_longest
from pathlib import Path
import re
import shutil
import struct
import subprocess
import time
import traceback
from typing import Optional


# NOTE: tuple[] typing syntax requires python 3.9 or later
def decompile(pymapconv_path: Path, smf_path: Path, folder_label: str) -> tuple[float, Path]:
    """
    Returns:
    - duration taken to decompile
    - path to folder containing output files
    - path to compilation_settings txt file
    """
    maps_folder = smf_path.parent
    decompile_output_folder = maps_folder / folder_label
    shutil.rmtree(decompile_output_folder, ignore_errors=True)
    decompile_output_folder.mkdir(exist_ok=True)

    # Make sure there isn't a compilation_settings file in the folder already
    try:
        compilation_settings: Path = (
            maps_folder / list(maps_folder.glob("*_compilation_settings.txt"))[0]
        )
        compilation_settings.unlink()
    except Exception:
        pass

    # Keep track of contents of maps folder, so we can see what files
    # were created by the decompiler
    map_folder_contents = set(maps_folder.iterdir())

    # Decompile and time duration
    start = time.perf_counter()
    subprocess.run([pymapconv_path, "--decompile", smf_path])
    end = time.perf_counter()
    duration = end - start

    # Move all created files into new folder
    new_map_folder_contents = set(maps_folder.iterdir()) - map_folder_contents
    for f in new_map_folder_contents:
        f.rename(decompile_output_folder / f.name)

    return duration, decompile_output_folder


def update_compilation_settings_paths(compilation_settings_path: Path):
    """
    Updates paths in compilation_settings.txt to account for being moved into py2_decompile/py3_decompile folder
    """
    map_name = compilation_settings_path.name.replace("_compilation_settings.txt", "")
    folder_name = compilation_settings_path.parent.name

    def replacer(matchobj):
        if matchobj:
            return str(Path("maps", folder_name, matchobj.group(1)))

    with open(compilation_settings_path, "rt") as fin:
        content = fin.read()
        content = re.sub(
            r"maps[\/\\](" + map_name + r"_[^\/\\\n]+)$", replacer, content, flags=re.MULTILINE
        )
    with open(compilation_settings_path, "wt") as fout:
        fout.write(content)


def compile(pymapconv_path: Path, compilation_settings_path: Path) -> tuple[float, Path]:
    """
    Returns duration taken to compile and path to smf file
    """
    maps_subfolder = compilation_settings_path.parent

    # Keep track of contents of maps subfolder, so we can see what files were
    # created by compiling
    folder_contents = set(maps_subfolder.iterdir())

    # Gather args from compilation_settings txt file
    with open(compilation_settings_path, "rt") as fin:
        settings = fin.read().strip()
    settings_list = settings.split("\n")

    # Compile and time duration
    start = time.perf_counter()
    subprocess.run([pymapconv_path, *settings_list])
    end = time.perf_counter()
    duration = end - start

    # Return list of all created files, so we can diff them
    new_folder_contents = set(maps_subfolder.iterdir()) - folder_contents

    return duration, new_folder_contents


def diff_files_in_folders(
    old_folder: Path, new_folder: Path, only_filenames: list[str] = None
) -> list[tuple[Optional[Path], Optional[Path]]]:
    """
    Returns a list of (old_path, new_path) tuples for files that differ.

    If a file exists in one folder but not the other, then the corresponding
    tuple element will be None. For example, if comparing folders A and B and
    folder A contains file foo but B doesn't, then this function returns
    [("A/foo", None)].
    """
    files_that_differ = []
    old_files = list(
        sorted(
            f.name for f in old_folder.iterdir() if not only_filenames or f.name in only_filenames
        )
    )
    new_files = list(
        sorted(
            f.name for f in new_folder.iterdir() if not only_filenames or f.name in only_filenames
        )
    )
    if old_files != new_files:
        print(f"WARNING: Folders {old_folder} and {new_folder} contain different files!")
        print(f"{old_files} != {new_files}")

    for old_file, new_file in zip_longest(old_files, new_files):
        if old_file is None:
            files_that_differ.append((None, new_folder / new_file))
        elif new_file is None:
            files_that_differ.append((old_folder / old_file, None))
        else:
            if old_file.endswith(".smf"):
                # Handle SMF files differently
                if diff_smf_files(old_folder / old_file, new_folder / new_file):
                    files_that_differ.append((old_folder / old_file, new_folder / new_file))
            else:
                # File name exists in both folders, so compare checksum of content
                if diff_files(old_folder / old_file, new_folder / new_file):
                    files_that_differ.append((old_folder / old_file, new_folder / new_file))

    return files_that_differ


def diff_files(old: Path, new: Path) -> bool:
    "Return True if files differ"
    with open(old, "rb") as fin_old, open(new, "rb") as fin_new:
        old_hash = hashlib.md5(fin_old.read()).hexdigest()
        new_hash = hashlib.md5(fin_new.read()).hexdigest()
        return old_hash != new_hash


def diff_smf_files(old: Path, new: Path) -> bool:
    "Return True if files differ"
    with open(old, "rb") as fin_old, open(new, "rb") as fin_new:
        # Replace random mapid with consistent value
        oldc = fin_old.read()
        newc = fin_new.read()
        oldc = oldc[:20] + struct.pack("< i", 1) + oldc[24:]
        newc = newc[:20] + struct.pack("< i", 1) + newc[24:]
        old_hash = hashlib.md5(oldc).hexdigest()
        new_hash = hashlib.md5(newc).hexdigest()
        return old_hash != new_hash


def main():
    parser = argparse.ArgumentParser(
        description="Decompile all smf map files in sdd folders in the given folder"
    )
    parser.add_argument("maps_folder", type=lambda p: Path(p).absolute())
    parser.add_argument("py2_decompiler", type=lambda p: Path(p).absolute())
    parser.add_argument("py3_decompiler", type=lambda p: Path(p).absolute())
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--maps",
        nargs="*",
        help="List of map names (e.g. great_divide_v1) to test (decompile and recompile). If not specified, ALL maps (.sdd folders) are tested.",
    )
    group.add_argument(
        "--maps-after",
        help="Map names following (greater than) this string will be tested (decompiled and recompiled).",
    )
    args = parser.parse_args()
    more_than_1_smf_file = []
    decompile_durations = {}
    decompile_mismatches = []
    compile_durations = {}
    compile_mismatches = []
    cached_output_path = Path("regression_test_output.txt")
    errors = {}

    for d in args.maps_folder.iterdir():
        if d.is_dir() and d.suffix == ".sdd":
            map_name = Path(d.name).stem
            if (
                (args.maps and map_name in args.maps)
                or (args.maps_after and map_name > args.maps_after)
                or (args.maps is None and args.maps_after is None)
            ):
                try:
                    maps_folder = d / "maps"

                    # Find smf file to feed to decompiler
                    smf_files = list(maps_folder.glob("*.smf"))
                    if len(smf_files) > 1:
                        more_than_1_smf_file.append(d.name)
                        print(f"WARNING: More than 1 smf file found in {d.name}: {smf_files}")
                    smf_path = maps_folder / smf_files[0]

                    # Decompile map with old and new versions of pymapconv
                    py2_duration, py2_folder = decompile(
                        args.py2_decompiler, smf_path, "py2_decompile"
                    )
                    py3_duration, py3_folder = decompile(
                        args.py3_decompiler, smf_path, "py3_decompile"
                    )
                    print(f"Py2 decompilation of {smf_path} took {py2_duration:.1f} s.")
                    print(f"Py3 decompilation of {smf_path} took {py3_duration:.1f} s.")
                    print()

                    decompile_durations[d.name] = {2: py2_duration, 3: py3_duration}

                    # Compare all files to make sure decompilation succeeded
                    diff_paths = diff_files_in_folders(py2_folder, py3_folder)
                    if diff_paths:
                        decompile_mismatches.extend(diff_paths)
                        print(
                            "WARNING: Decompiling with py2 and py3 versions of pymapconv produced different results in these files:"
                        )
                        print(diff_paths)

                    # Adjust paths inside compilation settings files to point to
                    # decompiled files that were moved into a new folder
                    py2_compilation_settings = (
                        py2_folder / list(py2_folder.glob("*_compilation_settings.txt"))[0]
                    )
                    update_compilation_settings_paths(py2_compilation_settings)
                    py3_compilation_settings = (
                        py3_folder / list(py3_folder.glob("*_compilation_settings.txt"))[0]
                    )
                    update_compilation_settings_paths(py3_compilation_settings)

                    # Compile map with old and new versions of pymapconv
                    py2_duration, py2_created_files = compile(
                        args.py2_decompiler, py2_compilation_settings
                    )
                    py3_duration, py3_created_files = compile(
                        args.py3_decompiler, py3_compilation_settings
                    )
                    compile_durations[d.name] = {2: py2_duration, 3: py3_duration}

                    # Compare all newly-created files to make sure output matches
                    # between old/new versions
                    py2_filenames = [p.name for p in py2_created_files]
                    diff_paths = diff_files_in_folders(
                        py2_folder, py3_folder, only_filenames=py2_filenames
                    )
                    if diff_paths:
                        compile_mismatches.extend(diff_paths)
                        print(
                            "WARNING: Compiling with py2 and py3 versions of pymapconv produced different results in these files:"
                        )
                        print(diff_paths)

                    with open(cached_output_path, "wt") as fout:
                        fout.write("Decompilation durations\n")
                        fout.write(repr(decompile_durations))
                        fout.write("\nCompilation durations\n")
                        fout.write(repr(compile_durations))

                        if more_than_1_smf_file:
                            fout.write("\nWARNING: Maps with more than 1 smf file\n")
                            fout.write(repr(more_than_1_smf_file))

                        fout.write(
                            "\nDecompilation differences (pymapconv didn't produce same decompile output!):\n"
                        )
                        fout.write(repr(decompile_mismatches))

                        fout.write(
                            "\nCompilation differences (pymapconv didn't produce same compile output!):\n"
                        )
                        fout.write(repr(compile_mismatches))

                        fout.write("\nErrors:\n")
                        fout.write(repr(errors))
                except Exception as exc:
                    errors[d.name] = traceback.format_exc()
                    print(traceback.format_exc())

    print("Decompilation durations")
    print(repr(decompile_durations))

    print("Compilation durations")
    print(repr(compile_durations))

    if more_than_1_smf_file:
        print("WARNING: Maps with more than 1 smf file")
        print(repr(more_than_1_smf_file))

    print("Decompilation differences (pymapconv didn't produce same decompile output!):")
    print(repr(decompile_mismatches))

    print("Compilation differences (pymapconv didn't produce same compile output!):")
    print(repr(compile_mismatches))

    print("Errors:")
    print(repr(errors))


if __name__ == "__main__":
    main()
