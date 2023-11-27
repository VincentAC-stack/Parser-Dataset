# Parser-Dataset
This is a parser for MuSoHu/SCAND Dataset.
## Basic Step:
### (1) First, create a general folder named `parser` and extract the compressed files into it.
### (2) According to requirement.txt, install the corresponding package. The command is:
```
pip install -r requirements.txt
```
### (3) Check the `musohu_parser.yaml` file and find that:
```
save_dir: "VAM/data/processed"
bags_dir: "VAM/data/musohu"
```
Therefore, we need to create `data/processed` and `data/musohu` subfolders in the `VAM` folder. After creation, we place the downloaded `.bag` file in the `musohu` folder and change sample_rate to 4.
### (4) When ready, return to the parser directory. 
First use `ls -l run.sh` to check the execution permissions of the `run.sh` file. If there is no `+x` executable permission, then `chmod +x run.sh`. Finally, run `./run.sh parser musohu`. If you encounter an error from rosbag, first `pip install bagpy`, and then run `./run.sh parser musohu`.
