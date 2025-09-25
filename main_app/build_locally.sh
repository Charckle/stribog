USERNAME=charckle
VERSION=$(cat VERSION)
IMAGE=stribog

docker build -f Dockerfile -t $USERNAME/$IMAGE:$VERSION-alpine .
