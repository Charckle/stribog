USERNAME=charckle
VERSION=$(cat VERSION)
IMAGE=stribog_web_manager

docker build -f Dockerfile-alpine -t $USERNAME/$IMAGE:$VERSION-alpine .
