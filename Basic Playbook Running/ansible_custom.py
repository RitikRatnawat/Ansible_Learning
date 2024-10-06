import boto3
from botocore.exceptions import ClientError
from ansible.module_utils.basic import AnsibleModule

# Function to create a Security Group with HTTP and SSH access
def create_firewall(group_name, group_protocol, group_rules):

    # Create a EC2 CLient to access EC2 Console
    ec2_client = boto3.client('ec2', region_name = "us-east-1")

    # Get the list of all VPCs registered in the Cloud
    response = ec2_client.describe_vpcs()

    # Get the VPC Id from the Response
    vpc_id = response['Vpcs'][0]['VpcId']

    try:
        # Create a Security Group on the AWS Cloud
        response = ec2_client.create_security_group(
            GroupName=group_name,
            Description="Creating Custom Firewall using Ansible Custom Module",
            VpcId=vpc_id)

        # Fetch the Created GroupId from the Response
        group_id = response['GroupId']
        
        # Create a list of rules for the Firewall
        ip_permissions = []
        for rule in group_rules:
            ip_permissions.append({
                'IpProtocol': group_protocol,
                'FromPort': rule['allow'],
                'ToPort': rule['allow'],
                'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
            })

        # Adding Inbound Rules in the Security Group
        data = ec2_client.authorize_security_group_ingress(
            GroupId=group_id,
            IpPermissions=ip_permissions)
        
        return data

    except ClientError as exp:
        raise exp


# Function for Ansible Custom Module
def configure_custom_firewall(module):

    # Retrieve Module Parameters
    firewall_name = module.params['name']
    firewall_protocol = module.params['protocol']
    firewall_rules = module.params['rules']


    try:
        results = create_firewall(firewall_name, firewall_protocol, firewall_rules)

        response = {
            'changed': True,
            'msg': results,
        }

    except Exception as exp:
        response = {
            'changed': False,
            'msg': exp
        }


    module.exit_json(**response)


def main():

    # Define the module arguments
    module_args = {
        'name': {
            'type': 'str',
            'required': True
        },
        'protocol': {
            'type': 'str',
            'required': True  
        },
        'rules': {
            'type': 'list',
            'required': True
        }
    }

    # Create the module instance
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Call the appropriate custom module function based on the module name
    if module._name == 'ansible_custom':
        configure_custom_firewall(module)
    else:
        module.fail_json(msg=f"Unsupported module: {module._name}.") 


if __name__ == '__main__':
    main()

