param name string
param location string = resourceGroup().location
param tags object = {}

param identityName string
param deployRoleAssignments bool = true
param containerRegistryName string
param keyVaultName string
param serviceName string = 'web'
param containerAppsEnvironmentName string
param applicationInsightsName string
param exists bool
@secure()
param appDefinition object

var appSettingsArray = filter(array(appDefinition.settings), i => i.name != '')
var secrets = map(filter(appSettingsArray, i => i.?secret != null), i => {
  name: i.name
  value: i.value
  secretRef: i.?secretRef ?? take(replace(replace(toLower(i.name), '_', '-'), '.', '-'), 32)
})
var env = map(filter(appSettingsArray, i => i.?secret == null), i => {
  name: i.name
  value: i.value
})

resource webIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
  tags: tags
}

resource applicationInsights 'Microsoft.Insights/components@2020-02-02' existing = {
  name: applicationInsightsName
}

resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

// Assign access to the ACR
module containerRegistryAccess '../shared/container-registry-access.bicep' = if (deployRoleAssignments) {
  name: '${name}-container-registry-access'
  params: {
    principalId: webIdentity.properties.principalId
  }
}

// Assign access to the key vault
module webKeyVaultAccess '../shared/keyvault-access.bicep' = {
  name: '${name}-keyvault-access'
  params: {
    keyVaultName: keyVaultName
    principalId: webIdentity.properties.principalId
  }
}

module app '../shared/container-app.bicep' = {
  name: '${serviceName}-container-app'
  dependsOn: deployRoleAssignments ? [ containerRegistryAccess, webKeyVaultAccess ] : [ webKeyVaultAccess ]
  params: {
    name: name
    location: location
    tags: union(tags, { 'azd-service-name': serviceName })
    identityName: webIdentity.name
    exists: exists
    containerAppsEnvironmentName: containerAppsEnvironmentName
    containerRegistryName: containerRegistryName
    containerCpuCoreCount: '1.0'
    containerMemory: '2.0Gi'
    containerMinReplicas: 1
    containerMaxReplicas: 10
    env: union([
      {
        name: 'AZURE_CLIENT_ID'
        value: webIdentity.properties.clientId
      }
      {
        name: 'AZURE_KEY_VAULT_ENDPOINT'
        value: keyVault.properties.vaultUri
      }
      {
        name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
        value: applicationInsights.properties.ConnectionString
      }
    ],
    env,
    map(secrets, secret => {
      name: secret.name
      secretRef: secret.secretRef
    }))
    secrets: union([
    ],
    map(secrets, secret => {
      name: secret.name
      secretRef: secret.secretRef
    }))
    targetPort: 3000
  }
}

output name string = app.name
output uri string = app.outputs.uri
