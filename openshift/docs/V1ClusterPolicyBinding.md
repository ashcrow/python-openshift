# V1ClusterPolicyBinding

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**last_modified** | [**UnversionedTime**](UnversionedTime.md) | LastModified is the last time that any part of the ClusterPolicyBinding was created, updated, or deleted | 
**metadata** | [**V1ObjectMeta**](V1ObjectMeta.md) | Standard object&#39;s metadata. | [optional] 
**policy_ref** | [**V1ObjectReference**](V1ObjectReference.md) | PolicyRef is a reference to the ClusterPolicy that contains all the ClusterRoles that this ClusterPolicyBinding&#39;s RoleBindings may reference | 
**role_bindings** | [**list[V1NamedClusterRoleBinding]**](V1NamedClusterRoleBinding.md) | RoleBindings holds all the ClusterRoleBindings held by this ClusterPolicyBinding, mapped by ClusterRoleBinding.Name | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


