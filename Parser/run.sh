#! /usr/bin/env bash

export PROJECT_NAME=VAM  # add your project folder to python path
export LOCAL_RANK=1
export NUM_TRAINERS=2 # number of GPUs you have
export PYTHONPATH=$PYTHONPATH:$PROJECT_NAME
export COMET_LOGGING_CONSOLE=info

Help()
{
   # Display Help
   echo 
   echo "Facilitates running different stages of training and evaluation."
   echo 
   echo "options:"
   echo "train_endtoend             Trains the end to end model."
   echo "train_barlow               Trains Barlow Twins."
   echo "parser                     Parse bag files."
   echo "run file_name              Runs file_name.py file."
   echo
}

run () {
  case $1 in
    train)
      if [[ -z $2 ]]
      then
        python $PROJECT_NAME/train_endtoend.py --conf $PROJECT_NAME/conf/config
      else
        echo "Using provided config file {$2} for training the end-to-end model."
        python $PROJECT_NAME/train_endtoend.py --conf $2
      fi
      ;;
    train_dist)
        torchrun --standalone --nnodes=1 --nproc-per-node=$NUM_TRAINERS $PROJECT_NAME/train_endtoend.py --conf $PROJECT_NAME/conf/config
      ;;
    train_barlow)
      if [[ -z $2 ]]
      then
        python $PROJECT_NAME/train_barlow.py --conf $PROJECT_NAME/conf/config_barlow
      else
        echo "Using provided config file {$2} for training Barlow Twins."
        python $PROJECT_NAME/train_barlow.py --conf $2
      fi
      ;;
    parser)
      if [[ $2 == 'musohu' ]]
      then
        echo "Using MuSoHu config file to Parse MuSoHu bags."
        python $PROJECT_NAME/utils/parser.py --conf $PROJECT_NAME/conf/musohu_parser

      elif [[ $2 == 'scand' ]]
      then
        echo "Using SCAND config file to Parse SCAND bags."
        python $PROJECT_NAME/utils/parser.py --conf $PROJECT_NAME/conf/scand_parser
      elif [[ $2 == 'sampler' ]]
      then
        echo "Creating samples from bag files!"
        python $PROJECT_NAME/utils/parser.py --conf $PROJECT_NAME/conf/config -cs
      else
        echo "{$2} does not exits!"
        python $PROJECT_NAME/utils/parser.py --conf $2 $3
      fi
      ;;
    run)
      python $2
      ;;
    -h) # display Help
      Help
      exit
      ;;
    *)
      echo "Unknown '$1' argument. Please run with '-h' argument to see more details."
      # Help
      exit
      ;;
  esac
}

run $1 $2 $3

# echo "Done."
