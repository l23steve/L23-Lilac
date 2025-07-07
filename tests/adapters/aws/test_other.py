import pytest

from lilac.adapters.aws import cloudwatch, ec2, ecr, ecs, route53

class FakePaginator:
    def __init__(self, pages):
        self.pages = pages
    def paginate(self, **kwargs):
        return self.pages

class FakeEcrClient:
    def __init__(self, repos=None, fail=False):
        self.repos = repos or []
        self.fail = fail
    def get_paginator(self, name):
        if self.fail:
            raise Exception("fail")
        return FakePaginator([{"repositories": self.repos}])


def test_list_repositories(monkeypatch):
    fake = FakeEcrClient(
        repos=[{"repositoryName": "r", "repositoryArn": "a", "repositoryUri": "u"}]
    )
    monkeypatch.setattr(ecr.boto3, "client", lambda service: fake)
    repos = ecr.list_repositories()
    assert repos[0]["name"] == "r"
    assert repos[0]["uri"] == "u"
    assert "details" in repos[0]


def test_list_repositories_error(monkeypatch):
    fake = FakeEcrClient(fail=True)
    monkeypatch.setattr(ecr.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ecr.list_repositories()

class FakeEcsClient:
    def __init__(
        self,
        services=None,
        tasks=None,
        service_details=None,
        task_details=None,
        fail=False,
    ):
        self.services = services or []
        self.tasks = tasks or []
        self.service_details = service_details or []
        self.task_details = task_details or []
        self.fail = fail
    def list_clusters(self):
        if self.fail:
            raise Exception("fail")
        return {"clusterArns": ["c"]}
    def list_services(self, cluster):
        if self.fail:
            raise Exception("fail")
        return {"serviceArns": self.services}

    def list_tasks(self, cluster):
        if self.fail:
            raise Exception("fail")
        return {"taskArns": self.tasks}

    def describe_services(self, cluster, services):
        if self.fail:
            raise Exception("fail")
        return {"services": self.service_details}

    def describe_tasks(self, cluster, tasks):
        if self.fail:
            raise Exception("fail")
        return {"tasks": self.task_details}


def test_list_services(monkeypatch):
    fake = FakeEcsClient(
        services=["s"],
        service_details=[{"serviceArn": "s", "desiredCount": 1}],
    )
    monkeypatch.setattr(ecs.boto3, "client", lambda service: fake)
    services = ecs.list_services()
    assert services[0]["serviceArn"] == "s"
    assert services[0]["details"]["desiredCount"] == 1


def test_list_tasks(monkeypatch):
    fake = FakeEcsClient(
        tasks=["t"],
        task_details=[{"taskArn": "t", "lastStatus": "RUNNING"}],
    )
    monkeypatch.setattr(ecs.boto3, "client", lambda service: fake)
    tasks = ecs.list_tasks()
    assert tasks[0]["taskArn"] == "t"
    assert tasks[0]["details"]["lastStatus"] == "RUNNING"


def test_list_services_error(monkeypatch):
    fake = FakeEcsClient(fail=True)
    monkeypatch.setattr(ecs.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ecs.list_services()


def test_list_tasks_error(monkeypatch):
    fake = FakeEcsClient(fail=True)
    monkeypatch.setattr(ecs.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ecs.list_tasks()

class FakeEc2Client:
    def __init__(self, fail=False):
        self.fail = fail
    def describe_instances(self):
        if self.fail:
            raise Exception("fail")
        return {
            "Reservations": [
                {
                    "Instances": [
                        {
                            "InstanceId": "i",
                            "InstanceType": "t",
                            "State": {"Name": "running"},
                        }
                    ]
                }
            ]
        }
    def describe_security_groups(self):
        if self.fail:
            raise Exception("fail")
        return {
            "SecurityGroups": [
                {
                    "GroupId": "gid",
                    "GroupName": "name",
                    "Description": "desc",
                }
            ]
        }
    def describe_network_interfaces(self):
        if self.fail:
            raise Exception("fail")
        return {
            "NetworkInterfaces": [
                {"NetworkInterfaceId": "nid", "SubnetId": "subnet"}
            ]
        }
    def describe_vpcs(self):
        if self.fail:
            raise Exception("fail")
        return {"Vpcs": [{"VpcId": "vpc", "CidrBlock": "10.0.0.0/16"}]}


def test_list_instances(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    instances = ec2.list_instances()
    assert instances[0]["id"] == "i"
    assert instances[0]["state"] == "running"
    assert "details" in instances[0]


def test_list_instances_error(monkeypatch):
    fake = FakeEc2Client(fail=True)
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ec2.list_instances()


def test_list_security_groups(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    groups = ec2.list_security_groups()
    assert groups[0]["name"] == "name"
    assert groups[0]["description"] == "desc"
    assert "details" in groups[0]


def test_list_network_interfaces(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    nis = ec2.list_network_interfaces()
    assert nis[0]["id"] == "nid"
    assert nis[0]["subnet_id"] == "subnet"
    assert "details" in nis[0]


def test_list_vpcs(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    vpcs = ec2.list_vpcs()
    assert vpcs[0]["id"] == "vpc"
    assert vpcs[0]["cidr_block"] == "10.0.0.0/16"
    assert "details" in vpcs[0]


def test_list_security_groups_error(monkeypatch):
    fake = FakeEc2Client(fail=True)
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ec2.list_security_groups()


def test_list_network_interfaces_error(monkeypatch):
    fake = FakeEc2Client(fail=True)
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ec2.list_network_interfaces()


def test_list_vpcs_error(monkeypatch):
    fake = FakeEc2Client(fail=True)
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ec2.list_vpcs()

class FakeRoute53Client:
    def __init__(self, fail=False):
        self.fail = fail
    def list_hosted_zones(self):
        if self.fail:
            raise Exception("fail")
        return {
            "HostedZones": [
                {
                    "Id": "Z1",
                    "Name": "example.com",
                    "ResourceRecordSetCount": 3,
                }
            ]
        }


def test_list_zones(monkeypatch):
    fake = FakeRoute53Client()
    monkeypatch.setattr(route53.boto3, "client", lambda service: fake)
    zones = route53.list_zones()
    assert zones[0]["id"] == "Z1"
    assert zones[0]["record_set_count"] == 3
    assert "details" in zones[0]


def test_list_zones_error(monkeypatch):
    fake = FakeRoute53Client(fail=True)
    monkeypatch.setattr(route53.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        route53.list_zones()

class FakeLogsClient:
    def __init__(self, fail=False):
        self.fail = fail
    def describe_log_groups(self):
        if self.fail:
            raise Exception("fail")
        return {
            "logGroups": [
                {"logGroupName": "g", "arn": "arn", "retentionInDays": 7}
            ]
        }


def test_list_log_groups(monkeypatch):
    fake = FakeLogsClient()
    monkeypatch.setattr(cloudwatch.boto3, "client", lambda service: fake)
    groups = cloudwatch.list_log_groups()
    assert groups[0]["name"] == "g"
    assert groups[0]["arn"] == "arn"
    assert groups[0]["retention"] == 7
    assert "details" in groups[0]


def test_list_log_groups_error(monkeypatch):
    fake = FakeLogsClient(fail=True)
    monkeypatch.setattr(cloudwatch.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        cloudwatch.list_log_groups()
