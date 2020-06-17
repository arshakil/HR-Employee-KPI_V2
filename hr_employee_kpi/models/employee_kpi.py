# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime
class Employee_kpi(models.Model):
    _name = 'hr.employee.kpi'
    _description = 'Employee KPI'
    _rec_name = "employee_id"
    _order = "id asc"


    employee_id = fields.Many2one('hr.employee', string='Employee', required="1")
    # job_title = fields.Many2one('hr.job', string='Job Title',required="1")
    job_title = fields.Char(related="employee_id.job_id.name", string='Job Title',readonly="1")

    department = fields.Char(related="employee_id.department_id.name", string='Department',readonly="1")
    # year = fields.Date(string="Year",required="1")
    valid_from = fields.Date(string="Valid From",required="1")
    valid_to = fields.Date(string="Valid To",required="1")
    employee_kpi_lines = fields.One2many('employee_kpi.lines', 'employee_kpi_id', string='Employee KPI Lines',store=True)

    kpi_val_total = fields.Float(string="Total", readonly="1",compute='_total_kpi_value')

    total_weight = fields.Float(string="Total weight")



    state = fields.Selection([
        ('draft', "Draft"),
        ('approved', "Approved"),
        ('refuse', "Refuse"),], string="Status", default='draft')

    def action_approved(self):
        self.state = "approved"
    def action_refuse(self):
        self.state = "refuse"

    def action_cancel(self):
        self.state = "draft"




    # Calculate Total of KPI Values
    @api.depends('employee_kpi_lines.kpi_value')
    def _total_kpi_value(self):
        # print ('total is Called')
        total = 0.0;
        t_weight = 0.0;
        for rec in self:
            for kpi_value_total in self.employee_kpi_lines:
                # if kpi_value_total.employee_kpi_lines.kpi_value > 0:
                # print ('kpi_value_total kpi_value',kpi_value_total)

                # total=total+kpi_value_total.kpi_value
                # print ('kpi_value Total',total)

                # extra for getting total
                total=total+kpi_value_total.set_kpi_value
                # print ('set_kpi_value Total', total)

                t_weight = t_weight + kpi_value_total.weight


        # print ('weight_total Total', t_weight)
        #
        # if t_weight>100:
        #     raise ValidationError(_('You can\'t set total weight more then 100'))
        rec.total_weight = t_weight

        rec.kpi_val_total=total


    # changing kpi dynamically
    # @api.onchange('job_title')
    # @api.depends('job_title',)
    @api.onchange('employee_id')
    def _LoadedAllKPI(self):
        employee_id = self.env['hr.employee'].search([('id', '=', self.employee_id.id)])
        # print ('employee_id',employee_id)
        if employee_id:
            kpi_lines=[]
            job_title_ids = self.env['employee_kpi.assign'].search([('job_title.id', '=', employee_id.job_id.id)])
            if job_title_ids:
                # print('bundle_product_ids',job_title_ids)
                for kpi in job_title_ids:
                    # print('kpi_title', str(kpi.kpi_title))
                    line = (0,0,{
                        'kpi_title':kpi.id
                    })
                    kpi_lines.append(line)
                    # print("employee_kpi_lines",kpi_lines)
                self.employee_kpi_lines=kpi_lines


    @api.model
    def create(self, vals):
        result = super(Employee_kpi, self).create(vals)
        print ('total_weight',result.total_weight)

        # validation check for Total Weight
        if result.total_weight>100.0:
            raise ValidationError(_('You can\'t set total weight more then 100, Please Change Your Weight'))
        # validation check for Employee KPI Lines
        if not result.employee_kpi_lines:
            raise ValidationError(_('You can\'t Create because employee doesn\'t have Job title !!, OR Please create KPI first for this job title'))

        # validation check for date
        if result.valid_from and result.valid_to:
            valid_from = datetime.strptime(vals['valid_from'], '%Y-%m-%d')
            valid_to = datetime.strptime(vals['valid_to'], '%Y-%m-%d')
            total_days = valid_to - valid_from
            days_is = int(total_days.days)+1
            if days_is < 1:
                raise ValidationError("You can\'t select that date!!, You have selected: %s" % total_days.days + " days"+" and Please check your Valid To field")
        return result


    @api.multi
    def write(self, vals):
        res = super(Employee_kpi, self).write(vals)
        print ('total_weight',vals.get('total_weight'))
        # validation check for Total Weight
        if vals.get('total_weight')>100:
            raise ValidationError(_('You can\'t set total weight more then 100, Please Change Your Weight'))
        return res

    @api.multi
    def unlink(self):
        # print ('delete is called')
        for kpi in self:
           if kpi.state in ('refuse'):
              raise ValidationError(_('You cannot delete KPI which is not draft State. You should change the state from Refuse to Draft.'))
           elif kpi.state in ('approved'):
              raise ValidationError(_('You cannot delete an KPI after it has been Approved. You can set it back to "Draft" state and delete it\'s content'))
        return super(Employee_kpi, self).unlink()



