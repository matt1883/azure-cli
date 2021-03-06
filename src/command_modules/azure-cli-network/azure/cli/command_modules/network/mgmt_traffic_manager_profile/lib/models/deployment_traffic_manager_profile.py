#---------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#---------------------------------------------------------------------------------------------
#pylint: skip-file

# coding=utf-8
# --------------------------------------------------------------------------
# Code generated by Microsoft (R) AutoRest Code Generator 0.17.0.0
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DeploymentTrafficManagerProfile(Model):
    """
    Deployment operation parameters.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar uri: URI referencing the template. Default value:
     "https://azuresdkci.blob.core.windows.net/templatehost/CreateTrafficManagerProfile_2016-08-08/azuredeploy.json"
     .
    :vartype uri: str
    :param content_version: If included it must match the ContentVersion in
     the template.
    :type content_version: str
    :param location: Location for traffic manager or 'global'. Default value:
     "global" .
    :type location: str
    :param monitor_path: Path to monitor. Default value: "/" .
    :type monitor_path: str
    :param monitor_port: Port to monitor. Default value: 80 .
    :type monitor_port: int
    :param monitor_protocol: Monitor protocol. Possible values include:
     'http', 'https'. Default value: "http" .
    :type monitor_protocol: str or :class:`monitorProtocol
     <trafficmanagerprofilecreationclient.models.monitorProtocol>`
    :param routing_method: Routing method. Possible values include:
     'priority', 'performance', 'weighted'
    :type routing_method: str or :class:`routingMethod
     <trafficmanagerprofilecreationclient.models.routingMethod>`
    :param status: Create an enabled or disabled profile. Possible values
     include: 'enabled', 'disabled'. Default value: "enabled" .
    :type status: str or :class:`status
     <trafficmanagerprofilecreationclient.models.status>`
    :param traffic_manager_profile_name: Name of resource.
    :type traffic_manager_profile_name: str
    :param ttl: DNS Config time-to-live in seconds. Default value: 30 .
    :type ttl: int
    :param unique_dns_name: Relative DNS name for the traffic manager
     profile, resulting FQDN will be <uniqueDnsName>.trafficmanager.net, must
     be globally unique.
    :type unique_dns_name: str
    :ivar mode: Gets or sets the deployment mode. Default value:
     "Incremental" .
    :vartype mode: str
    """ 

    _validation = {
        'uri': {'required': True, 'constant': True},
        'routing_method': {'required': True},
        'traffic_manager_profile_name': {'required': True},
        'unique_dns_name': {'required': True},
        'mode': {'required': True, 'constant': True},
    }

    _attribute_map = {
        'uri': {'key': 'properties.templateLink.uri', 'type': 'str'},
        'content_version': {'key': 'properties.templateLink.contentVersion', 'type': 'str'},
        'location': {'key': 'properties.parameters.location.value', 'type': 'str'},
        'monitor_path': {'key': 'properties.parameters.monitorPath.value', 'type': 'str'},
        'monitor_port': {'key': 'properties.parameters.monitorPort.value', 'type': 'int'},
        'monitor_protocol': {'key': 'properties.parameters.monitorProtocol.value', 'type': 'monitorProtocol'},
        'routing_method': {'key': 'properties.parameters.routingMethod.value', 'type': 'routingMethod'},
        'status': {'key': 'properties.parameters.status.value', 'type': 'status'},
        'traffic_manager_profile_name': {'key': 'properties.parameters.trafficManagerProfileName.value', 'type': 'str'},
        'ttl': {'key': 'properties.parameters.ttl.value', 'type': 'int'},
        'unique_dns_name': {'key': 'properties.parameters.uniqueDnsName.value', 'type': 'str'},
        'mode': {'key': 'properties.mode', 'type': 'str'},
    }

    uri = "https://azuresdkci.blob.core.windows.net/templatehost/CreateTrafficManagerProfile_2016-08-08/azuredeploy.json"

    mode = "Incremental"

    def __init__(self, routing_method, traffic_manager_profile_name, unique_dns_name, content_version=None, location="global", monitor_path="/", monitor_port=80, monitor_protocol="http", status="enabled", ttl=30):
        self.content_version = content_version
        self.location = location
        self.monitor_path = monitor_path
        self.monitor_port = monitor_port
        self.monitor_protocol = monitor_protocol
        self.routing_method = routing_method
        self.status = status
        self.traffic_manager_profile_name = traffic_manager_profile_name
        self.ttl = ttl
        self.unique_dns_name = unique_dns_name
