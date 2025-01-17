#!/usr/bin/env python
# (C) Copyright 2020-2021 Hewlett Packard Enterprise Development LP
#
# 
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# 
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# 
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import os
import time

from hamcrest import assert_that, is_, is_not
from utils import add_federation_block, remove_federation_block, copy_file_from_remote, send_file_to_remote, create_federation_entries, remove_entry


@step('I set federation config to "{trust_domain}" inside "{container_name}"')
def step_impl(context, trust_domain, container_name):
    endpoint_numeration = ""
    if trust_domain == context.second_trust_domain:
        endpoint_numeration = "2"
    bundle_endpoint = "spire-server%s" % endpoint_numeration    
    add_federation_block(trust_domain, bundle_endpoint, container_name)


@step('I remove federation configuration from "{container_name}"')
def step_impl(context, container_name):
    remove_federation_block(container_name)
    remove_entry(container_name)
    remove_entry(container_name, context.workload_c)


@step('I remove "{trust_domain}" federation association from "{host_name}"')
def step_impl(context, host_name, trust_domain):
    os.system("ssh root@%s \"spire-server bundle delete -id spiffe://%s -mode dissociate\"" % (host_name, trust_domain))
    time.sleep(10)


@step('Federation is activated between "{hostname1}" and "{hostname2}"')
def step_impl(context, hostname1, hostname2):
    bundle1_path, bundle2_path = "/opt/spire/server1.bundle", "/opt/spire/server2.bundle"
    os.system("ssh root@%s \"spire-server bundle show -format spiffe > %s\"" % (hostname1, bundle1_path))
    os.system("ssh root@%s \"spire-server bundle show -format spiffe > %s\"" % (hostname2, bundle2_path))
    copy_file_from_remote(hostname1, bundle1_path)
    send_file_to_remote(hostname2, bundle1_path)
    copy_file_from_remote(hostname2, bundle2_path)
    send_file_to_remote(hostname1, bundle2_path)
    os.system("ssh root@%s \"spire-server bundle set -format spiffe -id spiffe://%s -path %s\"" % (hostname1, context.second_trust_domain, bundle2_path))
    os.system("ssh root@%s \"spire-server bundle set -format spiffe -id spiffe://%s -path %s\"" % (hostname2, context.default_trust_domain, bundle1_path))
    time.sleep(5)
    remove_entry(hostname1)
    remove_entry(hostname1, context.workload_b)
    remove_entry(hostname2, context.workload_c)
    create_federation_entries(hostname1, context.default_trust_domain, context.second_trust_domain)
    create_federation_entries(hostname2, context.second_trust_domain, context.default_trust_domain, context.workload_c)
