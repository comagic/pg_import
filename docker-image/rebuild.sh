set -o xtrace

docker image rm andruche/pg_import:2.1.0-arm64
docker image rm andruche/pg_import:2.1.0-amd64
docker image rm andruche/pg_import:2.1.0
docker buildx build --platform linux/arm64/v8 -f Dockerfile -t andruche/pg_import:2.1.0-arm64 .
docker buildx build --platform linux/amd64 -f Dockerfile -t andruche/pg_import:2.1.0-amd64 .
docker push andruche/pg_import:2.1.0-amd64
docker push andruche/pg_import:2.1.0-arm64
docker manifest rm andruche/pg_import:2.1.0
docker manifest create andruche/pg_import:2.1.0 --amend andruche/pg_import:2.1.0-arm64 --amend andruche/pg_import:2.1.0-amd64
docker manifest push andruche/pg_import:2.1.0
docker pull andruche/pg_import:2.1.0
