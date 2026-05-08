#!/usr/bin/env bash
set -euo pipefail

BASE_URL="https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release"
WORKDIR="$(mktemp -d)"

cleanup() {
  rm -rf "${WORKDIR}"
}
trap cleanup EXIT

download_rule() {
  local rule_name="$1"
  local output_path="${WORKDIR}/${rule_name}"

  echo "Downloading ${rule_name}..."
  curl -L -s --fail "${BASE_URL}/${rule_name}" -o "${output_path}"
}

merge_rules() {
  local output_file="$1"
  shift

  local combined_file="${WORKDIR}/${output_file}.combined"
  local cleaned_file="${WORKDIR}/${output_file}.cleaned"

  : > "${combined_file}"

  for rule_name in "$@"; do
    download_rule "${rule_name}"
    grep '^  - ' "${WORKDIR}/${rule_name}" >> "${combined_file}"
  done

  echo "payload:" > "${cleaned_file}"
  sort -u "${combined_file}" >> "${cleaned_file}"
  mv "${cleaned_file}" "${output_file}"

  echo "Updated ${output_file} ($(wc -l < "${output_file}" | tr -d ' ') rules)"
}

merge_rules "merged_proxy.txt" \
  "proxy.txt" \
  "gfw.txt" \
  "tld-not-cn.txt" \
  "google.txt"

merge_rules "merged_direct.txt" \
  "direct.txt" \
  "cncidr.txt" \
  "lancidr.txt" \
  "apple.txt" \
  "icloud.txt"

merge_rules "merged_reject.txt" \
  "reject.txt" \
  "private.txt"
