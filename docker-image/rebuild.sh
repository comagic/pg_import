set -o xtrace

version=2.5.0

docker image rm andruche/pg_import:$version-arm64
docker image rm andruche/pg_import:$version-amd64
docker image rm andruche/pg_import:$version
docker manifest rm andruche/pg_import:$version
docker manifest rm andruche/pg_import:latest

set -e

docker buildx build --platform linux/arm64/v8 -f Dockerfile -t andruche/pg_import:$version-arm64 .
docker buildx build --platform linux/amd64 -f Dockerfile -t andruche/pg_import:$version-amd64 .
docker push andruche/pg_import:$version-arm64
docker push andruche/pg_import:$version-amd64
docker manifest create andruche/pg_import:$version --amend andruche/pg_import:$version-arm64 --amend andruche/pg_import:$version-amd64
docker manifest push andruche/pg_import:$version
docker manifest create andruche/pg_import:latest --amend andruche/pg_import:$version-arm64 --amend andruche/pg_import:$version-amd64
docker manifest push andruche/pg_import:latest
docker pull andruche/pg_import:$version
