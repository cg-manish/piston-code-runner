#!/bin/bash

# List of languages and their corresponding runtime versions
languages_and_versions=(
  "bash=5.2.0"
  "java=15.0.2"
  "python=3.12.0"
  "ruby=3.0.1"
  "swift=5.3.3"
  "go=1.16.2"
  "scala=3.2.2"
  "kotlin=1.8.20"
  "rust=1.68.2"
  "c++=10.2.0"
  "c=10.2.0"
  "dotnet=5.0.201"
  "javascript=20.11.1"
  "typescript=5.0.3"
)

# Loop through each language and runtime
for lang_ver in "${languages_and_versions[@]}"; do
  # Split the string into language and version
  IFS="=" read -r language version <<< "$lang_ver"
  
  # Run the install command
  echo "Installing $language with version $version"

"$HOME/piston/cli/index.js" ppman install "$language=$version"
done
