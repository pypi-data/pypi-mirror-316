# mkdocs_drawio_converter/plugin.py
import os
import sys
import re
import subprocess
from pathlib import Path
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options
from mkdocs.structure.files import Files
from mkdocs.utils import copy_file
import mkdocs.plugins

log = mkdocs.plugins.log.getChild('drawio-converter')

class ConfigurationError(Exception):
    """Raised when there's an error in the plugin configuration."""
    pass

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

class DrawioConverterPlugin(BasePlugin):
    config_scheme = (
        ('cache_dir', config_options.Type(str)),
        ('drawio_executable', config_options.Type(str)),
        ('drawio_args', config_options.Type(list, default=[])),
        ('format', config_options.Type(str, default='svg')),
        ('embed_format', config_options.Type(str, default='<img alt="{img_alt}" src="{img_src}">')),
        ('link_format', config_options.Type(str, default='[{text}]({href})')),
        ('sources', config_options.Type(str, default='*.drawio')),
    )

    DRAWIO_EXECUTABLE_NAMES = ['drawio', 'draw.io', 'diagrams.net']
    
    def __init__(self):
        self.sources = []
        self.docs_dir = None

    # [Previous methods remain the same until extract_drawio_references]

    def extract_drawio_references(self, content):
        """Extract Draw.io file references from markdown content."""
        references = []
        
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
            link_text = match.group(1)
            file_path = match.group(2)
            page_index = int(match.group(3)) if match.group(3) else 0
            
            # Skip if this is actually an image (already processed)
            if match.group(0).startswith('!'):
                continue
            
            references.append({
                'type': 'link',
                'match': match.group(0),
                'text': link_text,
                'file_path': file_path,
                'page_index': page_index
            })
        
        # Process all file paths to be relative to docs_dir
        for ref in references:
            file_path = ref['file_path']
            if os.path.isabs(file_path):
                try:
                    file_path = os.path.relpath(file_path, self.docs_dir)
                except ValueError:
                    log.warning(f"File {file_path} is outside documentation directory")
                    continue
            
            # Normalize path separators
            file_path = file_path.replace('\\', '/')
            ref['file_path'] = file_path
            
        return references

    def on_page_markdown(self, markdown, page, **kwargs):
        """Process markdown content to handle Draw.io file references."""
        if not markdown:
            return markdown

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
            
            log.debug(f'Processed Draw.io reference in {page.file.src_path}: {ref["file_path"]} (type: {ref["type"]})')
        
        return content

    def ensure_file_cached(self, src_path, source_rel, page_index):
        """Ensure the file is in cache and up to date."""
        cache_path = Path(self.config['cache_dir'])
        
        # Create subdirectories in cache to maintain structure
        rel_dir = os.path.dirname(source_rel)
        if rel_dir:
            cache_subdir = cache_path / rel_dir
            cache_subdir.mkdir(parents=True, exist_ok=True)
        
        cache_filename = cache_path / f"{source_rel}-{page_index}.{self.config['format']}"
        
        # Check if we need to update cache
        if (not cache_filename.exists() or 
            os.path.getmtime(src_path) > os.path.getmtime(cache_filename)):
            
            try:
                cmd = [
                    self.config['drawio_executable'],
                    '--export',
                    src_path,
                    '--format', self.config['format'],
                    '--output', str(cache_filename),
                    *self.config['drawio_args']
                ]
                
                if page_index > 0:
                    cmd.extend(['--page-index', str(page_index)])
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                return str(cache_filename), result.returncode
                
            except subprocess.CalledProcessError as e:
                log.error(f"Error converting {src_path}: {e}")
                return str(cache_filename), e.returncode
                
        return str(cache_filename), None

    def on_files(self, files, config, **kwargs):
        """Filter out cache files from processing."""
        cache_dir = Path(self.config['cache_dir'])
        return Files([f for f in files if not str(f.abs_src_path).startswith(str(cache_dir))])

    def on_post_build(self, config, **kwargs):
        """Process all collected sources after the build."""
        sources = set(self.sources)
        log.debug(f'Processing {len(sources)} unique sources')
        
        for source in sources:
            dest_rel_path = f'{source.source_rel}-{source.page_index}.{self.config["format"]}'
            abs_src_path = os.path.join(config['docs_dir'], source.source_rel)
            abs_dest_path = os.path.join(config['site_dir'], dest_rel_path)
            
            cache_filename, exit_status = self.ensure_file_cached(
                abs_src_path, source.source_rel, source.page_index)
            
            if exit_status not in (None, 0):
                log.error(f'Export failed with exit status {exit_status}; skipping copy')
                continue
                
            try:
                copy_file(cache_filename, abs_dest_path)
            except FileNotFoundError:
                log.warning('Export successful, but wrote no output file')
        
        self.sources = []