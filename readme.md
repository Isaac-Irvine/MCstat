
# Install and run
Make sure you have a docker environment file called env_file with your discord token in it.

Then do the following commands

```shell
docker build -t mcstat .
```

```shell
docker run --env-file env_file --name mcstat mcstat
```