#!/bin/bash

# Retrieve current opacity values
active_opacity=$(hyprctl getoption decoration:active_opacity | grep -oP '(?<=float: )\d+\.\d+')
inactive_opacity=$(hyprctl getoption decoration:inactive_opacity | grep -oP '(?<=float: )\d+\.\d+')

# Print the retrieved values for confirmation.
echo "Current active_opacity: $active_opacity"
echo "Current inactive_opacity: $inactive_opacity"

# Path to the temp file in the home directory
temp_file="$HOME/tmp/hypr_opacity_state"

# Check if the temp file exists
if [ -f "$temp_file" ]; then
	# Read previous opacity values from the temp file
	previous_active_opacity=$(grep "active_opacity" "$temp_file" | awk '{print $2}')
	previous_inactive_opacity=$(grep "inactive_opacity" "$temp_file" | awk '{print $2}')
	echo "Previous active_opacity: $previous_active_opacity"
	echo "Previous inactive_opacity: $previous_inactive_opacity"
else
	previous_active_opacity="1.0"
	previous_inactive_opacity="1.0"
fi

# Toggle opacity logic
if [ "$(printf %.6f "$active_opacity")" == "1.000000" ] && [ "$(printf %.6f "$inactive_opacity")" == "1.000000" ]; then
	if [ -f "$temp_file" ]; then
		# Restore original opacity values
		hyprctl keyword decoration:active_opacity "$previous_active_opacity"
		hyprctl keyword decoration:inactive_opacity "$previous_inactive_opacity"
		echo "Restored original opacity values."
		rm "$temp_file"
	else
		echo "No previous opacity values to restore."
	fi
else
	# Save current values to temp file
	mkdir -p "$HOME/tmp"
	echo "active_opacity $active_opacity" >"$temp_file"
	echo "inactive_opacity $inactive_opacity" >>"$temp_file"
	# Set opacity to 1
	hyprctl keyword decoration:active_opacity 1
	hyprctl keyword decoration:inactive_opacity 1
	echo "Set opacity to 1 and saved current values."
fi
