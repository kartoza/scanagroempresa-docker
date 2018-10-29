#!/usr/bin/env bash

if [ -z "$REPO_NAME" ]; then
	REPO_NAME=kartoza
fi

if [ -z "$IMAGE_NAME" ]; then
	IMAGE_NAME=scanagroempresa_geonode_generic
fi

if [ -z "$TAG_NAME" ]; then
	TAG_NAME=latest
fi

if [ -z "$BUILD_ARGS" ]; then
	BUILD_ARGS="--pull --no-cache"
fi

# Build Args Environment

if [ -z "$SCANAGROEMPRESA_DOCKER_TAG" ]; then
	SCANAGROEMPRESA_DOCKER_TAG=master
fi

if [ -z "$GEONODE_IMAGE" ]; then
	GEONODE_IMAGE=geosolutionsit/geonode-generic:1.0
fi

echo "SCANAGROEMPRESA_DOCKER_TAG=${SCANAGROEMPRESA_DOCKER_TAG}"
echo "GEONODE_IMAGE_TAG=${GEONODE_IMAGE}

echo "Build: $REPO_NAME/$IMAGE_NAME:$TAG_NAME"

docker build -t ${REPO_NAME}/${IMAGE_NAME} \
	--build-arg SCANAGROEMPRESA_DOCKER_TAG=${SCANAGROEMPRESA_DOCKER_TAG} \
	--build-arg GEONODE_IMAGE=${GEONODE_IMAGE} \
	${BUILD_ARGS} .
docker tag ${REPO_NAME}/${IMAGE_NAME}:latest ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
docker push ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
