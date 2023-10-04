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

resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: 'homeenergistorage'
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
  properties: {
    accessTier: 'Hot'
  }
}
resource files 'Microsoft.Storage/storageAccounts/fileServices@2022-09-01' = {
  parent: storageAccount
  name: 'default'
  properties: {}
}
resource share 'Microsoft.Storage/storageAccounts/fileServices/shares@2022-09-01' = {
  parent: files
  name: 'homeenergishare'
  properties: {
    enabledProtocols: 'SMB'
    shareQuota: 1
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
  resource storage 'storages@2023-04-01-preview' = {
    name: 'homeenergistorage'
    properties: {
      azureFile: {
        shareName: share.name
        accountName: storageAccount.name
        accountKey: storageAccount.listKeys().keys[0].value
        accessMode: 'ReadWrite'
      }
    }
  }
}

resource myernergiApp 'Microsoft.App/jobs@2023-05-01' = {
  // resource myernergiApp 'Microsoft.App/jobs@2023-05-02-preview' = {
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
      volumes: [
        {
          name: 'homeenergistorage-volume'
          storageName: 'homeenergistorage'
          storageType: 'AzureFile'
          mountOptions: 'uid=1000,gid=1000,nobrl,mfsymlinks,cache=none'
        }
      ]
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
            {
              name: 'DATABASE_PATH'
              value: '/var/local/homeenergistorage/home_energy.db'
            }
          ]
          volumeMounts: [
            {
              volumeName: 'homeenergistorage-volume'
              mountPath: '/var/local/homeenergistorage/'
            }
          ]
        }
      ]
    }
  }
}

output job_name string = myernergiApp.name