class Employee_kpi_lines(models.Model):
    _name = 'employee_kpi.lines'
    _description = 'Employee KPI Lines'
    _rec_name = "kpi_title"
    _order = "id asc"


    kpi_title = fields.Many2one('employee_kpi.assign', string="KPI Title")
    # kpi_title = fields.Many2one('employee_kpi.assign', string="KPI Title", default='add_single_KPI')
    measurement = fields.Char(string="Measurement")
    target = fields.Float(string="Target", digits=(12,2))
    actual = fields.Float(string="Actual")

    achievement_rate = fields.Float(string="Achievement Rate(%)",compute='_calculate_achievement_rate', readonly="1")
    weight = fields.Float(string="Weight(%)")
    kpi_value = fields.Float(string="KPI Value", compute='_calculate_kpi_value',)

    # extra for getting total
    set_kpi_value = fields.Float(string="Set KPI Value",compute='_calculate_kpi_value',store=True)

    unit = fields.Char(string="Unit")
    employee_kpi_id = fields.Many2one('hr.employee.kpi', string='Employee KPI Assign',ondelete='cascade')

    # Calculate Achievement Rate
    @api.depends('target','actual')
    def _calculate_achievement_rate(self):
        # print ('Changing target and actual')
        for rec in self:
            if rec.target>0 and rec.actual>0:
                rec.achievement_rate=round(((rec.actual/rec.target)*100),2)

    # Calculate KPI Value
    @api.depends('achievement_rate','weight')
    def _calculate_kpi_value(self):
        # print ('Changing weight and achievement_rate')
        for rec in self:
            if rec.achievement_rate>0 and rec.weight>0:
                rec.kpi_value=round(((rec.achievement_rate*rec.weight)/100),2)
                # print ('rec.kpi_value',rec.kpi_value)
                # extra for getting total
                rec.set_kpi_value=round(((rec.achievement_rate*rec.weight)/100),2)
                # print (' rec.set_kpi_value',  rec.set_kpi_value)



    # for individual kpi change kpi_title = fields.Many2one('employee_kpi.assign', string="KPI Title", inverse='_inverse_upper_name')

    @api.onchange('kpi_title')
    def add_single_KPI(self, *args, **kwargs):
        job_title_ids = self.env['employee_kpi.assign'].search([('job_title.id', '=', self.employee_kpi_id.employee_id.job_id.id)])
        # print('bundle_product_ids',job_title_ids)
        return {'domain': {'kpi_title': [('id', 'in', job_title_ids.ids)]}}


class Employee_kpi_assign(models.Model):
    _name = 'employee_kpi.assign'
    _description = 'Employee KPI Assign'
    _rec_name = "kpi_title"
    _order = "id asc"

    job_title = fields.Many2one('hr.job', string='Job Title', required="1")
    kpi_title = fields.Char(string="KPI Title", required="1")



    @api.multi
    def unlink(self):
        job_title_id_exist = self.env['employee_kpi.lines'].search([('kpi_title.id', '=', self.id)])
        if job_title_id_exist:
            raise ValidationError(_('You cannot delete an KPI after it has been Used. You have to delete used KPI first then you can delete it.'))
        else:
            return super(Employee_kpi_assign, self).unlink()

