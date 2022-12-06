# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ColonyCatalogues(models.Model):
    _name = "colony.catalogues"
    _description = "colony.catalogues"

    name = fields.Char(string="Colony name")#Nombre de colonia
    country_id = fields.Many2one("res.country", string="Country")
    state_id = fields.Many2one("res.country.state", string="State")
    city_id = fields.Many2one("res.city", string="city")
    zip = fields.Char(string="C.P.")