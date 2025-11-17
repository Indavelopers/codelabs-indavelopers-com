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
6. Clone this repo in your home directory: `cd ~`, `git clone https://github.com/Indavelopers/codelabs-indavelopers-com.git`
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

Let's test this, checking at each step if the Deployment is changed or unchanged:

- Try to recreate the Deployment again without changes: `kubectl apply -f webapp-deployment.yaml`
- Now, modify the manifest with a single replica Pod:
  - Using your desired editor, modify `replicas: 3` to `replicas: 1` in `webapp-deployment.yaml`.
  - For example, use Cloud Shell Editor: `edit webapp-deployment.yaml`
  - Redeploy the Deployment: `kubectl apply -f webapp-deployment.yaml`
- Modify the number of replicas back to 3 and redeploy again: `kubectl apply -f webapp-deployment.yaml`
- Now delete the Deployment and redeploy it: `kubectl delete -f webapp-deployment.yaml`, `kubectl apply -f webapp-deployment.yaml`

### Control loop

Kubernetes control plane's kube-controller-manager runs a control loop for all Kubernetes controllers, like Deployments.

The control loop checks the Objects status and spec, and if it finds a diff, performs any remediation action needed to get the status back to the **desired state**.

- Get the name of one Pod managed by the Deployment: `kubectl get pods`
- Kill this Pod: `kubectl delete pods NAME_OF_THE_POD`
- Check how Kubernetes control loop automatically recreates a new Pod: `kubectl get all -w`
- Repeat as many times as desired

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

### Resources

### Probes

## Networking

Duration: 10

- services
- LBs

## Operations

Duration: 10

1. commands: get, describe, logs, exec
2. requests
3. scaling - manual, hpa
4. Multi-container pod
5. Init pods

## Deploying a new version

Duration: 10

1. new container
2. rolling update - history
3. rollback

## Volumes

Duration: 15

1. configmap
2. secrets
3. statefulsets
