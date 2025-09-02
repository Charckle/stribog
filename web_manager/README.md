# What
- A webapp for getting iformation from websites

## generate password
- `docker image pull charckle/stribog_web_manager:latest` or the image you wnt to use
- `docker run --rm -it charckle/stribog_web_manager:latest python generate_password.py`


## to-do
- email test button

## podman
- the container runs as the user 1000 inside, but because of the user ID mapping, it will be something else on the local machine
    - this is how you change the mountesd folders accordingly:
    - `podman unshare chown -R 1000:1000 ./data`