# mkdocs_drawio_converter/plugin.py
import os
import re
import subprocess
from pathlib import Path
import shutil
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options

class DrawioConverterPlugin(BasePlugin):
    config_scheme = (
        ('cache_dir', config_options.Type(str)),
        ('format', config_options.Type(str, default='svg')),
        ('embed_format', config_options.Type(str, default='<img alt="{img_alt}" src="{img_src}">')),
        ('link_format', config_options.Type(str, default='[{text}]({href})')),
        ('drawio_executable', config_options.Type(str, default='/opt/drawio-exporter/drawio-exporter'))
    )

    def __init__(self):
        self.sources = []
        self.docs_dir = None

    def on_config(self, config):
        """Handle the configuration phase."""
        self.docs_dir = config['docs_dir']
        self.config['cache_dir'] = self.config.get('cache_dir') or os.path.join(os.getcwd(), '.drawio-cache')
        os.makedirs(self.config['cache_dir'], exist_ok=True)
        return config

    def extract_drawio_references(self, content):
        """Extract Draw.io file references from markdown content."""
        references = []
        
        try:
            # Match markdown image syntax: ![alt](path/to/file.drawio#pagenum)
            image_pattern = r'!\[([^\]]*)\]\(([^)]+\.drawio)(?:#(\d+))?\)'
            matches = re.finditer(image_pattern, content)
            
            for match in matches:
                alt_text = match.group(1)
                file_path = match.group(2)
                page_index = int(match.group(3)) if match.group(3) else 0
                
                references.append({
                    'type': 'image',
                    'match': match.group(0),
                    'alt_text': alt_text,
                    'file_path': file_path,
                    'page_index': page_index
                })
            
            # Match markdown link syntax: [text](path/to/file.drawio)
            link_pattern = r'\[([^\]]*)\]\(([^)]+\.drawio)(?:#(\d+))?\)'
            matches = re.finditer(link_pattern, content)
            
            for match in matches:
                if match.group(0).startswith('!'):  # Skip if it's an image (already processed)
                    continue
                    
                references.append({
                    'type': 'link',
                    'match': match.group(0),
                    'text': match.group(1),
                    'file_path': match.group(2),
                    'page_index': int(match.group(3)) if match.group(3) else 0
                })
        
        except Exception as e:
            print(f"Error extracting Draw.io references: {str(e)}")
            return []
        
        return references

    def ensure_file_cached(self, abs_src_path, source_rel, page_index):
        """Convert Draw.io file using drawio-exporter."""
        try:
            cache_path = Path(self.config['cache_dir'])
            cache_filename = cache_path / f"{source_rel}-{page_index}.{self.config['format']}"
            
            # Create cache subdirectories if needed
            os.makedirs(os.path.dirname(cache_filename), exist_ok=True)

            # Check if we need to update cache
            if cache_filename.exists():
                if os.path.getmtime(abs_src_path) <= os.path.getmtime(cache_filename):
                    return str(cache_filename), 0

            # Prepare command for drawio-exporter
            cmd = [
                self.config['drawio_executable'],
                abs_src_path,
                '--output', os.path.dirname(str(cache_filename)),
                '--format', self.config['format']
            ]

            if page_index > 0:
                cmd.extend(['--page', str(page_index)])

            print(f"Running conversion command: {' '.join(cmd)}")
            
            # Set proper environment variables
            env = os.environ.copy()
            env['DRAWIO_DESKTOP_RUNNER_COMMAND_LINE'] = "/opt/drawio-exporter/runner.sh"
            env['DRAWIO_DESKTOP_EXECUTABLE_PATH'] = "/opt/drawio-exporter/drawio-exporter"
            env['DRAWIO_DESKTOP_COMMAND_TIMEOUT'] = "0"
            
            # Run conversion command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(abs_src_path),
                env=env
            )

            print(f"Command output: {result.stdout}")
            if result.stderr:
                print(f"Command error output: {result.stderr}")

            if result.returncode != 0:
                print(f"Error converting {abs_src_path}:")
                print(f"Command: {' '.join(cmd)}")
                print(f"Error output: {result.stderr}")
                return str(cache_filename), result.returncode

            # Verify the file was created
            if not os.path.exists(cache_filename):
                print(f"Error: Output file {cache_filename} was not created")
                return str(cache_filename), 1

            return str(cache_filename), 0

        except Exception as e:
            print(f"Error during conversion of {abs_src_path}: {str(e)}")
            return str(cache_filename), 1

    def on_page_markdown(self, markdown, page, **kwargs):
        """Process markdown content to handle Draw.io file references."""
        if not markdown:
            return markdown

        try:
            content = markdown
            references = self.extract_drawio_references(content)
            
            for ref in references:
                # Create a DrawioSource object and add to sources list
                source = DrawioSource(ref['file_path'], ref['page_index'])
                self.sources.append(source)
                
                # Generate the path for the converted file
                converted_path = f'{ref["file_path"]}-{ref["page_index"]}.{self.config["format"]}'
                
                # Create the new embed based on reference type
                if ref['type'] == 'image':
                    new_embed = self.config['embed_format'].format(
                        img_alt=ref['alt_text'],
                        img_src=converted_path
                    )
                else:  # link type
                    new_embed = self.config['link_format'].format(
                        text=ref['text'],
                        href=converted_path
                    )
                
                # Replace the original reference with the new embed
                content = content.replace(ref['match'], new_embed)
            
            return content
            
        except Exception as e:
            print(f"Error processing markdown: {str(e)}")
            return markdown

    def on_post_build(self, config):
        """Process all collected sources after the build."""
        sources = set(self.sources)
        print(f"Processing {len(sources)} Draw.io files...")
        
        for source in sources:
            dest_rel_path = f'{source.source_rel}-{source.page_index}.{self.config["format"]}'
            abs_src_path = os.path.join(config['docs_dir'], source.source_rel)
            abs_dest_path = os.path.join(config['site_dir'], dest_rel_path)
            
            print(f"Converting: {source.source_rel}")
            cache_filename, exit_status = self.ensure_file_cached(
                abs_src_path, source.source_rel, source.page_index)
            
            if exit_status != 0:
                print(f'Export failed for {source.source_rel} with exit status {exit_status}; skipping copy')
                continue
                
            try:
                os.makedirs(os.path.dirname(abs_dest_path), exist_ok=True)
                shutil.copy2(cache_filename, abs_dest_path)
                print(f"Successfully converted {source.source_rel} to {dest_rel_path}")
            except FileNotFoundError:
                print(f'Export successful for {source.source_rel}, but output file not found')
            except Exception as e:
                print(f'Error copying file {source.source_rel}: {str(e)}')
        
        self.sources = []

class DrawioSource:
    """Represents a Draw.io source file and its metadata."""
    def __init__(self, source_rel, page_index):
        self.source_rel = source_rel
        self.page_index = page_index

    def __eq__(self, other):
        return (self.source_rel == other.source_rel and 
                self.page_index == other.page_index)

    def __hash__(self):
        return hash((self.source_rel, self.page_index))