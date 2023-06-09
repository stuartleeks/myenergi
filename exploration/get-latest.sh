#!/bin/bash
source ../.env

resp=$(curl -s --request GET   --url https://s18.myenergi.net/cgi-jday-Z${SERIAL_NUMBER}-2023-03-02   --digest -u "${SERIAL_NUMBER}:${API_KEY}")
resp_last=$(echo $resp | jq ".U${SERIAL_NUMBER} | last")
# echo $resp_last | jq -r '"\(.yr)-\(.mon)-\(.dom) \(.hr):\(.min) | gen: \(if .gep == null then 0 else .gep/(60*1000) end)kW exp: \(if .exp == null then 0 else .exp/(60*1000) end)kW imp: \(if .imp == null then 0 else .imp/(60*1000) end)kW"'
echo $resp_last | jq -r '"gen: \(if .gep == null then 0 else .gep/(60*1000) end)kW exp: \(if .exp == null then 0 else .exp/(60*1000) end)kW imp: \(if .imp == null then 0 else .imp/(60*1000) end)kW"'
