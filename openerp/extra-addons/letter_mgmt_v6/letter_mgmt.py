# -*- encoding: utf-8 -*-
##############################################################################
#
#    Parthiv Pate, Tech Receptives, Open Source For Ideas    
#    Copyright (C) 2009-Today Tech Receptives(http://techreceptives.com).
#    All Rights Reserved
#    
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from osv import osv
from osv import fields
import time
from tools.translate import _

class letter_type(osv.osv):
    """Class to define various types for letters like : envelope,parcel, etc."""
    
    _name = 'letter.type'
    
    _description = "types for letters like : envelope,parcel, etc."

    _columns = {
                'name':fields.char('Type',size=32,required=True),
                'code':fields.char('Code',size=8,required=True),
                'active':fields.boolean('Active'),
                }
    
    _defaults = {  
                 'active': lambda *a: 1,  
                 }
    
    _sql_constraints = [('code_uniq', 'unique(code)', 'Code must be unique !')]
     
letter_type()

class letter_class(osv.osv):
    """ Class to define the classification of letter like : classified, confidential, personal, etc. """ 
    
    _name = 'letter.class'
    
    _description = "letter like : classified, confidential, personal, etc."

    _columns = {
                'name':fields.char('Type',size=32,required=True),
                'active':fields.boolean('Active'),
                }
    
    _defaults = {  
                 'active': lambda *a: 1,  
                 }
    
letter_class()

class letter_channel(osv.osv):
    """ Class to define various channels using which letters can be sent or received like : post, fax, email. """

    _name = 'letter.channel'
    
    _description = "channels using which letters can be sent/received like:post,fax"

    _columns = {
                'name':fields.char('Type',size=32,required=True),
                'active':fields.boolean('Active'),
                }

    _defaults = {  
                'active': lambda *a: 1,  
                }
    
letter_channel()

def _links_get(self, cr, uid, context={}):
    obj = self.pool.get('res.request.link')
    ids = obj.search(cr, uid, [])
    res = obj.read(cr, uid, ids, ['object', 'name'], context)
    return [(r['object'], r['name']) for r in res]

class res_letter(osv.osv):
    """A register class to log all movements regarding letters"""
    
    _name = 'res.letter'
    
    _description = "A Register class to log all movements regarding letters"
    
    def _get_number(self, cr, uid, context):
        
        if context is None:
            context = {}
        move = context.get('move', 'in')
        if move == 'in':
            res = self.pool.get('ir.sequence').get(cr, uid, 'in.letter')
        else:
            res = self.pool.get('ir.sequence').get(cr, uid,'out.letter')
            
        return res
    
    
    
    _columns = {
                'name':fields.char('Subject',size=128,help="Subject of letter"),
                'number':fields.char('Number',size=32,help="Autogenerated Number of letter",required=True),
                'move':fields.selection([('in','IN'),('out','OUT')],'Move',readonly=True,help="Incoming or Outgoing Letter"),
                'type':fields.many2one('letter.type','Type',help="Type of Letter, Depeding upon size",required=True),
                'class':fields.many2one('letter.class','Class',help="Classification of Document",required=True),
                'date':fields.datetime('Sent / Received Date',required=True),
                'partner_id':fields.many2one('res.partner','Partner'),
                'address_id':fields.many2one('res.partner.address','Address'),
                'int_ref' : fields.reference('Reference', selection=_links_get, size=128),
                'int_ref2' : fields.reference('Reference 2', selection=_links_get, size=128),
                'user_id':fields.many2one('res.users',"Dispatcher",required=True),
                'snd_rec_id':fields.many2one('res.users',"Sender / Receiver"),
                'note':fields.text('Note'),
                'state':fields.selection([('draft','Draft'),('rec','Received'),('sent','Sent'),('rec_bad','Received Damage'),('rec_ret','Received But Returned'),('cancel','Cancelled')],'State',readonly=True),
                'parent_id':fields.many2one('res.letter','Parent'),
                'child_line':fields.one2many('res.letter','parent_id','Letter Lines'),
                'active':fields.boolean('Active'),
                'channel_id':fields.many2one('letter.channel','Sent / Receive Source'),
                'company_id':fields.many2one('res.company','Company',required=True),
                'history_line':fields.one2many('letter.history','register_id','History'),
                'ref_data':fields.char('Reference Number',size=32,help="Reference Number Provided by postal provider."),
                'weight':fields.float('Weight (in KG)'),
                'size':fields.char('Size',size=64),
                }
    
    _defaults = {
                'number': _get_number,
                'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
                'user_id':lambda self, cr, uid, context: uid,
                'move':lambda self, cr, uid, context: context.get('move','in'),
                'state': lambda *a: 'draft',
                'active':lambda *a: 1,
                'company_id': lambda self,cr,uid,c: self.pool.get('res.company')._company_default_get(cr, uid, 'res.letter', context=c),
                }
    
    def history(self,cr,uid,ids,context={},keyword=False):
        lh_pool = self.pool.get('letter.history')
        for id in ids:
            lh_pool.create(cr,uid,{'name':keyword,'user_id':uid,'register_id':id})
        return True
    
    def action_received(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'rec'})
        self.history(cr, uid, ids, context={'translated_keyword':_('Received')}, keyword=_('Received'))
        return True
    def action_cancel(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'cancel'})
        self.history(cr, uid, ids, context={'translated_keyword':_('Cancel')}, keyword=_('Cancel'))
        return True
    
    def action_sent(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'sent'})
        self.history(cr, uid, ids, context={'translated_keyword':_('Sent')}, keyword=_('Sent'))
        return True
    
    def action_rec_ret(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'rec_ret'})
        self.history(cr, uid, ids, context={'translated_keyword':_('Received But Returned')}, keyword=_('Received But Returned'))
        return True
    
    def action_rec_bad(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'rec_bad'})
        self.history(cr, uid, ids, context={'translated_keyword':_('Received Damage')}, keyword=_('Received Damage'))
        return True
    
    def action_set_draft(self,cr,uid,ids,context={}):
        self.write(cr,uid,ids,{'state':'draft'})
        self.history(cr, uid, ids, context={'translated_keyword':_('Set To Draft')}, keyword=_('Set To Draft'))
        return True
    
res_letter()



class letter_history(osv.osv):
    _name = "letter.history"
    _description = "Letter Communication History"
    _order = "id desc"
    
    _columns = {
        'register_id':fields.many2one('res.letter','Register'),
        'name': fields.char('Action', size=64),
        'date': fields.datetime('Date'),
        'user_id': fields.many2one('res.users', 'User Responsible', readonly=True),
    }
    _defaults = {
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
letter_history()