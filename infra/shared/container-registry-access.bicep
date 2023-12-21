metadata description = 'Assigns ACR Pull role to access an Azure Container Registry.'

param principalId string

var acrPullRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')

// This requires Microsoft.Authorization/roleAssignments/write permission,
// such as being an Owner, User Access Administrator, or RBAC Administrator at the scope the role is being assigned.
resource acrPullRoleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: resourceGroup() // Scope is specified as the resource group level but this could be changed to be a specific ACR resource
  name: guid(resourceGroup().id, principalId, acrPullRole)
  properties: {
    roleDefinitionId: acrPullRole
    principalType: 'ServicePrincipal'
    principalId: principalId
  }
}
