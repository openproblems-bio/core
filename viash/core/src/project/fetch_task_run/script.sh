#!/bin/bash

## VIASH START
par_input=s3://openproblems-nextflow/work/f6/8565066aee4771cc2790b92b4ac660
par_output=debug
## VIASH END

# remove output if it already exists
if [ -d "$par_output" ]; then
  rm -rf "$par_output"
fi

AWS_EC2_METADATA_DISABLED=true \
  aws s3 sync \
    "$par_input" \
    "$par_output" \
    --no-sign-request

cd "$par_output"

# Replace the miniconda aws with the system aws
sed -i 's#/home/ec2-user/miniconda/bin/\(aws .* s3 [^ ]*\)#\1 --no-sign-request#g' .command.run
sed -i 's#nxf_s3_download() {#&\n  echo "Downloading $1";#' .command.run

bash .command.run nxf_stage
