# for Dummies

- [Convention and Guides](#convention-and-guides)
- [Install Python](#install-python)
- [Setup Kubernetes](#setup-kubernetes)
- [Containerize the App](#containerize-the-app)
- [Deploy the Image to VT K8s](#deploy-the-image-to-vt-k8s)

## Convention and Guides

Check the project [docs](./convention-and-style.md) for more guides.

## Install Python

```bash
$ brew install python3
```

## Install Tools

- [Git](https://git-scm.com/)
- [Docker](https://docs.docker.com/get-docker/)
- kubectl ([MacOS](https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/), [Linux](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/))

## Setup Kubernetes

Check [Cloud Quickstart](https://wiki.cs.vt.edu/index.php/Cloud_Quickstart) for more information.

## Containerize the App

```bash
$ docker login
$ docker buildx build --platform linux/amd64 -t <your-docker-id>/stockbots:tagname .
$ docker push <your-docker-id>/stockbots:tagname
```

## Deploy the Image to VT Kubernetes

After you setup your Kubernetes on your local machine, you can run following commands.

```bash
$ kubectl apply -k ./deploy/base
```
