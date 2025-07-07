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
    fake = FakeEcrClient(repos=[{"repositoryName": "r", "repositoryArn": "a"}])
    monkeypatch.setattr(ecr.boto3, "client", lambda service: fake)
    repos = ecr.list_repositories()
    assert repos == [{"name": "r", "arn": "a"}]


def test_list_repositories_error(monkeypatch):
    fake = FakeEcrClient(fail=True)
    monkeypatch.setattr(ecr.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ecr.list_repositories()

class FakeEcsClient:
    def __init__(self, services=None, tasks=None, fail=False):
        self.services = services or []
        self.tasks = tasks or []
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


def test_list_services(monkeypatch):
    fake = FakeEcsClient(services=["s"])
    monkeypatch.setattr(ecs.boto3, "client", lambda service: fake)
    services = ecs.list_services()
    assert services == [{"serviceArn": "s", "clusterArn": "c"}]


def test_list_tasks(monkeypatch):
    fake = FakeEcsClient(tasks=["t"])
    monkeypatch.setattr(ecs.boto3, "client", lambda service: fake)
    tasks = ecs.list_tasks()
    assert tasks == [{"taskArn": "t", "clusterArn": "c"}]


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
                {"Instances": [{"InstanceId": "i", "InstanceType": "t"}]}
            ]
        }
    def describe_security_groups(self):
        if self.fail:
            raise Exception("fail")
        return {"SecurityGroups": [{"GroupId": "gid", "GroupName": "name"}]}
    def describe_network_interfaces(self):
        if self.fail:
            raise Exception("fail")
        return {"NetworkInterfaces": [{"NetworkInterfaceId": "nid"}]}
    def describe_vpcs(self):
        if self.fail:
            raise Exception("fail")
        return {"Vpcs": [{"VpcId": "vpc"}]}


def test_list_instances(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    instances = ec2.list_instances()
    assert instances == [{"id": "i", "type": "t"}]


def test_list_instances_error(monkeypatch):
    fake = FakeEc2Client(fail=True)
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        ec2.list_instances()


def test_list_security_groups(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    groups = ec2.list_security_groups()
    assert groups == [{"id": "gid", "name": "name"}]


def test_list_network_interfaces(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    nis = ec2.list_network_interfaces()
    assert nis == [{"id": "nid"}]


def test_list_vpcs(monkeypatch):
    fake = FakeEc2Client()
    monkeypatch.setattr(ec2.boto3, "client", lambda service: fake)
    vpcs = ec2.list_vpcs()
    assert vpcs == [{"id": "vpc"}]


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
        return {"HostedZones": [{"Id": "Z1", "Name": "example.com"}]}


def test_list_zones(monkeypatch):
    fake = FakeRoute53Client()
    monkeypatch.setattr(route53.boto3, "client", lambda service: fake)
    zones = route53.list_zones()
    assert zones == [{"id": "Z1", "name": "example.com"}]


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
        return {"logGroups": [{"logGroupName": "g"}]}


def test_list_log_groups(monkeypatch):
    fake = FakeLogsClient()
    monkeypatch.setattr(cloudwatch.boto3, "client", lambda service: fake)
    groups = cloudwatch.list_log_groups()
    assert groups == [{"name": "g"}]


def test_list_log_groups_error(monkeypatch):
    fake = FakeLogsClient(fail=True)
    monkeypatch.setattr(cloudwatch.boto3, "client", lambda service: fake)
    with pytest.raises(Exception):
        cloudwatch.list_log_groups()
