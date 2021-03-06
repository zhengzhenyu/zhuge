# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""Client side of the conductor RPC API."""

from oslo_config import cfg
import oslo_messaging as messaging

from kongming.common import constants
from kongming.common import rpc
from kongming.objects import base as objects_base


CONF = cfg.CONF


class ConductorAPI(object):
    """Client side of the conductor RPC API.

    API version history:

    |    1.0 - Initial version.

    """

    RPC_API_VERSION = '1.0'

    def __init__(self, topic=None):
        super(ConductorAPI, self).__init__()
        self.topic = topic or constants.CONDUCTOR_TOPIC
        target = messaging.Target(topic=self.topic,
                                  version='1.0')
        serializer = objects_base.KongmingObjectSerializer()
        self.client = rpc.get_client(target,
                                     version_cap=self.RPC_API_VERSION,
                                     serializer=serializer)

    def create_instance_cpu_mapping(self, context, mapping_obj):
        cctxt = self.client.prepare(topic=self.topic)
        return cctxt.cast(context, 'update_instance_cpu_mapping',
                          mapping_obj=mapping_obj)

    def update_instance_cpu_mapping(self, context, mapping_obj):
        cctxt = self.client.prepare(topic=self.topic)
        return cctxt.cast(context, 'update_instance_cpu_mapping',
                          mapping_obj=mapping_obj)

    def check_and_update_instance_cpu_mapping(self, context,
                                              instance_uuid,
                                              instance_host):
        cctxt = self.client.prepare(topic=self.topic)
        return cctxt.cast(context, 'check_and_update_instance_cpu_mapping',
                          instance_uuid=instance_uuid,
                          instance_host=instance_host)

    def check_and_update_host_resources(self, context, host):
        cctxt = self.client.prepare(topic=self.topic)
        return cctxt.call(context, 'check_and_update_host_resources', host=host)

    def check_and_update_instances(self, context, host, instance_list):
        cctxt = self.client.prepare(topic=self.topic)
        return cctxt.call(context, 'check_and_update_instances',
                          host=host, instances=instance_list)
