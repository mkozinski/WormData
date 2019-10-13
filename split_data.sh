function getSplit {
  local IMGDIR=$1
  local LBLDIR=$2
  local trainFile=$3
  local testFile=$4
  if [[ -e $trainFile ]] ; then
    echo "Error: $trainFile exists"
    exit 1
  fi
  if [[ -e $testFile ]] ; then
    echo "Error: $testFile exists"
    exit 2
  fi
  echo -e "# image, label" >> $trainFile
  echo -e "trainFiles=[" >> $trainFile
  echo -e "# image, label" >> $testFile
  echo -e "testFiles=[" >> $testFile
  for A in $IMGDIR/*
  do
    echo $A
    randn=$(( $RANDOM % 4 ))
    if (( $randn < 3 )) ; then
      outfile=$trainFile
    else 
      outfile=$testFile
    fi
    I=`basename $A`
    R=${I%.*}
    if [[ -e $LBLDIR/${R}.npy ]]; then
      echo -en "[\"$IMGDIR/${R}.tif\", " >> ${outfile}
      echo -e  "\"$LBLDIR/${R}.npy\",]," >> ${outfile}
    else
      echo "skipping $R because it does not have a label"
    fi
  done
  echo -e "]" >> $trainFile
  echo -e "]" >> $testFile
}


echo "generating the split files"
#getSplit "$1" "$2" "$3" "$4"
getSplit AIY_neuron/AIY_tif AIY_neuron/AIY_gt trainFiles_AIY.txt testFiles_AIY.txt
getSplit AIA\&AIB_neurons/AIA\&AIB_tif AIA\&AIB_neurons/gt trainFiles_AIAAIB.txt testFiles_AIAAIB.txt
