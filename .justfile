_default:
  @just --list --unsorted

run-test-app:
  cd home_energy && \
  python app.py