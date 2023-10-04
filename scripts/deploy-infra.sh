#!/bin/bash
set -e

script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

if [[ -f "$script_dir/../.env" ]]; then
	echo "Loading .env"
	source "$script_dir/../.env"
fi
if [[ -f "$script_dir/../_deploy.env" ]]; then
	echo "Loading _deploy.env"
	source "$script_dir/../_deploy.env"
fi

if [[ ${#LOCATION} -eq 0 ]]; then
  echo 'ERROR: Missing environment variable LOCATION' 1>&2
  exit 6
fi
if [[ ${#SERIAL_NUMBER} -eq 0 ]]; then
  echo 'ERROR: Missing environment variable SERIAL_NUMBER' 1>&2
  exit 6
fi
if [[ ${#API_KEY} -eq 0 ]]; then
  echo 'ERROR: Missing environment variable API_KEY' 1>&2
  exit 6
fi
if [[ ${#DEFAULT_START_DATE} -eq 0 ]]; then
  echo 'ERROR: Missing environment variable DEFAULT_START_DATE' 1>&2
  exit 6
fi

cat << EOF > "$script_dir/../infra/azuredeploy.parameters.json"
{
  "\$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentParameters.json#",
  "contentVersion": "1.0.0.0",
  "parameters": {
    "location": {
      "value": "${LOCATION}"
    },
	"myenergiSerialNumber": {
	  "value": "${SERIAL_NUMBER}"
	},
	"myenergiApiKey": {
	  "value": "${API_KEY}"
	},
	"myenergiDefaultStartDate": {
	  "value": "${DEFAULT_START_DATE}"
	}
  }
}
EOF

deployment_name="deployment-myenergi-${LOCATION}"
cd "$script_dir/../infra/"
echo "Starting Bicep deployment ($deployment_name)"
output=$(az deployment sub create \
  --location "$LOCATION" \
  --template-file main.bicep \
  --name "$deployment_name" \
  --parameters azuredeploy.parameters.json \
  --output json)
echo "$output" | jq "[.properties.outputs | to_entries | .[] | {key:.key, value: .value.value}] | from_entries" > "$script_dir/../infra/output.json"

