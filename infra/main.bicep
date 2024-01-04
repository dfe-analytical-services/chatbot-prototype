targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the environment that can be used as part of naming resource convention')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

@description('Id of the user or app to assign application roles')
param principalId string

@minLength(1)
@maxLength(64)
@description('Name of the product to be used a value for the Product tag')
param productName string

@minLength(1)
@maxLength(64)
@description('Name of the resource group')
param resourceGroupName string

@description('Specify if role assignments should be deployed')
param deployRoleAssignments bool = true

param apiAppExists bool = false
param webAppExists bool = false
@secure()
param apiAppDefinition object
@secure()
param webAppDefinition object

// Tags that should be applied to all resources.
// 
// Note that 'azd-service-name' tags should be applied separately to service host resources.
// Example usage:
//   tags: union(tags, { 'azd-service-name': <service name in azure.yaml> })
var tags = {
  'azd-env-name': environmentName
  Product: productName
}

var webContainerAppNameOrDefault = '${resourceGroupName}-${abbrs.appContainerApps}web'
var corsAcaUrl = 'https://${webContainerAppNameOrDefault}.${containerAppsEnv.outputs.defaultDomain}'

var abbrs = loadJsonContent('./abbreviations.json')

// Organize resources in a resource group
resource rg 'Microsoft.Resources/resourceGroups@2023-07-01' = {
  name: resourceGroupName
  location: location
  tags: tags
}

// Store secrets in a keyvault
module keyVault './shared/keyvault.bicep' = {
  name: 'key-vault'
  params: {
    location: location
    tags: tags
    name: '${resourceGroupName}-${abbrs.keyVaultVaults}01'
    principalId: principalId
  }
  scope: rg
}

// Container registry
module containerRegistry './shared/container-registry.bicep' = {
  name: 'container-registry'
  params: {
    location: location
    tags: tags
    name: '${replace(resourceGroupName,'-','')}${abbrs.containerRegistryRegistries}01'
  }
  scope: rg
}

// Monitor application with Azure Monitor
module monitoring './shared/monitoring.bicep' = {
  name: 'monitoring'
  params: {
    location: location
    tags: tags
    logAnalyticsName: '${resourceGroupName}-${abbrs.operationalInsightsWorkspaces}01'
    applicationInsightsName: '${resourceGroupName}-${abbrs.insightsComponents}01'
  }
  scope: rg
}

// Container apps host
module containerAppsEnv './shared/container-apps-environment.bicep' = {
  name: 'container-apps-environment'
  params: {
    name: '${resourceGroupName}-${abbrs.appManagedEnvironments}01'
    location: location
    tags: tags
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
  scope: rg
}

// Qdrant database service
module db './shared/container-app-service.bicep' = {
  name: 'db'
  params: {
    name: '${resourceGroupName}-${abbrs.appContainerApps}db'
    location: location
    tags: tags
    containerAppsEnvironmentName: containerAppsEnv.outputs.name
    serviceType: 'qdrant'
    targetPort: 6333
    containerMinReplicas: 1
    containerMaxReplicas: 1
  }
  scope: rg
}

// Api container app
module api './app/api.bicep' = {
  name: 'api'
  params: {
    name: '${resourceGroupName}-${abbrs.appContainerApps}api'
    location: location
    tags: tags
    identityName: '${resourceGroupName}-${abbrs.managedIdentityUserAssignedIdentities}api'
    deployRoleAssignments: deployRoleAssignments
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    dbServiceName: db.outputs.name
    containerAppsEnvironmentName: containerAppsEnv.outputs.name
    containerRegistryName: containerRegistry.outputs.name
    keyVaultName: keyVault.outputs.name
    corsAcaUrl: corsAcaUrl
    exists: apiAppExists
    appDefinition: apiAppDefinition
  }
  scope: rg
}

// Web container app
module web './app/web.bicep' = {
  name: 'web'
  params: {
    name: '${resourceGroupName}-${abbrs.appContainerApps}web'
    location: location
    tags: tags
    identityName: '${resourceGroupName}-${abbrs.managedIdentityUserAssignedIdentities}web'
    deployRoleAssignments: deployRoleAssignments
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    containerAppsEnvironmentName: containerAppsEnv.outputs.name
    containerRegistryName: containerRegistry.outputs.name
    exists: webAppExists
    appDefinition: webAppDefinition
    apiBaseUrl: api.outputs.uri
  }
  scope: rg
}

output AZURE_KEY_VAULT_NAME string = keyVault.outputs.name
output AZURE_KEY_VAULT_ENDPOINT string = keyVault.outputs.endpoint
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerRegistry.outputs.loginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerRegistry.outputs.name
