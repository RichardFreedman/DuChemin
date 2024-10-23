REQUESTED:
* SSL Cert issues
* postgresql configured with `POSTGRES_HOST_AUTH_METHOD=trust`
* postgresql not secured
* docker container network exposed?
* postgresql container causing a crash???
* 

DISCOVERD:
* Fixed docker file ln53 `COPY.` -> `COPY .`
* Removed `version=3` in docker-compose.yml obsolete
* load_data script was called in entrypoint.sh but not copied to app folder and named (loaddata.sh)
* django secret key is checked into repository (is this the production secret key)????
* django database username and password are set to default `postgres` && `postgres`
* settings not divided properly between development & production environments
* nginx container is outdated (1.19 -> 1.27)
* python container is outdated (3.9 -> 3.12)
* django is super outdated v3 vs v5
* other packages are outdated
* SIGKILL in django container
* Routing is in correct `/about` and subpages are unreachable also `/help`
* Rest of the migrations are missing?


TODO:
* Setup django settings with proper development and production settings
