metadata description = 'Creates or updates an existing Azure Container App.'
param name string
param location string = resourceGroup().location
param tags object = {}

@description('Allowed origins')
param allowedOrigins array = []

@description('Name of the environment for container apps')
param containerAppsEnvironmentName string

@description('CPU cores allocated to a single container instance, e.g., 0.5')
param containerCpuCoreCount string = '0.5'

@description('The maximum number of replicas to run. Must be at least 1.')
@minValue(1)
param containerMaxReplicas int = 10

@description('Memory allocated to a single container instance, e.g., 1Gi')
param containerMemory string = '1.0Gi'

@description('The minimum number of replicas to run. Must be at least 1.')
param containerMinReplicas int = 1

@description('The name of the container')
param containerName string = 'main'

@description('The name of the container registry')
param containerRegistryName string = ''

@description('The protocol used by Dapr to connect to the app, e.g., http or grpc')
@allowed([ 'http', 'grpc' ])
param daprAppProtocol string = 'http'

@description('The Dapr app ID')
param daprAppId string = containerName

@description('Enable Dapr')
param daprEnabled bool = false

@description('The environment variables for the container')
param env array = []

@description('Specifies if the resource ingress is exposed externally')
param external bool = true

@description('The name of the user-assigned identity')
param identityName string = ''

@description('The name of the container image')
param imageName string = ''

@description('Specifies if the resource already exists')
param exists bool = false

@description('Specifies if Ingress is enabled for the container app')
param ingressEnabled bool = true

param revisionMode string = 'Single'

@description('The secrets required for the container')
param secrets array = []

@description('The service binds associated with the container')
param serviceBinds array = []

@description('The name of the container apps add-on to use. e.g. redis')
param serviceType string = ''

@description('The target port for the container')
param targetPort int = 80

resource existingApp 'Microsoft.App/containerApps@2024-03-01' existing = if (exists) {
  name: name
}

module app 'container-app.bicep' = {
  name: '${deployment().name}-update'
  params: {
    name: name
    location: location
    tags: tags
    allowedOrigins: allowedOrigins
    containerAppsEnvironmentName: containerAppsEnvironmentName
    containerCpuCoreCount: containerCpuCoreCount
    containerMaxReplicas: containerMaxReplicas
    containerMemory: containerMemory
    containerMinReplicas: containerMinReplicas
    containerName: containerName
    containerRegistryName: containerRegistryName
    daprAppProtocol: daprAppProtocol
    daprAppId: daprAppId
    daprEnabled: daprEnabled
    env: env
    external: external
    identityName: identityName
    imageName: !empty(imageName) ? imageName : exists ? existingApp.properties.template.containers[0].image : ''
    ingressEnabled: ingressEnabled
    revisionMode: revisionMode
    secrets: secrets
    serviceBinds: serviceBinds
    serviceType: serviceType
    targetPort: targetPort
  }
}

output defaultDomain string = app.outputs.defaultDomain
output imageName string = app.outputs.imageName
output name string = app.outputs.name
output serviceBind object = app.outputs.serviceBind
output uri string = app.outputs.uri
