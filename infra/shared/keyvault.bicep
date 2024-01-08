metadata description = 'Creates an Azure Key Vault.'
param name string
param location string = resourceGroup().location
param tags object = {}

@description('Service principal that should be granted read access to the Key Vault. If unset, no service principal is granted access by default')
param principalId string = ''

@description('Id of the admin security group that should be granted access to the Key Vault. If unset, no security group is granted access by default')
param adminSecurityGroupId string = ''

@description('Id of the delivery team security group that should be granted access to the Key Vault. If unset, no security group is granted access by default')
param deliveryTeamSecurityGroupId string = ''

var servicePrincipalAccessPolicies = !empty(principalId) ? [
  {
    objectId: principalId
    permissions: { secrets: [ 'get', 'list' ] }
    tenantId: subscription().tenantId
  }
] : []

var adminSecurityGroupAccessPolicies = !empty(adminSecurityGroupId) ? [
  {
    objectId: adminSecurityGroupId
    permissions: { secrets: [ 'all' ] }
    tenantId: subscription().tenantId
  }
] : []

var deliveryTeamSecurityGroupAccessPolicies = !empty(deliveryTeamSecurityGroupId) ? [
  {
    objectId: deliveryTeamSecurityGroupId
    permissions: { secrets: [ 'backup', 'delete', 'get', 'list', 'restore', 'set' ] }
    tenantId: subscription().tenantId
  }
] : []

var defaultAccessPolicies = union(servicePrincipalAccessPolicies, adminSecurityGroupAccessPolicies, deliveryTeamSecurityGroupAccessPolicies)

resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {
  name: name
  location: location
  tags: tags
  properties: {
    tenantId: subscription().tenantId
    sku: { family: 'A', name: 'standard' }
    enabledForTemplateDeployment: true
    accessPolicies: union(defaultAccessPolicies, [
      // define access policies here
    ])
  }
}

output endpoint string = keyVault.properties.vaultUri
output name string = keyVault.name
