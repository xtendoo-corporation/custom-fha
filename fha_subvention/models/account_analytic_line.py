# Copyright 2021 Xtendoo Corporation
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html

from odoo import api, fields, models, _


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    move_id = fields.Many2one('account.move.line', string='Journal Item', ondelete='cascade', index=True,
                              check_company=True)

    group_id = fields.Many2one('account.analytic.group', related='account_id.group_id', store=True, readonly=True,
                               compute_sudo=True)

    move_move_id = fields.Many2one(
        related='move_id.move_id',
        string='Invoice Number',
        readonly=True,
    )
    abs_amount = fields.Monetary(
        string='Absolute Amount',
        compute='_compute_amount',
        store=True,
    )
    subvention = fields.Boolean(
        string="Subvention Deprecated",
        default=False,
    )
    is_subvention = fields.Boolean(
        string='Is Subvention',
        related='group_id.subvention',
    )
    account_id = fields.Many2one(
        'account.analytic.account',
        'Subvention',
        required=False,
        ondelete='restrict',
        index=True,
        domain="[('is_subvention', '=', True), '|', ('company_id', '=', False), ('company_id', '=', company_id)]",
    )
    justified_percentage = fields.Float(
        related='account_id.percentage',
        digits=(16, 2),
        default=0.0,
    )
    justified_amount = fields.Monetary(
        string='Justified Amount',
        help='The justified amount.',
        currency_field='currency_id',
        store=True,
        compute='_compute_justified_amount',
    )

    @api.model
    def create(self, vals):
        if not vals.get('move_id'):
            if vals.get('move_line_id'):
                vals['move_id'] = vals['move_line_id']
        record = super().create(vals)
        return record

    @api.model
    def init(self):
        print("*" * 50)
        print("ENTRA EN INIT")
        # Inicializar la variable para contar los registros sin asignar move_id
        no_move_id = 0

        # Filtrar los registros específicos
        record_ids = self.env['account.analytic.line'].search([])

        for record in record_ids:
            if not record.move_id:
                print(f"NO TIENE MOVE_ID: {record.name}")

                # Buscar líneas de movimientos con misma descripción y fecha
                account_move_line_ids = self.env['account.move.line'].search([
                    ('name', '=', record.name),
                    ('date', '=', record.date),
                ])

                print(f"account_move_line_ids encontrados: {account_move_line_ids}")

                assigned = False  # Bandera para verificar si se asignó un move_id

                if len(account_move_line_ids) == 1:
                    # Si solo hay una coincidencia, asignar directamente
                    print("Solo 1 coincidencia, se asigna.")
                    record.move_id = account_move_line_ids[0].id
                    assigned = True
                else:
                    print("Más de 1 coincidencia.")
                    for account_move_line_id in account_move_line_ids:
                        # Verificar si ya está asignado en algún registro
                        is_in_move_id = any(
                            analytic_record.move_id.id == account_move_line_id.id
                            for analytic_record in record_ids
                        )
                        if not is_in_move_id:
                            print(f"Asignando {account_move_line_id.id} a {record.id}")
                            record.move_id = account_move_line_id.id
                            assigned = True
                            break  # Salir del bucle al encontrar una coincidencia libre
                        else:
                            print(f"{account_move_line_id.id} ya está ocupado.")

                # Incrementar el contador si no se asignó ningún move_id
                if not assigned:
                    no_move_id += 1

        print(f"Total registros sin asignar move_id: {no_move_id}")
        print("*" * 50)

    @api.depends('amount')
    def _compute_amount(self):
        for record in self:
            record.abs_amount = abs(record.amount)

    @api.depends('amount', 'justified_percentage')
    def _compute_justified_amount(self):
        self.justified_amount = 0
        for record in self.filtered(lambda r: r.amount != 0):
            record.justified_amount = abs(record.amount) * record.justified_percentage / 100
