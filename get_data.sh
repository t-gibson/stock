#!/usr/bin/env bash
#
# Script to download and process the Southpark script data

set -o errexit
set -o pipefail
set -o nounset
[[ "${DEBUG:-""}" = "true" ]] && set -o xtrace

RAW_DATA_DIR="data/raw/southpark"
PROCESSED_DATA_DIR="data/processed"
GIT_URL="https://github.com/BobAdamsEE/SouthParkData.git"

main () {
  mkdir -p "${RAW_DATA_DIR}" "${PROCESSED_DATA_DIR}"

  # if fails we assume the repo has already been cloned
  git clone "${GIT_URL}" "${RAW_DATA_DIR}" || true

  python prepare_data.py \
    "${RAW_DATA_DIR}/All-seasons.csv" \
    "${PROCESSED_DATA_DIR}/character-lines.csv"
}


main "$@"
