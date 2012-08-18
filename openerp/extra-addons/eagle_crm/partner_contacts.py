# -*- coding: utf-8 -*-##  File: partner_contact.py#  Module: eagle_crm##  Created by sbe@open-net.ch##  Copyright (c) 2011 Open-Net Ltd. All rights reserved.###############################################################################	#	OpenERP, Open Source Management Solution#	Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).##	This program is free software: you can redistribute it and/or modify#	it under the terms of the GNU Affero General Public License as#	published by the Free Software Foundation, either version 3 of the#	License, or (at your option) any later version.##	This program is distributed in the hope that it will be useful,#	but WITHOUT ANY WARRANTY; without even the implied warranty of#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the#	GNU Affero General Public License for more details.##	You should have received a copy of the GNU Affero General Public License#	along with this program.  If not, see <http://www.gnu.org/licenses/>.	 ###############################################################################from osv import osv,fieldsclass res_partner_contact(osv.osv):    """ Inherits partner and adds CRM information in the partner form """    _inherit = 'res.partner.contact'    _columns = {        'mailing': fields.boolean('Mailing', required=False),		'lead': fields.one2many('crm.lead', 'sel_contact_id', 'Leads', domain=[('type','=','lead')] ),		'meetings': fields.one2many('crm.meeting', 'contact_id', 'Meeting'),		'phonecalls': fields.one2many('crm.phonecall', 'partner_addr_contact', 'Phone Call'),	}res_partner_contact()