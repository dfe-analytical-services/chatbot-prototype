param name string
param location string = resourceGroup().location
param tags object = {}

@description('Name of the Log Analytics workspace')
param logAnalyticsWorkspaceName string

@description('Name of the Application Insights resource')
param applicationInsightsName string

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalyticsWorkspace.properties.customerId
        sharedKey: logAnalyticsWorkspace.listKeys().primarySharedKey
      }
    }
    daprAIConnectionString: applicationInsights.properties.ConnectionString
  }
}

resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' existing = {
  name: logAnalyticsWorkspaceName
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

output name string = containerAppsEnvironment.name
output defaultDomain string = containerAppsEnvironment.properties.defaultDomain
