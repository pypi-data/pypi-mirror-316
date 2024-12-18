import os
import shutil
import tempfile
import unittest
from pathlib import Path
import subprocess
import yaml
from mkdocs.config import load_config
from mkdocs.structure.files import Files
from mkdocs_drawio_converter.plugin import DrawioConverterPlugin

class TestDrawioConverterPlugin(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for testing
        self.test_dir = tempfile.mkdtemp()
        self.docs_dir = os.path.join(self.test_dir, 'docs')
        self.site_dir = os.path.join(self.test_dir, 'site')
        self.cache_dir = os.path.join(self.test_dir, '.drawio-cache')
        
        # Create necessary directories
        os.makedirs(self.docs_dir)
        os.makedirs(os.path.join(self.docs_dir, 'diagrams', 'vector'))
        os.makedirs(self.site_dir)
        
        # Create test drawio file
        self.create_test_drawio_file()
        
        # Create test markdown file
        self.create_test_markdown_file()
        
        # Create test mkdocs.yml
        self.create_test_mkdocs_config()
        
        # Initialize plugin
        self.plugin = DrawioConverterPlugin()
        
    def create_test_drawio_file(self):
        """Create a simple test drawio file"""
        drawio_path = os.path.join(self.docs_dir, 'diagrams', 'vector', 'catalogue.drawio')
        with open(drawio_path, 'w') as f:
            f.write('''<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net" modified="2023-12-18T12:00:00.000Z">
    <diagram id="test" name="Page-1">
        <mxGraphModel><root><mxCell id="0"/></root></mxGraphModel>
    </diagram>
</mxfile>''')

    def create_test_markdown_file(self):
        """Create test markdown file with drawio references"""
        md_content = """# Lead to Order
 
## 1 Introduction
 
This use case demonstrates a Sales Lead and Opportunity Capture process.
 
[catalogue.drawio]
 
![Page 1](diagrams/vector/catalogue.drawio#0)
"""
        with open(os.path.join(self.docs_dir, 'test.md'), 'w') as f:
            f.write(md_content)

    def create_test_mkdocs_config(self):
        """Create test mkdocs.yml configuration"""
        config = {
            'site_name': 'Test Site',
            'docs_dir': self.docs_dir,
            'site_dir': self.site_dir,
            'plugins': [{
                'drawio-converter': {
                    'cache_dir': self.cache_dir,
                    'format': 'svg'
                }
            }]
        }
        with open(os.path.join(self.test_dir, 'mkdocs.yml'), 'w') as f:
            yaml.dump(config, f)

    def convert_with_docker(self, input_path, output_path):
        """Convert drawio to svg using Docker"""
        try:
            cmd = [
                'docker', 'run', '--rm',
                '-v', f'{os.path.dirname(input_path)}:/data',
                'rlespinasse/drawio-export',
                '-f', 'svg',
                '-i', os.path.basename(input_path),
                '-o', os.path.basename(output_path)
            ]
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Docker conversion failed: {e}")
            return False

    def test_markdown_processing(self):
        """Test markdown processing functionality"""
        # Load test markdown
        with open(os.path.join(self.docs_dir, 'test.md'), 'r') as f:
            markdown_content = f.read()
        
        # Process markdown with plugin
        config = load_config(os.path.join(self.test_dir, 'mkdocs.yml'))
        self.plugin.on_config(config)
        
        processed_content = self.plugin.on_page_markdown(
            markdown_content,
            config['pages'][0] if 'pages' in config else None
        )
        
        # Verify references were processed
        self.assertIn('.svg', processed_content)
        self.assertNotIn('.drawio#0', processed_content)

    def test_file_conversion(self):
        """Test drawio to svg conversion"""
        input_file = os.path.join(self.docs_dir, 'diagrams', 'vector', 'catalogue.drawio')
        output_file = os.path.join(self.site_dir, 'diagrams', 'vector', 'catalogue-0.svg')
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Convert using Docker
        success = self.convert_with_docker(input_file, output_file)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(output_file))

    def test_full_pipeline(self):
        """Test the entire plugin pipeline"""
        # Load config
        config = load_config(os.path.join(self.test_dir, 'mkdocs.yml'))
        
        # Initialize plugin
        self.plugin.on_config(config)
        
        # Process markdown
        with open(os.path.join(self.docs_dir, 'test.md'), 'r') as f:
            markdown_content = f.read()
        
        processed_content = self.plugin.on_page_markdown(
            markdown_content,
            config['pages'][0] if 'pages' in config else None
        )
        
        # Run post-build processing
        self.plugin.on_post_build(config)
        
        # Verify outputs
        expected_svg = os.path.join(self.site_dir, 'diagrams', 'vector', 'catalogue-0.svg')
        self.assertTrue(os.path.exists(expected_svg))

    def tearDown(self):
        """Clean up temporary test directories"""
        shutil.rmtree(self.test_dir)

def main():
    """Main test runner"""
    print("Running MkDocs Drawio Converter Plugin Tests")
    print("===========================================")
    print(f"Current directory: {os.getcwd()}")
    
    # Run tests
    unittest.main(argv=[''], verbosity=2, exit=False)

if __name__ == '__main__':
    main()