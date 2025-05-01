#!/bin/bash
set -e
werf compose down --dev --docker-compose-options="--profile dev" --docker-compose-command-options="-v"
werf host purge --dev


project_name=$(grep '^project:' werf.yaml | awk '{print $2}')
if [ -z "$project_name" ]; then
  echo "Project name not found in werf.yaml"
  exit 1
fi

echo "Project name to cleanup: $project_name"

mapfile -t image_ids < <(docker images --format '{{.Repository}} {{.ID}}' | grep "^${project_name}" | awk '{print $2}')

echo "Found ${#image_ids[@]} images for project '$project_name'"

if [ "${#image_ids[@]}" -gt 0 ]; then
  echo "Removing old images (leaving the most recent one)..."
  for image_id in "${image_ids[@]}"; do
    echo "Removing image ID: ${image_id}"
        if ! output=$(docker rmi -f "${image_id}" 2>/dev/null); then
        echo "Skipping ${image_ids[$i]} due to dependencie"
        else
        echo "$output"
        fi
  done
else
  echo "No duplicate images to clean up."
fi
