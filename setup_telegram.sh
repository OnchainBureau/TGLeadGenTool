      #!/bin/bash

      # Navigate to the instances directory
      cd "$(dirname "$0")"

      # Define the list of instance IDs
      INSTANCE_IDS=("56937386202" "56937481408" "56986426330")

      # Loop through each instance and set up Telegram AppImage
      for instance in "${INSTANCE_IDS[@]}"; do
          cd "$instance" || { echo "Directory $instance not found!"; exit 1; }
          wget https://telegram.org/dl/desktop/linux -O Telegram.AppImage
          chmod +x Telegram.AppImage
          # Rename to Telegram for consistency
          mv Telegram.AppImage Telegram
          cd ..
      done