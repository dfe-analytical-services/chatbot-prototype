metadata description = 'Creates a container app service in an Azure Container App environment.'
param name string
param location string = resourceGroup().location
param tags object = {}

@description('Name of the environment for container apps')
param containerAppsEnvironmentName string

@description('The maximum number of replicas to run. Must be at least 1.')
@minValue(1)
param containerMaxReplicas int = 1

@description('The minimum number of replicas to run. Must be at least 1.')
param containerMinReplicas int = 1

@description('Specifies if the resource ingress is exposed externally')
param external bool = false

@description('The name of the container apps add-on to use. e.g. redis')
param serviceType string

@description('The target port for the container')
param targetPort int

resource containerAppsEnvironment 'Microsoft.App/managedEnvironments@2023-05-01' existing = {
  name: containerAppsEnvironmentName
}

resource app 'Microsoft.App/containerApps@2023-05-01' = {
  name: name
  location: location
  tags: tags
  identity: {
    type: 'None'
    userAssignedIdentities: null
  }
  properties: {
    managedEnvironmentId: containerAppsEnvironment.id
    configuration: {
      activeRevisionsMode: 'Single'
      ingress: {
        external: external
        targetPort: targetPort
        transport: 'auto'
      }
      dapr: { 
        enabled: false
      }
      service: { 
        type: serviceType
      }
    }
    template: {
      scale: {
        minReplicas: containerMinReplicas
        maxReplicas: containerMaxReplicas
      }
    }
  }
}

output name string = app.name
output serviceBind object = !empty(serviceType) ? { serviceId: app.id, name: name } : {}
