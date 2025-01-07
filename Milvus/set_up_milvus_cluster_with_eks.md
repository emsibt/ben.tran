<h1>Set up Milvus cluster with AWS EKS</h1>

> This documentaion releases with purpose to help quickly setup the Milvus Cluster in EKS Cluster

<h2>Table of contents</h2>

- [Prerequisites](#prerequisites)
- [Setup S3 Bucket for Milvus's Object Storage](#setup-s3-bucket-for-milvuss-object-storage)
- [Setup an Amazon EKS Cluster](#setup-an-amazon-eks-cluster)
- [Setup an storage class](#setup-an-storage-class)
- [Setup AWS LoadBalancer Controller](#setup-aws-loadbalancer-controller)
- [Setup Milvus DB](#setup-milvus-db)
- [Setup ACM Domain in Route53 for MilvusDB](#setup-acm-domain-in-route53-for-milvusdb)
- [Milvus Credentials](#milvus-credentials)
- [Apply Cluster AutoScaling (CA) for Milvus](#apply-cluster-autoscaling-ca-for-milvus)
  - [Apply new spec ASG](#apply-new-spec-asg)
  - [Create IAM Policy for Cluster Autoscaler](#create-iam-policy-for-cluster-autoscaler)
  - [Deploy cluster-autoscaler deployment](#deploy-cluster-autoscaler-deployment)
- [Setup Metrics Server for Milvus Cluster](#setup-metrics-server-for-milvus-cluster)
- [Conclusion](#conclusion)
  - [Complete](#complete)
  - [TODO](#todo)


This document base on the official documentation from Milvus to setup EKS at article [Deploy a Milvus Cluster on EKS](https://milvus.io/docs/eks.md). Please double check about the latest version as you work

Following the documentation, you need to prepare some tools inside your machine to compatible provision Milvus Cluster

![alt text](../assets/images/architecture_milvus_service_with_EKS.drawio.png)

## Prerequisites

The tools needs for provisioning cluster, including

- [`aws-cli`](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) : `>= 2.17.59`
- [`kubectl`](https://kubernetes.io/docs/tasks/tools/) : `>= v1.29.0`
- [`helm`](https://helm.sh/docs/intro/install/) : `>= v3.16.2`
- [`eksctl`](https://eksctl.io/installation/) : `0.194.0`

Next, you need to prepare IAM permission to finish provision your EKS cluster and you can choose highest permission `AdministratorAccess`.

## Setup S3 Bucket for Milvus's Object Storage

> NOTE: This bucket will be provisioned by IaC as Terraform. Recommend to keep this bucket safe to protect data inside Milvus Cluster.

Checking the Bucket configuration in [milvus_eks_service.tf](./terraform/milvus_eks_service.tf#L1)

## Setup an Amazon EKS Cluster

You need to prepare `eks_cluster.yaml` inside your project to provide information into `eksctl` in provision progressing, you can find this file at
[eks_cluster.yml](./terraform/Milvus/eks_cluster.yaml)

After you read and understand configuration, you can apply with `eksctl` command

```bash
eksctl create cluster -f eks_cluster.yaml
```

>NOTE: This provision progress will run during 10 - 15 Mins with AWS Cloudformation to provision for you EKS, EC2, IAM Network and Pluggin inside EKS Cluster including Networking and Storage

After successful provisioning, you can get the `kubeconfig` to use it with `kubectl` by using command `aws eks`

```bash
aws eks update-kubeconfig --region 'ap-southeast-1' --name <name-of-cluster>
```

Now, you are in cluster and have permission depend on what IAM and role which permit inside the EKS cluster. If not you can try to read about issue [Grant IAM users access to Kubernetes with EKS access entries](https://docs.aws.amazon.com/eks/latest/userguide/access-entries.html)

```bash
kubetcl get nodes
```

> **Warnings**
> You need to handle add tags into public and private subnet with vpc used in EKS Cluster, because it's will help you create load balancer with 0 issues

You can double-check it in portal if VPC in Subnet Tab. If it doesn't automatically add new tags, you can add inside the terraform file which defind the public and private subnet.
```bash
# e.g
...
...
  private_subnet_tags = {
    "kubernetes.io/cluster/milvus-cluster"          = "shared",
    "kubernetes.io/cluster/sup-por-dev-k8s-cluster" = "shared",
    "kubernetes.io/cluster/milvus-cluster-v2"       = "shared",
    "kubernetes.io/role/internal-elb"               = "1"
  }
  public_subnet_tags = {
    "kubernetes.io/cluster/milvus-cluster"          = "shared",
    "kubernetes.io/cluster/sup-por-dev-k8s-cluster" = "shared",
    "kubernetes.io/cluster/milvus-cluster-v2"       = "shared",
    "kubernetes.io/role/elb"                        = "1"
  }
```

## Setup an storage class

Because Milvus cluster use `etcd` for metadata storage and need to reply on the `gp3` StorageClass to create and manage PVC

All manifest is written and kept inside [milvus_storageclass.yaml](./terraform/Milvus/milvus_storageclass.yaml)

If you find and understand this file, you can use `kubectl` to apply this manifest into EKS Cluster

```bash
kubetcl apply -f milvus_storageclass.yaml
```

After adding into cluster, you can use `kubetcl` to double-check

```bash
kubetcl get storageclasses
```

With current cluster, `gp2` is default storageclasses so you need use `kubectl patch` command to change `gp2` into `gp3`

```bash
kubetcl patch storageclass gp2 -p '{"metadata": {"annotations":{"storageclass.kubernetes.io/is-default-class":"false"}}}'
```

## Setup AWS LoadBalancer Controller

To compatible and ease to integrate with EKS Cluster, AWS LoadBalancer is first one of choice

AWS LoadBalancer is written and distributed by Helm Chart. So, you need to use helm to install its into cluster

```bash
helm repo add eks https://aws.github.io/eks-charts
helm repo update
```

After add and update repo for helm chart `aws-load-balancer-controller`, you can install into EKS Cluster

```bash
helm install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system\
  --set clusterName='milvus-cluster' \
  --set serviceAccount.create=false \
  --set serviceAccount.name=aws-load-balancer-controller
```

Wait a bit and you can verify the installation

```bash
kubectl get deployment -n kube-system aws-load-balancer-controller
```

## Setup Milvus DB

Same as AWS LoadBalancer, Milvus is written and managed by Helm Chart, you can follow helm workflow to add and install helm chart from repository

But first of all, with MIlvusDB, you need to make a lot of configuration for changing cluster work same as your expectation. Thoes configurations write in some file, including

- [milvus_attu.yaml](./terraform/Milvus/milvus_attu.yaml): Enable Attu and Ingress for Attu service
- [milvus_cluster.yaml](./terraform/Milvus/milvus_cluster.yaml): Set configuration for MilvusDB, include `externalS3`, `kafka`, enable `cluster` mode and authentiate to connect MilvusDB
- [milvus_service.yaml](./terraform/Milvus/milvus_service.yaml): Enable LoadBalancer Service for MilvusDB to map TCP port into AWS LB to help remote connect

When you already double check about all configuration. you can use `helm` command to add and install chart

- Use Helm chart: `milvus-4.2.19`
- Milvus Cluster: `2.4.15`

```bash
helm repo add milvus https://zilliztech.github.io/milvus-helm/
helm repo update
```

After add repo, you can install Milvus Cluster from helm chart with 3 configuration file to overwrite default value

```bash
helm install milvus-db milvus/milvus -n milvus -f milvus_service.yaml -f milvus_attu.yaml -f milvus_cluster.yaml
```

Wait until all pods are `Running`

```bash
kubectl get pods -n milvus
```

> NOTE
> Helm does not support scheduling the order of service creation. It is normal that business pods to restart for one or two times before etcd and kafka are up in the early stage.

After all things work, you will see your `milvus-db` and `milvus-attu` svc (service)

```bash
# Get MilvusDB
kubectl get svc -n milvus

# Get Ingress Attu
kubectl get ingress -n milvus
```

## Setup ACM Domain in Route 53 for MilvusDB

To protect connection from Attu and convenient in connecting Attu and MilvusDB from remote, You need to setup domain for those services into Route53

You need retrieve `arn` of two LB created by EKS Cluster, and put into definition inside [milvus_eks_service.tf](./terraform/milvus_eks_service.tf) and set domain with certificate depend on your environment to route traffic eith CNAME Record Load Balancer to Project Domain.

## Apply Cluster AutoScaling (CA) for Milvus

> When the first deployment, Milvus will use basic plan with only one mode and do not scale. To increase High Avalability (HA), apply the CA is one of requirement for EKS Cluster

### Apply new spec ASG

To check the status of ASG (Auto scaling group) apply for Milvus cluster. **(NOTE: you need to use the role at lease to permit describe ASG, EC2 to get this information)**

```bash
aws autoscaling \
    describe-auto-scaling-groups \
    --query "AutoScalingGroups[? Tags[? (Key=='eks:cluster-name') && Value=='milvus-cluster']].[AutoScalingGroupName, MinSize, MaxSize, DesiredCapacity]" \
    --output table \
    --region ap-southeast-1
```

```bash
-----------------------------------------------------------------------
|                      DescribeAutoScalingGroups                      |
+------------------------------------------------------+----+----+----+
|  eks-ng-milvus-c4c9808f-ad3f-9cb2-535c-8566bc52adee  |  1 |  1 |  1 |
+------------------------------------------------------+----+----+----+
```

Now, you need to increase number node with MaxSize with at least 1 more

First of all, get the only autoscalinggroupname

```bash
export ASG_NAME=$(aws autoscaling describe-auto-scaling-groups --query " AutoScalingGroups[? Tags[? (Key=='eks:cluster-name') && Value=='milvus-cluster-v2']].AutoScalingGroupName" --output text --region ap-southeast-1 )
```

Now you need to modify with new spec for Milvus ASG

```bash
aws autoscaling \
    update-auto-scaling-group \
    --auto-scaling-group-name ${ASG_NAME} \
    --min-size 2 \
    --desired-capacity 2 \
    --max-size 3 \
    --region ap-southeast-1
```

Apply sucessfully and you can recheck with command

```bash
aws autoscaling \
    describe-auto-scaling-groups \
    --query "AutoScalingGroups[? Tags[? (Key=='eks:cluster-name') && Value=='milvus-cluster-v2']].[AutoScalingGroupName, MinSize, MaxSize,DesiredCapacity]" \
    --output table \
    --region ap-southeast-1
```

```bash
-----------------------------------------------------------------------
|                      DescribeAutoScalingGroups                      |
+------------------------------------------------------+----+----+----+
|  eks-ng-milvus-c4c9808f-ad3f-9cb2-535c-8566bc52adee  |  2 |  3 |  2 |
+------------------------------------------------------+----+----+----+
```

### Create IAM Policy for Cluster Autoscaler

You need to use Terraform to provision policies and provide it for eks cluster. You may need to create the `EKSClusterAutoScaler` policy: 
```yaml
policy = jsonencode({
    "Version" : "2012-10-17",
    "Statement" : [
      {
        "Effect" : "Allow",
        "Action" : [
          "autoscaling:DescribeAutoScalingGroups",
          "autoscaling:DescribeAutoScalingInstances",
          "autoscaling:DescribeLaunchConfigurations",
          "autoscaling:DescribeScalingActivities",
          "autoscaling:SetDesiredCapacity",
          "autoscaling:TerminateInstanceInAutoScalingGroup",
          "ec2:DescribeLaunchTemplateVersions",
          "eks:DescribeNodegroup"
        ],
        "Resource" : "*"
      }
    ]
  })
```

For environment with Kubernetes operations, I provision the permission `EKSClusterAutoScaler` and now youy can create `service account` with Milvus EKS to use this policies

```bash
eksctl create iamserviceaccount \
    --name cluster-autoscaler \
    --namespace kube-system \
    --cluster milvus-cluster \
    --attach-policy-arn "arn:aws:iam::{AWS_ACCOUNT_ID}:policy/EKSClusterAutoScaler" \
    --approve \
    --override-existing-serviceaccounts \
    --region ap-southeast-1
```

Waiting provision completely by AWS Cloudformation, you can check about service account after that with command

```bash
kubectl get serviceaccount -n kube-system cluster-autoscaler -o yaml
```

### Deploy cluster-autoscaler deployment

To deploy, you need run apply command to approve and deloyments manifest of `cluster-autoscaler` into your host with `auto-discovery` ode. Manifest is write and use from [milvus_cluster_autoscaler.yaml](./terraform/Milvus/milvus_cluster_autoscaler.yaml) (NOTE: Explore more about configuration, you can refer to [cluster-autoscaler-autodiscover.yaml](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/examples/cluster-autoscaler-autodiscover.yaml))

```bash
kubectl apply -f milvus_cluster_autoscaler.yaml
```

Waiting few second and check your deployment inside `kube-system` namespace with command

```bash
kubectl get deployments -n kube-system cluster-autoscaler
```

You can set more anotation and option into cluster-autoscaler, explore and read more at [Cluster Autoscaler on AWS](https://github.com/kubernetes/autoscaler/blob/master/cluster-autoscaler/cloudprovider/aws/README.md)

## Setup Metrics Server for Milvus Cluster

![alt text](../assets/images/monitoring.png)

To enhance more visibility and flexibility for monitoring stack to observability milvus cluster for both `metrics` and `logs`. Therefore, follwoing the documentation at [Monitor your cluster performance and view logs](https://docs.aws.amazon.com/eks/latest/userguide/eks-observe.html), I decide to use `CloudWatch` to handle this configuration through couple tools, including

- CloudWatch Agent - Scrape metrics
- Fluentbit - Scrape logs

To more understand configuration, you can double check the definition in [Github - cwagent-fluent-bit-quickstart-enhanced.yaml](https://github.com/aws-samples/amazon-cloudwatch-container-insights/blob/main/k8s-deployment-manifest-templates/deployment-mode/daemonset/container-insights-monitoring/quickstart/cwagent-fluent-bit-quickstart-enhanced.yaml)

Check the configuration at [milvus_cluster_cwagent-fluentbit.yaml](./terraform/Milvus/milvus_cluster_cwagent-fluentbit.yaml)

> Note: Remembe when you apply this configuration, you need to ensure
> 1. Add add-on policy `CloudwatchAgentServerPolicy` into role used by NodePool
> 2. Replace the parameter to pass for CWagent and Fluentbit, e.g: clustername, region, ...

After you double check whole of process, run the apply with `kubectl` command

```bash
kutectl apply -f milvus_cluster_cwagent_fluentbit.yaml
```

Wait a little bit before, you can check `deamonset` workload to successful deploy or not by

```bash
kubectl get pods -n amazon-cloudwatch
```

Now you can turn back into CloudWatch tyo double check about the result

- Metrics: Use all metrics and you can view whole metrics in cluster `ContainerInsights` category
- Logs: Use all logs and you can view EKS Logs on total pods with some category, such as
  - `/aws/containerinsights/Cluster_Name/application`
  - `/aws/containerinsights/Cluster_Name/host`
  - `/aws/containerinsights/Cluster_Name/dataplane`
  - `/aws/containerinsights/Cluster_Name/performance`

## Conclusion

### Complete

After deploy and operating Milvus Cluster, the realistic resource spend for each service inside Milvus Cluster that describe via

![alt text](../assets/images/milvus_actual_nodes_resource.png)

![alt text](../assets/images/milvus_actual_pods_resources.png)

### TODO

> 🔭 **Set limit resources for Milvus Workload** and **apply HPA** for creating High Availability to autoscale pod depend resources was needed for specific time in Milvus Cluster 