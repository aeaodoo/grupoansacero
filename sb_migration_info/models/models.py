# -*- coding: utf-8 -*-
import tempfile
import binascii
import base64
import xlrd
import io
from io import StringIO
import os
from os.path import splitext
import csv
from odoo.exceptions import Warning
from odoo import models, fields, _, api, SUPERUSER_ID, registry
import logging
from ..helpers import utilities
from datetime import date

_logger = logging.getLogger(__name__)


class ResPartnerInfoImportWizard(models.TransientModel):
    _name = 'import.partner.info'
    _description = 'import.partner.info'
   
    option = fields.Selection([('csv', 'CSV')], default='csv', string="Import File Type")
    file = fields.Binary(string="Archivo", required=True)
   
    def import_file_csv_xlsx(self):
        """ Function to import product or update from csv or xlsx file """
        
        row_size = 500
        warn_msg = ''
        #Read file type .csv
        if self.option == 'csv':
            try:
                csv_data = base64.b64decode(self.file)
                data_file = io.StringIO(csv_data.decode("utf-8"))
                data_file.seek(0)
                file_reader = []
                csv_reader = csv.reader(data_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                file_reader.extend(csv_reader)
            except:
                raise Warning(_("El archivo no es de tipo '%s'" % self.option))


            number_lines = sum(1 for row in file_reader)
            if number_lines > row_size:
                #Split file 
                res = self.split_xlsx_or_csv(self.option, self.file, row_size)
                print("Aquí todo bien= ", res)
                warn_msg = _("El archivo contiene %s registros. \nSe crearon %s archivos con %s registros en cada archivo. \nEl CRON se encargará de procesar de forma automática.") % (
                                number_lines,
                                len(res),
                                row_size
                )
                
                if warn_msg:
                    message_id = self.env['migration.message.wizard'].create({'message': warn_msg})
                    return {
                        'name': 'Message',
                        'type': 'ir.actions.act_window',
                        'view_mode': 'form',
                        'res_model': 'migration.message.wizard',
                        'res_id': message_id.id,
                        'target': 'new'
                    }    
            else:
                if file_reader:
                    res = self.update_seller_price_in_product(file_reader)
                    
                    if not warn_msg:
                        message_id = self.env['migration.message.wizard'].create({'message': 'Se actualizó/importó de forma exitosa.'})
                        return {
                            'name': 'Message',
                            'type': 'ir.actions.act_window',
                            'view_mode': 'form',
                            'res_model': 'migration.message.wizard',
                            'res_id': message_id.id,
                            'target': 'new'
                        }
        else:
            raise Warning(_("Por favor selecciona un archivo con formato .csv"))
        
        return res

    @api.returns("ir.attachment")
    def _create_csv_attachment(self, f, file_name):
        encoding = "utf-8"
        datas = base64.encodebytes(f.getvalue().encode(encoding))
        attachment = self.env["ir.attachment"].create(
            {
                "name": file_name, 
                "res_model": self._name, 
                'res_id': self.id,
                'mimetype': 'application/csv',
                "type": "binary", 
                "datas": datas, 
                "state": "processing"
            }
        )
        
        print("ID attachment= ", attachment)
        return attachment
    

    def split_xlsx_or_csv(self, type_file, file, size_row):
        """
        Función para trozar el excel en batch
        """
        
        if type_file == 'csv':
            fields, data = utilities._read_csv_attachment(file)
            file_name="Lote.csv"
            root, ext = splitext(file_name)
            header = fields
            rows = [row for row in data]
            pages = []
            allAttachment = []
            
            row_count = len(rows)
            start_index = 0
            
            while start_index < row_count:
                pages.append(rows[start_index: start_index+size_row])
                start_index += size_row
            
            for i, page in enumerate(pages):
                # print("Página =", i)
                f = StringIO()
                writer = csv.writer(f, delimiter=',', quotechar='"')
                writer.writerow(header)
                for row in page:
                    writer.writerow(row)
                attachment = self._create_csv_attachment(f, file_name=root + "_" + str(i+1) + ext)
                allAttachment.append(attachment.id)
                
        return allAttachment
    
        
    def update_seller_price_in_product(self, values,):
        line_count = 0
        for row in values:
            if line_count == 0:
                line_count += 1
            else:
                name = row[2].strip()
                street_name = row[4].strip()
                search_colony = None
                category_ids = None
                
                ##########Buscar colonia
                if row[8]:
                    city_id_name = row[8].strip()
                    split_city_name = city_id_name.split(", ")
                    # print("Split city name= ", split_city_name)
                    #Buscar colonia 
                    search_colony = self.env['colony.catalogues'].search_read([('name', 'ilike', split_city_name[0]), ('zip','=', row[11])], ['name','zip','city_id','state_id','country_id'])
                # print("Información de la colonia=", search_colony)
                
                ##########Buscar categoría
                if row[13]:
                    format_category_ids = ["{}".format(item) for item in row[13].split(', ')]
                    category_ids = self.env['res.partner.category'].search([('name', 'in', format_category_ids)]).ids
                #print("Información de las categorías= ", category_ids)
                
                ###########Buscar cliente/proveedor
                search_partner = self.env['res.partner'].search([('name', '=', name)], limit=1) 
                # print("search_partner: ", search_partner)
               
                if not search_partner:
                    info_partner = {
                        'id': row[0],
                        'company_type': row[1],
                        'name': name,
                        'street_name': street_name if street_name else '',
                        'street_number': row[5] if row[5] != 'FALSE'else '',
                        'street_number2': row[6] if row[6] != 'FALSE' else '',
                        'l10n_mx_edi_colony': search_colony[0]['id'] if search_colony else None,
                        'city_id': search_colony[0]['city_id'][0] if search_colony else None,
                        'state_id': search_colony[0]['state_id'][0] if search_colony else None,
                        'zip': row[11] if row[11] else '',
                        'country_id': search_colony[0]['country_id'][0] if search_colony else 156,
                        'vat': row[3] if row[3] != 'FALSE' else 'XAXX010101000',#"MX"+row[3] if row[3] != 'FALSE' else '',
                        'How_do_you_know_us': row[14] if row[14] != 'Otro' and row[14] != 'FALSE' else None,
                        'code_plus': row[15] if row[15] != 'FALSE' else '',
                        'phone': row[16] if row[16] != 'FALSE' else '',
                        'mobile': row[17] if row[17] != 'FALSE' else '',
                        'email': row[18] if row[18] != 'FALSE' else '',
                        'lang': row[19] if row[19] else None,
                        'category_id': category_ids if category_ids else None,
                        'purchasing_manager': self.env['res.partner'].search([('name', '=', row[20])]).id if row[20] else None,
                        'customer_rank': 1 if row[22] == 'TRUE' else 0,
                        'supplier_rank': 1 if row[23] == 'TRUE' else 0,
                        'user_id': self.env['res.users'].search([('name', '=', row[25])]).id if row[25] else None,
                        # 'team_id': self.env['crm.team'].search([('name', '=', row[25])]).id if row[25] else None, 
                        'property_payment_term_id': self.env['account.payment.term'].search([('name', '=', row[33])]).id if row[33] else None,
                        'property_product_pricelist': self.env['product.pricelist'].search([('name', '=', row[29])]).id if row[29] else None,
                        'property_account_position_id': self.env['account.fiscal.position'].search([('name', '=', row[39])]).id if row[39] else None,
                        'property_supplier_payment_term_id': self.env['account.payment.term'].search([('name', '=', row[38])]).id if row[38] else None,
                        'ref': row[30] if row[30] != 'FALSE' else '',
                        'industry_id': self.env['res.partner.industry'].search([('name', '=', row[31])]).id if row[31] else None,
                        'trust': row[34] if row[34] else None,
                        'credit_limit': float(row[36]),
                    }
                    #print("Crear partner= ", info_partner)
                    self.env['res.partner'].sudo().create(info_partner)
                else:
                    print("Actualizar partner= ", search_partner)
                    search_partner.sudo().write({
                        'company_type': row[1],
                        'name': name,
                        'street_name': street_name if street_name else '',
                        'street_number': row[5] if row[5] != 'FALSE'else '',
                        'street_number2': row[6] if row[6] != 'FALSE' else '',
                        'l10n_mx_edi_colony': search_colony[0]['id'] if search_colony else None,
                        'city_id': search_colony[0]['city_id'][0] if search_colony else None,
                        'state_id': search_colony[0]['state_id'][0] if search_colony else None,
                        'zip': row[11] if row[11] else '',
                        'country_id': search_colony[0]['country_id'][0] if search_colony else 156,
                        'vat': row[3] if row[3] != 'FALSE' else 'XAXX010101000',#"MX"+row[3] if row[3] != 'FALSE' else '',
                        'How_do_you_know_us': row[14] if row[14] != 'Otro' and row[14] != 'FALSE' else None,
                        'code_plus': row[15] if row[15] != 'FALSE' else '',
                        'phone': row[16] if row[16] != 'FALSE' else '',
                        'mobile': row[17] if row[17] != 'FALSE' else '',
                        'email': row[18] if row[18] != 'FALSE' else '',
                        'lang': row[19] if row[19] else None,
                        'category_id': category_ids if category_ids else None,
                        'purchasing_manager': self.env['res.partner'].search([('name', '=', row[20])]).id if row[20] else None,
                        'customer_rank': 1 if row[22] == 'TRUE' else 0,
                        'supplier_rank': 1 if row[23] == 'TRUE' else 0,
                        'user_id': self.env['res.users'].search([('name', '=', row[25])]).id if row[25] else None,
                        # 'team_id': self.env['crm.team'].search([('name', '=', row[25])]).id if row[25] else None, 
                        'property_payment_term_id': self.env['account.payment.term'].search([('name', '=', row[33])]).id if row[33] else None,
                        'property_product_pricelist': self.env['product.pricelist'].search([('name', '=', row[29])]).id if row[29] else None,
                        'property_account_position_id': self.env['account.fiscal.position'].search([('name', '=', row[39])]).id if row[39] else None,
                        'property_supplier_payment_term_id': self.env['account.payment.term'].search([('name', '=', row[38])]).id if row[38] else None,
                        'ref': row[30] if row[30] != 'FALSE' else '',
                        'industry_id': self.env['res.partner.industry'].search([('name', '=', row[31])]).id if row[31] else None,
                        'trust': row[34] if row[34] else None,
                        'credit_limit': float(row[36]),
                    })
                
        return {}

