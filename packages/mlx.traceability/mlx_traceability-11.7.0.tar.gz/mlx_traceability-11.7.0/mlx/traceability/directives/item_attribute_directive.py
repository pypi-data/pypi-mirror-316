"""Module for the item-attribute directive"""
from docutils import nodes

from ..traceability_exception import report_warning
from ..traceable_attribute import TraceableAttribute
from ..traceable_base_directive import TraceableBaseDirective
from ..traceable_base_node import TraceableBaseNode
from ..traceable_item import TraceableItem


class ItemAttribute(TraceableBaseNode):
    '''Attribute to documentation item'''

    def perform_replacement(self, app, collection):
        """
        Perform the node replacement
        Args:
            app: Sphinx application object to use.
            collection (TraceableCollection): Collection for which to generate the nodes.
        """
        if self['id'] in TraceableItem.defined_attributes:
            attr = TraceableItem.defined_attributes[self['id']]
            header = attr.name
            if attr.caption:
                header += ': ' + attr.caption
        else:
            header = self['id']
        top_node = self.create_top_node(header)
        self.replace_self(top_node)


class ItemAttributeDirective(TraceableBaseDirective):
    """
    Directive to declare attribute for items

    Syntax::

      .. item-attribute:: attribute_id [attribute_caption]

         [attribute_content]

    """
    # Required argument: id
    required_arguments = 1
    # Optional argument: caption (whitespace allowed)
    optional_arguments = 1
    # Content allowed
    has_content = True

    def run(self):
        """ Processes the contents of the directive. """
        env = self.state.document.settings.env

        # Convert to lower-case as sphinx only allows lowercase arguments (attribute to item directive)
        attribute_id = self.arguments[0]
        attribute_node = ItemAttribute('')
        attribute_node['document'] = env.docname
        attribute_node['line'] = self.lineno

        stored_id = TraceableAttribute.to_id(attribute_id)
        target_node = nodes.target('', '', ids=[stored_id])
        if stored_id not in TraceableItem.defined_attributes:
            report_warning('Found attribute description which is not defined in configuration ({})'
                           .format(attribute_id),
                           env.docname,
                           self.lineno)
            attribute_node['id'] = stored_id
        else:
            attr = TraceableItem.defined_attributes[stored_id]
            attr.caption = self.caption
            attr.set_location(env.docname, self.lineno)
            attribute_node['id'] = attr.identifier

        # Output content of attribute to document
        template = []
        for line in self.content:
            template.append('    ' + line)
        self.state_machine.insert_input(template, self.state_machine.document.attributes['source'])

        return [target_node, attribute_node]
