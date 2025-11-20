summary: Introduction to Kubernetes
id: introduction-to-k8s
categories: Kubernetes
status: Published
authors: Marcos Manuel Ortega
Feedback Link: <https://github.com/Indavelopers/codelabs-indavelopers-com>

# Introduction to Kubernetes

## Introduction

Duration: 5

### What You'll Learn

- Workspace
- Containers
- Kubernetes
- Deploying the webapp to Kubernetes
- Namespaces, labels, resources, probes
- Networking
- Operations
- Deploying a new version
- Volumes

## Workspace

1. Remember to use the same Google account you used to register for the workshop
2. Recommended: Follow the workshop using the Google Cloud [Cloud Console](https://console.cloud.google.com) and [Cloud Shell](https://shell.cloud.google.com)
3. In your lab project, you'll find a GKE kubernetes cluster pre-provisioned for you
4. Fetch your GKE cluster credentials into your `kubectl` config: `gcloud container clusters get-credentials lab-cluster --location europe-west4-a`, where `lab-cluster` is the name of your cluster and `europe-west4-a` is the region
   1. If needed, change the cluster name and location
5. Test your `kubectl` config: `kubectl version`, `kubectl cluster-info`
6. Enable kubectl autocompletion for Bash: `source <(kubectl completion bash)`
   1. Optionally, enable it permanently for your user: `echo 'source <(kubectl completion bash)' >>~/.bashrc`
7. Clone this repo in your home directory: `cd ~`, `git clone https://github.com/Indavelopers/codelabs-indavelopers-com.git`
   1. You can also use a different location. If so, mind your repo location when changing directories in next steps

## Containers

Duration: 15

Kubernetes deploys and manages containerized applications, using the OCI container standard.
We will containerize a Python Flask hello-world webapp.

### Webapp

The webapp code is in `codelabs-content/introduction-to-k8s/webapp/src`:

- `main.py`: Main Python Flask webapp code.
- `requirements.py`: Python module dependencies in Pip requirements format.
- `venv`: Python virtual environment.
- `Dockerfile`: Dockerfile for the container image.

Check the app locally:

1. Work in the webapp dir: `cd ~/codelabs-indavelopers-com/codelabs/introduction-to-k8s/webapp/src`
1. Activate the virtual environment: `source venv/bin/activate`
1. Install Python dependencies: `pip install -r requirements`
1. Run Flask in debug mode: `flask --app main run --debug`
1. Check the app locally on `localhost:5000` with the Cloud Shell "Web preview" option.
   1. Cancel the Flask debug server with `Ctrl+C`
   1. Deactivate the virtual environment: `deactivate`

### Containerize the webapp

Create a container image using the provided `Dockerfile` and push it to the provided container repository in Google Artifact Registry:

1. Check the envvar setting your Google Cloud project ID in Cloud Shell: `echo $GOOGLE_CLOUD_PROJECT`
   1. If needed, change the project ID (`YOUR_PROJECT_ID`) and set up the envvar again: `gcloud config set project YOUR_PROJECT_ID`, `export GOOGLE_CLOUD_PROJECT=YOUR_PROJECT_ID`
2. Create the container image locally with Docker: `docker build -t europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo/webapp:v1 .`
3. Check the containerized app locally on `localhost:5000`: `docker run -p 5000:5000 europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo/webapp:v1`
4. Authenticate your local Docker installation with your user account: `gcloud auth configure-docker europe-west4-docker.pkg.dev`
5. Push the container image to Google Artifact Registry: `docker push europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo/webapp:v1`
6. Check the container image on Google Artifact Registry: In the Cloud Console, navigate to Google Artifact Registry, check the `lab-repo` Docker repository, and find your pushed container image

## Kubernetes

Duration: 30

"Kubernetes is my _container shepherd_, it maintains my containerized applications for me."

1. [Kubernetes](https://kubernetes.io) is an OSS container orchestrator for [OCI containers]([https://](https://opencontainers.org/)) maintained by the [CNCF](https://www.cncf.io), initially developed by Google based on [Borg](https://research.google/pubs/large-scale-cluster-management-at-google-with-borg/).
2. Kubernetes acts as an intermediate declarative layer, hiding the complex infrastructure from the user.
3. This OSS intermediate layer standarizes the underlying infrastructure, so that the app can be migrated 'as is' from one environment to another, and the user uses the same API, commands and tools.
4. Kubernetes was designed from the ground up to be a "platform for developing platforms", with API extensibility in mind.
5. The original design goal for Kubernetes was to become the single cluster for all applications and workloads, sharing the same resources in a more compact manner ([From Google to the world: The Kubernetes origin story](https://cloud.google.com/blog/products/containers-kubernetes/from-google-to-the-world-the-kubernetes-origin-story))

Kubernetes follows:

- "Object over object over object".
- "Abstraction over abstraction over abstraction".

### Architecture

[Kubernetes architecture](https://kubernetes.io/docs/concepts/architecture/)

![Kubernetes Architecture](assets/kubernetes-cluster-architecture.svg)

([Original image](https://kubernetes.io/images/docs/kubernetes-cluster-architecture.svg))

### Pods

[Pods](https://kubernetes.io/docs/concepts/workloads/pods/)

![Pods](assets/module_03_nodes.svg)

([Original image](https://d33wubrfki0l68.cloudfront.net/5cb72d407cbe2755e581b6de757e0d81760d5b86/a9df9/docs/tutorials/kubernetes-basics/public/images/module_03_nodes.svg))

- Pods are the minimum deployment and management unit in Kubernetes.
- Pods abstract "an application deployed on a server". Like a server, a Pod:
  - Can run more than one container, as a server runs more than one process.
    - For example, auxiliary containers or init containers.
  - Runs an internal loopback network where conatiners can communicate with each other on different ports, as different processes on a server communicate using `localhost`.
  - Have a single IP, where containers can open ports for external communication, as different processes on a server can use the single server IP
  - Allows all containers to individually mount and use the shared storage volumes, as different processes on a server can mount the same storage volumes.

### Running a Pod

You can create Kubernetes objects, like a Pod, using imperative commands. This is useful for quick tests and learning, but for production workloads, it's recommended to use declarative manifests (YAML files).

1. Run a Pod named `webapp` using the `webapp` image you pushed to Artifact Registry: `kubectl run webapp --image=europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo/webapp:v1`
2. Check the status of your Pod. Wait for it to be in the `Running` state: `kubectl get pods`
3. To access the application running inside the Pod from your Cloud Shell, you can use port-forwarding. This will forward traffic from a port on your local machine (Cloud Shell) to the port inside the Pod: `kubectl port-forward pod/webapp 5000:5000`
4. Now you can use the Cloud Shell "Web preview" on port 5000 to see your "Hello, world!" message.
5. Once you are done, stop the port-forwarding with `Ctrl+C` and delete the Pod to clean up your environment: `kubectl delete pod webapp`

## Deploying the webapp to Kubernetes

Duration: 15

- [Kubernetes objects, desired vs actual status, manifests](https://kubernetes.io/docs/concepts/overview/working-with-objects/)
- [Declarative object configuration](https://kubernetes.io/docs/concepts/overview/working-with-objects/object-management/#declarative-object-configuration)
- [Controllers](https://kubernetes.io/docs/concepts/workloads/controllers/)
- [Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [ReplicaSets](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/)

### Deploying the webapp

- Work in `webapp/manifests`: `cd ~/codelabs-indavelopers-com/codelabs/introduction-to-k8s/webapp/manifests`
- Replace `YOUR_PROJECT_ID` in the Deployment manifest with your actual project ID: `sed -i "s/YOUR_PROJECT_ID/$GOOGLE_CLOUD_PROJECT/g" webapp-deployment.yaml`
- Check the Deployment manifest at `webapp-deployment.yaml`: `cat webapp-deployment.yaml`
- Create the Deployment: `kubectl apply -f webapp-deployment.yaml`
- Check the Deployment and its Pods: `kubectl get all`

### Declarative approach

With a declarative approach, you can manage any object with full idempotency:

- If the resource with the same Kind and name doesn't exists, it will be created.
- If it exists, and there's no change in the manifest, it will remain unchanged.
- If it exists, and there's a change in the manifest, it will be updated.

Let's test this, checking at each step if the Deployment is changed or unchanged, by using `kubectl apply -f MANIFEST_FILE.yaml`:

- Try to recreate the Deployment again without changes: `kubectl apply -f webapp-deployment.yaml`
- Now, modify the manifest with a single replica Pod:
  - Using your desired editor, modify `replicas: 3` to `replicas: 1` in `webapp-deployment.yaml`.
  - For example, use Cloud Shell Editor: `edit webapp-deployment.yaml`
  - Redeploy the Deployment: `kubectl apply -f webapp-deployment.yaml`
  - Check the Deployment and its Pods: `kubectl get all`
- Modify the number of replicas back to 3 and redeploy again: `kubectl apply -f webapp-deployment.yaml`
- Check the Deployment and its Pods: `kubectl get all`
- Now delete the Deployment and redeploy it: `kubectl delete -f webapp-deployment.yaml`, `kubectl apply -f webapp-deployment.yaml`
- Check the Deployment and its Pods: `kubectl get all`

### Control loop

Kubernetes control plane's kube-controller-manager runs a control loop for all Kubernetes controllers, like Deployments.

The control loop checks the Objects status and spec, and if it finds a diff, performs any remediation action needed to get the status back to the **desired state**.

- Get the name of one Pod managed by the Deployment: `kubectl get pods`
- Kill this Pod: `kubectl delete pods NAME_OF_THE_POD`
- Check how Kubernetes control loop automatically recreates a new Pod: `kubectl get all`

## Namespaces, labels, resources, probes

Duration: 10

### Namespaces

Namespaces allows the separation of operations, access control, and resource asignation for different applications.

- Check default Kubernetes namespaces: `kubectl get namespaces`
- Create a new namespace for the webapp: `kubectl create -f webapp-namespace.yaml`
- Check the new namespace: `kubectl get namespaces`
- Delete the webapp Deployment from the `default` namespace: `kubectl delete -f webapp-deployment.yaml`
- Deploy the Deployment to the new namespace: `kubectl apply -n webapp -f webapp-deployment.yaml`
- Check there are not resources in the default namespace: `kubectl get all`
- Check there are resources in the webapp namespace: `kubectl get all -n webapp`

### Labels

Labels allow to group together several resources, even of different kinds, and can also be used as selectors:

- For the `webapp-deployment`, check the Deployment and Pods labels, and Deployment selector: `cat webapp-deployment.yaml`
- Get all Pods filtering by label `app=webapp`: `kubectl get pods -l app=webapp -n webapp`
- Get all Deployments filtering by label `app=webapp`: `kubectl get deployments -l app=webapp -n webapp`

### Resources

For Kubernetes to be able to choose the best Node to deploy the Pods, and have a compact use of resources across the whole cluster, you should always asign request and limits for each container resources.

- _Requests_ set the minimum requested resources to run the Pod in normal operations.
- _Limits_ allows the containers to use more resources than requested if there are free resources in the Node, but:
  - Kills the Pod if uses more memory than the limit.
  - Limits the containers to the CPU limit.

- Check resources assigned to the single-container Pods in `webapp-deployment`: `cat webapp-deployment.yaml`

You can also add [ResourceQuota](https://kubernetes.io/docs/concepts/policy/resource-quotas/) to a namespace to limit maximum resources for an app.

To enforce that every container has requests and limits declared, set up min. and max. requests and limits, and more, you can use [LimitRange](https://kubernetes.io/docs/concepts/policy/limit-range/).

### Probes

Kubernetes maintains the Pods running through _controller_ objects like _Deployments_, recreating Pods in an `exited` status if the container process crashes.

Nevertheless, many times an application becomes unresponsive or present some issues while in a `running` state.

In order to Kubernetes to be able to check the application status, and not only the container, there are 3 available _probes_:

- Liveness: determine if the application is running but unable to make progress, and the container needs to be restarted.
- Readiness: determine if the container and the application is ready to start to receive traffic.
- Startup: determine if the application inside the container has started, and disables _liveness_ and _readiness_ probes until it succeds

You can find an example of the use of probes here: [Configure Liveness, Readiness and Startup Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/#define-readiness-probes).

## Networking

Duration: 10

[Services](https://kubernetes.io/docs/concepts/services-networking/service/) acts as static endpoints to access application running in ephemeral Pods, distributing requests across Pods.

Services come in 4 flavours:

- ClusterIP: Internal service, only reacheable from inside the Kubernetes cluster - except for a [Multi Cluster Service](https://kubernetes.io/docs/concepts/services-networking/multi-cluster-service/)
- NodePort: External service, opens a high-number port in each Node's IP, either for private or public access.
- LoadBalancer: External service, uses either a cloud provider load balancer or other available implementations. Configurable for private or public access.
- ExternalName: Maps a Service to a DNS name, used for example in migration or hybrid environments.

In Google Cloud, LoadBalancer Services are implemented as regional external, non-proxy TCP Network Load Balancers.

### Deploying a LoadBalancer Service

- Check the `webapp-service` in `manifests`: `cat webapp-service.yaml`
- Create the Service: `kubectl apply -f webapp-service.yaml -n webapp`
- Check the Service: `kubectl get services -n webapp`
- Wait for the cloud external load balancer to adquire a public IP: `kubectl get services webapp-service -n webapp -w`
- Copy your external load balancer IP as `EXTERNAL_LOAD_BALANCER_IP`: `kubectl get services webapp-service -n webapp -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`
- Check your application through the external load balancer's IP: `curl http://EXTERNAL_LOAD_BALANCER_IP`
- Check the load balancer automatically created: in the Cloud Console, search for `Network Services > Load Balancing`, locate the load balancer and check its configuration.

### L7 LoadBalancer

While a LoadBalancer Service is implemented as a L4 load balancer, you can also use [Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/) or the new, preferred [Gateway API](https://kubernetes.io/docs/concepts/services-networking/gateway/) to deploy L7 load balancers, which are implemented in Google Cloud as global external HTTPS Application Load Balancers.

## Operations

Duration: 10

### Commands

Let's check in deep the most common Kubectl commands for normal operations and object troubleshooting:

#### Get

_Get_ is the first basic Kubectl command and Kubernetes API method. It list objects of selected _Kind_ in that _namespace_ (`default` if not specified).

Try it:

- `kubectl get all`
- `kubectl get all -n webapp`
- `kubectl get pods -n webapp`
- `kubectl get pods -n webapp NAME_OF_POD`
- `kubectl get deployments -n webapp`
- `kubectl get deployments -n webapp webapp-deployment`
- Get _spec_ and _status_ info for an object: `kubectl get deployments -n webapp webapp-deployment -o yaml > webapp-deployment_output.yaml`, `cat webapp-deployment_output.yaml`
  - This way, you can get the YAML manifest with the spec for any created object, save it and use it for redeploying the object, or modifying it - in this case, mind the _generation_ field.

#### Describe

_Describe_ is the second basic Kubectl command and Kubernetes API method. It describes in full the _spec_ and _status_ of any object, but doesn't use the same manifest _spec_ API schema (use `kubectl get KIND OBJECT_NAME -o yaml` for that).

Try it:

- `kubectl get pods -n webapp`
- `kubectl describe pods NAME_OF_POD -n webapp`
- `kubectl describe deployments webapp-deployment -n webapp`
- `kubectl describe all`

Getting firtst and then describing a Deployment is usually the best way to find it's current _status_ and troubleshoot any problems, like the common _CrashLoopBackOff_ error.

#### Logs

_Logs_ is the third basic Kubectl command and Kubernetes API method. It returns logs for a specific Pod or, if there are multiple containers in that Pod, for a specific container.

Try it:

- `kubectl get pods -n webapp`
- `kubectl logs NAME_OF_POD -n webapp`

#### Exec

_Exec_ is the fourth basic Kubectl command and Kubernetes API method. It allows to run a single command in a Pod container, or stablish an interactive TTY terminal.

Try it:

- `kubectl get pods -n webapp`
- `kubectl exec NAME_OF_POD -n webapp -- ls /`
- `kubectl exec NAME_OF_POD -it -n webapp -- /bin/bash`
  - `ls /app`
  - `whoami`
  - `uname`
  - `exit`

### HorizontalPodAutoscaler

After manually scaling the Deployment, changing the number of replicas and redeploying it, we'll configure a [HorizontalPodAutoscaler](https://kubernetes.io/docs/tasks/run-application/horizontal-pod-autoscale/):

- Check the `webapp-hpa` in `manifests`: `cat webapp-hpa.yaml`
- Create the HPA: `kubectl apply -f webapp-hpa.yaml -n webapp`
- Check the HPA: `kubectl get hpa webapp-hpa -n webapp`
- Watch for the number of running Pods for the `webapp-deployment` and the `webapp-hpa` HPA behaviour: `kubectl get hpa webapp-hpa -n webapp -w`
- Find the ClusterIP for the `webapp-service` Service, so we can test it internally instead of through the external load balancer as `SERVICE_CLUSTERIP`: `kubectl get service webapp-service -n webapp -o jsonpath='{.spec.clusterIP}'`
- Now open another Cloud Shell terminal tab and create some load: `kubectl run -it load-generator --rm --image=busybox:1.37 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://SERVICE_CLUSTERIP; done"`
- In a couple of minutes, you should see the CPU increasing, and new Pods spinning up.

## Deploying a new version

Duration: 10

Now we'll explore how to deploy a new app version for the `webapp` Deployment. In this case, a new version will be defined by a new container image tag/version, and will be updated with a rolling update, which is the default Deployment updating policy.

First, let's create and push the new container image:

- Work in `codelabs-content/introduction-to-k8s/webapp/src`: `cd codelabs-content/introduction-to-k8s/webapp/src`
- Modify `main.py` to return a new message, eg. from `return 'Hello, world!'` to `return 'Hello, world! v2'`
- Test your webapp locally:
  - Activate the Python virtual environment: `source venv/bin/activate`
  - Run the Flask app in debug mode: `flask --app main run --debug`
  - Check the app locally on `localhost:5000` with the Cloud Shell "Web preview" option.
  - Cancel the Flask debug server with `Ctrl+C`
  - Deactivate the virtual environment: `deactivate`
- Now build the new container image version with the `v2` tag: `docker build -t europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo/webapp:v2 .`
- And push the new container image version to Artifact Registry: `docker push europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo/webapp:v2`
- Check the container image on Google Artifact Registry: `gcloud artifacts docker images list europe-west4-docker.pkg.dev/$GOOGLE_CLOUD_PROJECT/lab-repo`

Now let's deploy the new `webapp-deployment` version with a rolling update:

- Work in `codelabs-content/introduction-to-k8s/webapp/manifests`: `cd codelabs-content/introduction-to-k8s/webapp/manifests`
- Modify `webapp-deployment.yaml` to use the new `v2` container image, using Cloud Shell Editor, nano, vim or emacs: `edit webapp-deployment.yaml`
- Now redeploy the Deployment with a new version: `kubectl apply -f webapp-deployment.yaml -n webapp`
- Check the Deployment recreating its Pods: `kubectl get pods -n webapp -w`, then `Ctrl + C`
- Copy your external load balancer IP as `EXTERNAL_LOAD_BALANCER_IP`: `kubectl get services webapp-service -n webapp -o jsonpath='{.status.loadBalancer.ingress[0].ip}'`
- Check your application new version through the external load balancer's IP: `curl http://EXTERNAL_LOAD_BALANCER_IP`

Sometimes, new application versions present some issues and you need to revert to the previous version. In that case, Kubernetes maintains a history of Deployments revisions that you can use for a quick rollback:

- Check the Deployment revision history: `kubectl rollout history deployment webapp-deployment -n webapp`
- You should see 2 revisions. Check the previous revision with index `1`: `kubectl rollout history deployment webapp-deployment -n webapp --revision 1`
- Rollback to the previous revision: `kubectl rollout undo deployment webapp-deployment -n webapp`
  - You could also specify to which revision to rollback with `kubectl rollout undo deployment webapp-deployment -n webapp --to-revision 1`
- Now check again the Deployment recreating its Pods: `kubectl get pods -n webapp -w`, then `Ctrl + C`
- Check the status of the rollout/rollback: `kubectl rollout status deployment webapp-deployment -n webapp`
- When all Pods are ready, check again your application new version through the external load balancer's IP: `curl http://EXTERNAL_LOAD_BALANCER_IP`
- Describe the Deployment and check the container image version in use: `kubectl describe deployments webapp-deployment -n webapp`

If you were able to solve the issue, and want to rollback again to `v2`, you can rollback to that revision:

- Rollback to the previous revision: `kubectl rollout undo deployment webapp-deployment -n webapp --to-revision 2`
- Check the Deployment revision history with the new revision: `kubectl rollout history deployment webapp-deployment -n webapp`
- Now check again the Deployment recreating its Pods: `kubectl get pods -n webapp -w`, then `Ctrl + C`
- When all Pods are ready, check again your application "new" version through the external load balancer's IP: `curl http://EXTERNAL_LOAD_BALANCER_IP`

## Volumes

Duration: 15

1. configmap
2. secrets
3. statefulsets

TODO
