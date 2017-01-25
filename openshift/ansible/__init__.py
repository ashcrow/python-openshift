import copy
import json
import re
import string

from ansible.module_utils.basic import AnsibleModule

from kubernetes import config
from kubernetes.config.config_exception import ConfigException
from kubernetes.client.rest import ApiException
from openshift import client


class OpenShiftAnsibleModuleError(Exception):
    """
    Raised when there is an error inside of an Ansible module.
    """

    def __init__(self, message, **kwargs):
        """
        Creates an instance of the AnsibleModuleError class.
        :param message: The friendly error message.
        :type message: basestring
        :param kwargs: All other keyword arguments.
        :type kwargs: dict
        """
        self.message = message
        self.value = kwargs
        self.value['message'] = message

    def __str__(self):
        """
        String representation of the instance.
        """
        return json.dumps(self.value)


class OpenShiftAnsibleModule(AnsibleModule):
    def __init__(self, openshift_type):
        self.openshift_type = openshift_type
        self.openshift_types = self._init_types()

        if openshift_type not in self.openshift_types:
            raise OpenShiftAnsibleModuleError(
                "Unkown type {} specified.".format(openshift_type)
            )

        api_versions = [ x.lower() for x in self.openshift_types[openshift_type]['versions']]
        argument_spec = {
            'state': {'default': 'present', 'choices': ['present', 'absent']},
            'name': {'required': True},
            'kubeconfig': {},
            'context': {},
            'api_version': {'choices': api_versions, 'required': True}
        }

        for version in self.openshift_types[openshift_type]['versions']:
            #print(self.openshift_types[openshift_type][version]['model_class'])
            #print(dir(self.openshift_types[openshift_type][version]['model_class']))
            #print(vars(self.openshift_types[openshift_type][version]['model_class']))
            model_class = self.openshift_types[openshift_type][version]['model_class']
            model_obj = model_class()
            properties = self._properties_from_model(model_class)
            #print(properties)

            if 'metadata' not in properties:
                raise OpenShiftAnsibleModuleError(
                    "Object {} does not contain metadata field".format(model_class)
                )

            for p in properties:
                sub_model_class = getattr(client.models, model_obj.swagger_types[p])
                sub_props = self._properties_from_model(sub_model_class)
                sub_obj = sub_model_class()

                if p == 'status':
                    continue

