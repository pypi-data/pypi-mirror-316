# superlimo
SuperPoint-based Lagrangian Ice MOtion algorithm

## Installation

Create environment
`mamba env create -f environment.yml`

Install SuperLIMo
`pip install superlimo`

## Usage
* Edit your config file (see examples/example_config.yml)
* Download Sentinel-1 SAFE files
* Run superlimo `derive-drift confilg_file.yml S1_FILE_NAME_0.SAFE S1_FILE_NAME_1.SAFE output_dir/output_file.npz`
* Read initial (`x0`, `y0`) and final (`x1`, `y1`) coordinates of the derived drift vectors from the output.
The quality of the vector (maximum cross-correlation) is in the `mcc` variable.