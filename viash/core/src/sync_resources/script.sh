#!/bin/bash

## VIASH START
par_input='_viash.yaml'
## VIASH END

extra_params=( )

if [ "$par_quiet" == "true" ]; then
  extra_params+=( "--quiet" )
fi
if [ "$par_dryrun" == "true" ]; then
  extra_params+=( "--dryrun" )
fi
if [ "$par_delete" == "true" ]; then
  extra_params+=( "--delete" )
fi

if [ ! -z ${par_exclude+x} ]; then
  IFS=":"
  for var in $par_exclude; do
    unset IFS
    extra_params+=( "--exclude" "$var" )
  done
fi


# Disable the use of the Amazon EC2 instance metadata service (IMDS).
# see https://florian.ec/blog/github-actions-awscli-errors/
# or https://github.com/aws/aws-cli/issues/5234#issuecomment-705831465
export AWS_EC2_METADATA_DISABLED=true


function sync_s3() {
  local s3_path="$1"
  local dest_path="$2"
    aws s3 sync \
    "$s3_path" \
    "$dest_path" \
    --no-sign-request \
    "${extra_params[@]}"
}

resources_detected=$(yq e '.info | has("test_resources")' "$par_input")
if [ "$resources_detected" == "false" ]; then
  echo "No test resources detected."
  exit 0
fi

# reformat the test resources into a pseudo-json that can be read line-by-line by bash
nr_res=$( yq e '.info.test_resources | length' "$par_input")

for ((i=0; i<nr_res; i++)); do
  type=$(yq e ".info.test_resources[$i].type" "$par_input")
  if [ "$type" == "s3" ]; then
    s3_path=$(yq e ".info.test_resources[$i].path" "$par_input")
    dest_path=$(yq e ".info.test_resources[$i].dest" "$par_input")
    sync_s3 "$s3_path" "$dest_path"
  fi
done

cp -r resources_test/ "$par_output"
