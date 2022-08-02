# Regression Tester

This tool decompiles and recompiles maps with different versions of pymapconv to
discover if changes to the code have caused changes in the program output (map
files).

It was initially used to ensure that upgrading pymapconv.py from python 2 to
python 3 didn't cause the program to produce different map files. Some argument
and folder names used by the script are labeled as py2/py3 but can be thought of
as "old"/"new".

## Setup

Required: Python 3.9 or later

To use the regression tester, you need 2 versions of pymapconv. For example, you
might build an exe file and save it as `old_pymapconv.exe`, then make code
changes and build a new exe file and save it as `new_pymapconv.exe`. Then, you
can pass both these exe files into the regression_tester script and it will
compare outputs produced by both versions.

You must also pre-prepare maps, by extracting them to a folder and naming the
folder with a `.sdd` extension. When you're done, there should be a `maps`
folder nested directly inside the `.sdd` folder.

## Usage

To see command line arguments and descriptions:

```
python regression_tester/regression_tester.py --help
```

Required arguments are:
1. Path to BAR maps folder
2. Path to old pymapconv executable
3. Path to new pymapconv executable

If no other arguments are specified, it will process ALL `.sdd` folders in your
BAR maps folder.

```
# Example usage
F:\Python310\python.exe regression_tester\regression_tester.py F:\Games\Beyond-All-Reason\data\maps old_pymapconv.exe new_pymapconv.exe
```

Alternatively, you may provide a `--maps` argument at the end of the command
line and specify map file names to test:

```
# Example usage (this will look for folders inside the BAR maps folder named comet_catch_remake_1.8.sdd, great_divide_v1.sdd, etc.)
F:\Python310\python.exe regression_tester\regression_tester.py F:\Games\Beyond-All-Reason\data\maps old_pymapconv.exe new_pymapconv.exe --maps comet_catcher_remake_1.8 great_divide_v1 tangerine_remake_1.0 mariposa_island_v2.4
```

Alternatively, you may provide a `--maps-after` argument to specify that the
regression tester script should start processing maps with a name greater than
the provided argument. This is useful if you're processing all maps but are
interrupted in the middle -- you can pick up where you left off.

```
# Example usage (this will start with the first map after great_divide_v1, e.g. greenest_fields_1.3)
F:\Python310\python.exe regression_tester\regression_tester.py F:\Games\Beyond-All-Reason\data\maps old_pymapconv.exe new_pymapconv.exe --maps-after great_divide_v1

# Example usage (this will start with the first map beginning with the letter m, e.g. mariposa_island_v2.4)
F:\Python310\python.exe regression_tester\regression_tester.py F:\Games\Beyond-All-Reason\data\maps old_pymapconv.exe new_pymapconv.exe --maps-after m
```

Compilation and decompilation results (durations, errors, and mismatches) will
be printed to terminal and saved to a file named `regression_test_output.txt` in
the current working directory. The `regression_test_output.txt` file is written
after each map processed, so if something crashes you don't lose all progress.

## Details

The only difference in output currently allowed by the regression tester is the
random mapid (bytes 20-23 of SMF files).

For more about the contents of SMF files, see
https://springrts.com/wiki/Mapdev:SMF_format