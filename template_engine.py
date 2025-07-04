"""
Fastie Template Engine - Mako wrapper for code generation
"""

from mako.template import Template
from mako.lookup import TemplateLookup
from mako.exceptions import RichTraceback
from pathlib import Path
from typing import Dict, Any
import click


class FastieTemplateEngine:
    """Template engine wrapper for Fastie CLI using Mako templates"""
    
    def __init__(self):
        """Initialize the template engine with proper lookup directories"""
        self.templates_dir = Path(__file__).parent / 'templates'
        
        # Ensure templates directory exists
        if not self.templates_dir.exists():
            self.templates_dir.mkdir(parents=True, exist_ok=True)
            
        self.lookup = TemplateLookup(
            directories=[str(self.templates_dir)],
            module_directory='/tmp/mako_modules',
            strict_undefined=True,
            input_encoding='utf-8',
            output_encoding=None  # Return Unicode strings, not bytes
        )
    
    def render(self, template_name: str, **context) -> str:
        """
        Render a template with given context
        
        Args:
            template_name: Path to template file relative to templates directory
            **context: Template variables
            
        Returns:
            Rendered template content
        """
        try:
            template = self.lookup.get_template(template_name)
            return template.render(**context).strip()
        except Exception as e:
            self._handle_template_error(template_name, e)
            raise
    
    def _handle_template_error(self, template_name: str, error: Exception):
        """Handle template rendering errors with helpful debugging info"""
        click.echo(f"❌ Template error in {template_name}:")
        click.echo(f"   {str(error)}")
        
        # Show Mako traceback if available
        if hasattr(error, 'source') or 'mako' in str(error).lower():
            try:
                traceback = RichTraceback()
                for (filename, lineno, function, line) in traceback.traceback:
                    click.echo(f"   File {filename}, line {lineno}, in {function}")
                    click.echo(f"     {line}")
                click.echo(f"   {traceback.error}")
            except:
                pass  # Fallback to basic error message
    
    def template_exists(self, template_name: str) -> bool:
        """Check if a template file exists"""
        return (self.templates_dir / template_name).exists()
    
    def list_templates(self, directory: str = None) -> list:
        """List available templates in a directory"""
        search_dir = self.templates_dir
        if directory:
            search_dir = search_dir / directory
            
        if not search_dir.exists():
            return []
            
        return [f.name for f in search_dir.glob('*.mako')]


# Global template engine instance
template_engine = FastieTemplateEngine()


def render_template(template_name: str, **context) -> str:
    """Convenience function to render templates"""
    return template_engine.render(template_name, **context)


def get_template_helpers():
    """Common template helper functions"""
    return {
        'to_class_name': lambda name: ''.join(word.capitalize() for word in name.lower().replace('-', '_').split('_')),
        'to_snake_case': lambda name: name.lower().replace('-', '_'),
        'to_title_case': lambda name: name.replace('_', ' ').replace('-', ' ').title(),
        'to_plural': lambda name: f"{name}s" if not name.endswith('s') else name,
        'to_table_name': lambda name: f"{name.lower().replace('-', '_')}s"
    } 