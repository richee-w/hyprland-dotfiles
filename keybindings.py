#!/usr/bin/python3

import re
import os
from shutil import copyfile

def extract_keybindings(conf_path):
    if not os.path.exists(conf_path):
        raise FileNotFoundError(f"Configuration file not found: {conf_path}")

    with open(conf_path, 'r') as file:
        conf_content = file.read()

    # Regular expression to match sections and keybindings
    section_pattern = re.compile(r'###\s*(.+?)\n(.*?)(?=\n#|$)', re.DOTALL)
    keybinding_pattern = re.compile(r'^bind\s*=\s*(.+)', re.MULTILINE)

    sections = section_pattern.findall(conf_content)
    keybindings = {}

    for section in sections:
        section_name, section_content = section
        section_bindings = keybinding_pattern.findall(section_content)
        section_bindings = [binding.replace('$mainMod', 'SUPER') for binding in section_bindings]
        keybindings[section_name.strip()] = section_bindings

    return keybindings

def extract_custom_keybindings(custom_conf_path):
    if not os.path.exists(custom_conf_path):
        raise FileNotFoundError(f"Custom configuration file not found: {custom_conf_path}")

    with open(custom_conf_path, 'r') as file:
        conf_content = file.read()

    unbind_pattern = re.compile(r'^unbind\s*=\s*(.+)', re.MULTILINE)
    bind_pattern = re.compile(r'^bind\s*=\s*(.+)', re.MULTILINE)

    unbinds = unbind_pattern.findall(conf_content)
    binds = bind_pattern.findall(conf_content)

    # Replace $mainMod with SUPER in unbinds and binds
    unbinds = [binding.replace('$mainMod', 'SUPER') for binding in unbinds]
    binds = [binding.replace('$mainMod', 'SUPER') for binding in binds]

    return unbinds, binds

def merge_keybindings(default_keybindings, custom_unbinds, custom_binds):
    merged_keybindings = default_keybindings.copy()

    # Unbind keys in default keybindings
    for section in merged_keybindings:
        merged_keybindings[section] = [binding for binding in merged_keybindings[section] if binding not in custom_unbinds]

    # Add/override with custom binds
    for bind in custom_binds:
        section, binding = bind.split(',', 1)
        section = section.strip()
        if section not in merged_keybindings:
            merged_keybindings[section] = []
        merged_keybindings[section].append(binding.strip())

    return merged_keybindings

def write_to_markdown(keybindings, markdown_path):
    # Create a backup of the existing markdown file if it exists
    if os.path.exists(markdown_path):
        backup_path = markdown_path + '.backup'
        copyfile(markdown_path, backup_path)
        print(f"Backup of existing markdown file created at {backup_path}")

    with open(markdown_path, 'w') as md_file:
        md_file.write("# Hyprland Keybindings\n\n")
        for section, bindings in keybindings.items():
            md_file.write(f"## {section}\n")
            for binding in bindings:
                md_file.write(f"- `{binding}`\n")
            md_file.write("\n")

# Paths to the configuration files
default_conf_path = '/home/rich/dotfiles/hypr/conf/keybindings/default.conf'
custom_conf_path = '/home/rich/dotfiles/hypr/conf/custom.conf'
# Path where you want to save the markdown file
markdown_path = '/home/rich/dotfiles/hypr/cheatsheet.md'

try:
    # Extract keybindings from default and custom configurations
    default_keybindings = extract_keybindings(default_conf_path)
    custom_unbinds, custom_binds = extract_custom_keybindings(custom_conf_path)

    # Merge the keybindings
    merged_keybindings = merge_keybindings(default_keybindings, custom_unbinds, custom_binds)

    # Write the merged keybindings to the markdown file
    write_to_markdown(merged_keybindings, markdown_path)

    print(f"Keybindings extracted to {markdown_path}")
except Exception as e:
    print(f"An error occurred: {e}")
