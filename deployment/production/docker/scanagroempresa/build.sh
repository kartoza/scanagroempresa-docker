#!/usr/bin/env bash

if [ -z "$REPO_NAME" ]; then
	REPO_NAME=kartoza
fi

if [ -z "$IMAGE_NAME" ]; then
	IMAGE_NAME=scanagroempresa
fi

if [ -z "$TAG_NAME" ]; then
	TAG_NAME=latest
fi

if [ -z "$BUILD_ARGS" ]; then
	BUILD_ARGS="--pull --no-cache"
fi

# Build Args Environment

if [ -z "$SCANAGROEMPRESA_TAG" ]; then
	SCANAGROEMPRESA_TAG=develop
fi

echo "SCANAGROEMPRESA_TAG=${SCANAGROEMPRESA_TAG}"

echo "Build: $REPO_NAME/$IMAGE_NAME:$TAG_NAME"

docker build -t ${REPO_NAME}/${IMAGE_NAME} \
	--build-arg SCANAGROEMPRESA_TAG=${SCANAGROEMPRESA_TAG} \
	${BUILD_ARGS} .
docker tag ${REPO_NAME}/${IMAGE_NAME}:latest ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
docker push ${REPO_NAME}/${IMAGE_NAME}:${TAG_NAME}
