#!/bin/bash
set -e
werf compose up --dev --docker-compose-options="--profile dev"
echo "Attache to container with IDE"
werf compose down --dev --docker-compose-options="--profile dev"
echo "Cleaning up..."
werf host purge --dev


project_name=$(grep '^project:' werf.yaml | awk '{print $2}')
if [ -z "$project_name" ]; then
  echo "Project name not found in werf.yaml"
  exit 1
fi

echo "Project name to cleanup: $project_name"

mapfile -t image_ids < <(docker images --format '{{.Repository}} {{.ID}}' | grep "^${project_name}" | awk '{print $2}')

echo "Found ${#image_ids[@]} images for project '$project_name'"

if [ "${#image_ids[@]}" -gt 1 ]; then
  echo "Removing old images (leaving the most recent one)..."
  for (( i=${#image_ids[@]}-1; i>0; i-- )); do
    echo "Removing image ID: ${image_ids[$i]}"
        if ! output=$(docker rmi -f "${image_ids[$i]}" 2>/dev/null); then
        echo "Skipping ${image_ids[$i]} due to error"
        else
        echo "$output"
        fi
  done
else
  echo "No duplicate images to clean up."
fi
