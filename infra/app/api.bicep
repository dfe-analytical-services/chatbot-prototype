param name string
param location string = resourceGroup().location
param tags object = {}

param identityName string

param deployRoleAssignments bool = true

resource apiIdentity 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: identityName
  location: location
  tags: tags
}

module containerRegistryAccess '../shared/container-registry-access.bicep' = if (deployRoleAssignments) {
  name: '${name}-container-registry-access'
  params: {
    principalId: apiIdentity.properties.principalId
  }
}
