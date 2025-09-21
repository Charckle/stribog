USERNAME=charckle
VERSION=$(cat VERSION)
IMAGE=stribog

docker build -f Dockerfile-alpine -t $USERNAME/$IMAGE:$VERSION-alpine .
