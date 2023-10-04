targetScope = 'subscription'

@description('Specifies the name of the resource group to deploy into')
param resourceGroupName string = 'home_energy'

@description('Specifies the supported Azure location (region) where the resources will be deployed')
param location string

@description('Specifies the serial number of the myenergi device to retrieve data for')
param myenergiSerialNumber string

@description('Specifies the API key to use to retrieve data from the myenergi API')
param myenergiApiKey string

@description('Specifies the default start date to use when retrieving data from the myenergi API for the first time')
param myenergiDefaultStartDate string = ''

resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
}

module apps 'modules/app.bicep' = {
  name: 'apps'
  scope: resourceGroup
  params: {
    location: location
    myenergiSerialNumber: myenergiSerialNumber
    myenergiApiKey: myenergiApiKey
    myenergiDefaultStartDate: myenergiDefaultStartDate
  }
}

output resource_group_name string = resourceGroup.name
output job_name string = apps.outputs.job_name

