cd
pwd
bzr branch --stacked lp:openobject-server/6.0 server
bzr branch --stacked lp:openobject-addons/6.0 addons
bzr branch --stacked lp:openobject-addons/extra-6.0 extra-addons
bzr branch --stacked lp:openobject-client-web/6.0 web
bzr branch lp:openerp.pt-br-localiz l10n_br
cd addons/
ll
ls
rm -rf l10b_br
ls ..
ln -s ../extra-addons/account_fiscal_position_rule
ln -s ../extra-addons/account_fiscal_position_rule_purchase
ln -s ../extra-addons/account_fiscal_position_rule_stock
ln -s ../extra-addons/account_fiscal_position_rule_sale
ln -s ../extra-addons/account_product_fiscal_classification
ln -s ../l10n_br/l10n_br$ ln -s ../l10n_br/l10n_br_account
ln -s ../l10n_br/l10n_br_base
ln -s ../l10n_br/l10n_br_data_account
ln -s ../l10n_br/l10n_br_data_base
ln -s ../l10n_br/l10n_br_data_cep
ln -s ../l10n_br/l10n_br_delivery
ln -s ../l10n_br/l10n_br_fp_rule_sale_link
ln -s ../l10n_br/l10n_br_product
ln -s ../l10n_br/l10n_br_purchase
ln -s ../l10n_br/l10n_br_sale
ln -s ../l10n_br/l10n_br_stock
ll
ls 
cd ..
ll
ls
ls -la
cp /opt/openerp/server/debian/openerp-server.init /opt/openerp
cp /opt/openerp/server/doc/openerp-server.conf /opt/openerp
sudo gedit openerp-server.init 
ll
ls -la
gedit openerp-server.init 
vi openerp-server.init 
sudo
vi openerp-server.conf 
exit
cd
pwd

ll
ls
ls -la
ls -s /opt/openerp/extra-addons/ /opt/openerp/extra-adons
ln -s /opt/openerp/extra-addons/ /opt/openerp/extra-adons
ll
ls -la
exit