#                print("\tProperty: {}".format(p))
#                print("\tType: {}".format(model_obj.swagger_types[p]))
#                for prop in sub_props:
#                    print("\t\tProperty: {}".format(prop))
#                    prop_type = sub_obj.swagger_types[prop]
#                    print("\t\tType: {} ({})".format(prop_type, type(prop_type)))
#
                if p == 'metadata':
                    if not isinstance(sub_obj, client.V1ObjectMeta):
                        raise OpenShiftAnsibleModuleError(
                            "Unknown metadata type: {}".format(sub_model_class)
                        )
                    for prop in sub_props:
                        if prop in ['labels', 'annotations']:
                            argument_spec[prop] = {'required': False, 'type': 'dict'}
                        elif prop in ['namespace']:
                            methods = self.openshift_types[openshift_type][version]['methods']
                            if 'namespaced' in methods:
                                if 'unnamespaced' in methods:
                                    required = False
                                else:
                                    required = True
                                argument_spec[prop] = {'required': required}
                else:
                    for prop in sub_props:
                        prop_type = sub_obj.swagger_types[prop]
                        if isinstance(prop_type, str) and prop_type.startswith('dict('):
                            ansible_type = 'dict'
                        elif isinstance(prop_type, str) and prop_type.startswith('list['):
                            ansible_type = 'list'
                        else:
                            ansible_type = prop_type

                        if prop in argument_spec:
                            raise OpenShiftAnsibleModuleError(
                                "param {} already present in argument_spec".format(prop)
                            )
                        argument_spec[p+'_'+prop] = {'required': False, 'type': ansible_type}

        mutually_exclusive = None
        required_together = None
        required_one_of = None
        required_if = None
        AnsibleModule.__init__(self, argument_spec, supports_check_mode=True)

    def execute_module(self):
        print(self.params)
        state = self.params.pop('state')
        api_version = self.params.pop('api_version')
        name = self.params.pop('name')
        kubeconfig = self.params.pop('kubeconfig')
        context = self.params.pop('context')
        namespace = self.params.pop('namespace', None)

        try:
            config = self._get_client_config(kubeconfig, context)
        except OpenShiftAnsibleModuleError as e:
            self.fail_json(msg='Error loading config', error=str(e))

        import yaml
        print(yaml.dump(self.openshift_types[self.openshift_type][api_version.upper()]))

        method_key = 'unnamespaced' if namespace is None else 'namespaced'
        type_info = self.openshift_types[self.openshift_type][api_version.upper()]
        api_class = type_info['methods'][method_key]['read']['api_class']
        api_obj = api_class()
        obj_get = getattr(api_obj, type_info['methods'][method_key]['read']['name'])
        existing = None
        try:
            existing = obj_get(name)
        except ApiException as e:
            if e.status != 404:
                raise

        return_attributes = {
            'changed': False,
            'api_version': api_version,
            self.openshift_type: None
        }

        if state == 'absent':
            if existing is None:
                self.exit_json(**return_attributes)
            else:
                if not self.check_mode:
                    obj_delete = getattr(api_obj, type_info['methods'][method_key]['delete']['name'])
                    obj_delete(name)
                return_attributes['changed'] = True
                self.exit_json(**return_attributes)

        # TODO: test values of provided arguments if state present
        # TODO: update object if state present and provided arguments differ

    @staticmethod
    def _get_openshift_object(config):
        pass


    @staticmethod
    def _properties_from_model(model_class):
        return [x for x in dir(model_class) if isinstance(getattr(model_class, x), property)]

    @staticmethod
    def _get_client_config(kubeconfig, context):
        try:
            # attempt to load the client config from file
            config.load_kube_config(config_file=kubeconfig, context=context)
        except IOError as e:
            # TODO: attempt to create client config from args
            raise OpenShiftAnsibleModuleError(
                "Cannot determine api endpoint, please specify kubeconfig",
                error=str(e)
            )
        except ConfigException as e:
            raise OpenShiftAnsibleModuleError(
                "Error generating client configuration",
                error=str(e)
            )
        return config

    @staticmethod
    def _init_types():
        version_pattern = re.compile("V\d((alpha|beta)\d)?")
        models = [x for x in dir(client.models) if version_pattern.match(x)]

        types = {}
        for model in models:
            match = version_pattern.match(model)
            version = match.group(0)
            name = version_pattern.sub('', model)
            if name in types:
                types[name]['versions'].append(version)
            else:
                types[name] = {'versions': [version]}

            types[name][version] = {'model_class': getattr(client, model), 'methods': {}}

        apis = [x for x in dir(client.apis) if version_pattern.search(x)]
        apis.append('OapiApi')
        for api in apis:
            match = version_pattern.search(api)
            if match is not None:
                version = match.group(0)
                name = version_pattern.sub('', api)[:-3]
            else:
                version = 'V1'
                name = api[:-3]
            api_class = getattr(client, api)

            for attr in dir(api_class):
                if attr.endswith('with_http_info'):
                    continue
                if attr.endswith('status'):
                    continue

                method_pattern = re.compile("^(create|delete_collection|delete|list|replace|patch|read)(_namespaced)?_(.*)?")
                match = method_pattern.match(attr)
                if match is None:
                    continue

                method = match.group(1)
                namespaced = match.group(2) != None
                object_name = match.group(3)

                all_namespaces = False
                if attr.endswith('_for_all_namespaces'):
                    all_namespaces = True
                    object_name = object_name[:-19]

                object_name = string.capwords(object_name, '_').replace('_','')
                object_version = version

                # TODO: find a way to better handle these
                if object_name == 'EvictionEviction':
                    object_name = 'Eviction'
                    object_version = 'V1beta1'
                elif object_name in ['ScaleScale', 'PodLog', 'NamespaceFinalize', 'DeploymentsScale',
                                     'ReplicasetsScale', 'ReplicationcontrollersScale',
                                     'LocalResourceAccessReview', 'ResourceAccessReview',
                                     'BuildRequestClone', 'BuildRequestInstantiate',
                                     'DeploymentRollbackRollback', 'DeploymentConfigRollbackRollback',
                                     'DeploymentRequestInstantiate', 'BuildLogLog', 'BindingBinding',
                                     'CertificateSigningRequestApproval', 'ScheduledJob',
                                     'DeploymentLogLog', 'SecretListSecrets', 'BuildDetails', '']:
                    continue
                if namespaced:
                    key = 'namespaced'
                elif all_namespaces:
                    key = 'all_namespaces'
                else:
                    key = 'unnamespaced'

                try:
                    if key not in types[object_name][object_version]['methods']:
                        types[object_name][object_version]['methods'][key] = {}
                except KeyError:
                    print("missing version key for object: {}, api: {}, method: {}".format(object_name, api, attr))

                method_info = {
                    'name': attr,
                    'api': api,
                    'api_class': api_class,
                }
                if method not in types[object_name][object_version]['methods'][key]:
                    types[object_name][object_version]['methods'][key][method] = method_info
        return types


