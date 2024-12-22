# axonemalyze
Calculate the circularity of axoneme picks from cryo-ET images.

# Functions
The code is split into two command-line functions:
- `segment_axonemes`
- `estimate_circularity`

Installing the package gives access to these functions. The command-line functions are to be run in that order.

For more help with these functions, use the `-h` flag.

## segment_axonemes
The function takes a directory as input. This directory should contain all files in the `.coords` format with the xyz coordinates of the picks.

Here is an example of how to run this function:
```
segment_axonemes test_data/
```

This function outputs a directory (default `segmented/`) in the input directory with a single `.csv` file per axoneme.

## estimate_circularity.py
This function takes a directory as input. This directory should contain all files in the `.csv` format as outputted by `segment_axonemes.py`.

Here is an example of how to run this function:
```
estimate_circularity test_data/segmented/
```

This function prints an average circularity for each axoneme that contains at least five doublets to the standard output.
