@description('Specifies the supported Azure location (region) where the resources will be deployed')
param location string

@description('Specifies the serial number of the myenergi device to retrieve data for')
param myenergiSerialNumber string

@description('Specifies the API key to use to retrieve data from the myenergi API')
param myenergiApiKey string

@description('Specifies the default start date to use when retrieving data from the myenergi API for the first time')
param myenergiDefaultStartDate string = ''

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2021-12-01-preview' = {
  name: 'homeenergi'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource containerAppEnv 'Microsoft.App/managedEnvironments@2022-03-01' = {
  name: 'home-energi'
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}

resource myernergiApp 'Microsoft.App/jobs@2022-11-01-preview' = {
  name: 'myenergi'
  location: location
  // identity ?
  properties: {
    environmentId: containerAppEnv.id
    configuration: {
      scheduleTriggerConfig: {
        // https://learn.microsoft.com/en-us/azure/container-apps/jobs?tabs=azure-resource-manager#start-a-job-execution-on-demand
        // https://learn.microsoft.com/en-us/azure/templates/microsoft.app/jobs?pivots=deployment-language-bicep
        cronExpression: '*/30 * * * *'
        parallelism: 1
        replicaCompletionCount: 1
      }
      replicaRetryLimit: 1
      replicaTimeout: 300
      triggerType: 'Schedule'
    }

    template: {
      containers: [
        {
          name: 'myenergi'
          image: 'ghcr.io/stuartleeks/myenergi:latest'
          resources: {
            cpu: json('0.5')
            memory: '1Gi'
          }
          env: [
            {
              name: 'SERIAL_NUMBER'
              value: myenergiSerialNumber
            }
            {
              name: 'API_KEY'
              value: myenergiApiKey
            }
            {
              name: 'DEFAULT_START_DATE'
              value: myenergiDefaultStartDate
            }
          ]
        }
      ]
    }
  }
}

output job_name string = myernergiApp.name
