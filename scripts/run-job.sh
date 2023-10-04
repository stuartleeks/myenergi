#!/bin/bash
set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

resource_group_name=$(jq -r .resource_group_name "$script_dir/../infra/output.json")
if [[ ${#resource_group_name} -eq 0 ]]; then
  echo 'ERROR: Missing resource_group_name from infra/output.json' 1>&2
  exit 6
fi

job_name=$(jq -r .job_name "$script_dir/../infra/output.json")
if [[ ${#job_name} -eq 0 ]]; then
  echo 'ERROR: Missing job_name from infra/output.json' 1>&2
  exit 6
fi

az containerapp job start --resource-group "$resource_group_name" --name "$job_name"
