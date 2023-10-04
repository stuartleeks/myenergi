_default:
  @just --list --unsorted

run-test-app:
  cd home_energy && \
  python app.py

deploy-infra:
	./scripts/deploy-infra.sh

run-job:
  ./scripts/run-job.sh
