# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.modules.product.product import STATES, DEPENDS

__all__ = ['Configuration', 'Template']
__metaclass__ = PoolMeta


class Configuration:
    __name__ = 'product.configuration'
    end_of_life_template = fields.Many2One('electronic.mail.template',
        'End of life notify template')


class Template:
    __name__ = 'product.template'

    end_of_life = fields.Date('End of life', states=STATES,
        depends=DEPENDS)

    @classmethod
    def notify_end_of_life(cls, products, trigger):
        pool = Pool()
        Config = pool.get('product.configuration')
        Template = pool.get('electronic.mail.template')

        config = Config.get_singleton()
        if config and config.end_of_life_template:
            template = config.end_of_life_template.id
            for product in products:
                records = product._get_notify_end_of_life_records()
                Template.render_and_send(template, records)

    def _get_notify_end_of_life_records(self):
        pool = Pool()
        try:
            SaleLine = pool.get('sale.line')
        except KeyError:
            return [self]

        return SaleLine.search([
                ('sale.state', 'in', ['quotation', 'confirmed']),
                ('product.template', '=', self.id),
                ])
