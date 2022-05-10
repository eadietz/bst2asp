#!/usr/bin/env bash
for file in $(find . -type f -name ex\*.lp | sort) ; do
  echo "=============================================================================================="
  echo "Generating Plausibility for File $file"
  python plausibility.py $file || exit 3
done

python gen_table.py