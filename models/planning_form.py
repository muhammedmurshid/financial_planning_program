from odoo import models, fields, _, api


class FinancialPlanningForm(models.Model):
    _name = 'financial.planning.form'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Financial Planning Program'
    _rec_name = 'display_name'

    name = fields.Char(string='Name')
    batch_id = fields.Many2one('logic.base.batch', string='Batch', requird=True, required=True)
    coordinator_id = fields.Many2one('res.users', string='Coordinator', default=lambda self: self.env.user)
    scheduled_date_one = fields.Date(string='Scheduled Dates')
    scheduled_date_two = fields.Date(string='Scheduled Date')
    state = fields.Selection(
        [('draft', 'Draft'), ('scheduled', 'Scheduled'), ('started', 'Started'), ('completed', 'Completed')],
        string='State', default='draft', tracking=True)
    photo_day_one = fields.Binary(string='Day 1')
    photo_day_two = fields.Binary(string='Day 2')
    finance_ids = fields.One2many('financial.planning.students.list', 'finance_id', string='Finance')
    finance_sec_ids = fields.One2many('second.day.planning', 'finance_sec_id', string='Finance')
    certificate_ids = fields.One2many('financial.certificate', 'certificate_id', string='Certificate')
    day_one_strength = fields.Integer(string='Day 1 Strength', compute='_compute_day_one_strength', store=1)
    day_two_strength = fields.Integer(string='Day 2 Strength', compute='_compute_day_two_strength', store=1)

    day_one_average = fields.Char(string='Day 1 Average', compute='_compute_day_one_average', store=1)
    day_two_average = fields.Char(string='Day 2 Average', compute='_compute_day_two_average', store=1)

    @api.depends('day_two_strength','batch_strength')
    def _compute_day_two_average(self):
        for rec in self:
            rec.day_two_average = str(rec.day_two_strength) + ' ' + '/' + ' ' + str(rec.batch_strength)

    @api.depends('day_one_strength', 'batch_strength')
    def _compute_day_one_average(self):
        for rec in self:
            rec.day_one_average = str(rec.day_one_strength) + ' ' + '/' + ' ' + str(rec.batch_strength)

    @api.depends('finance_ids')
    def _compute_day_one_strength(self):
        for rec in self:
            rec.day_one_strength = len(rec.finance_ids)

    @api.depends('finance_sec_ids')
    def _compute_day_two_strength(self):
        for rec in self:
            rec.day_two_strength = len(rec.finance_sec_ids)

    def action_schedule(self):
        self.state = 'scheduled'

    def _compute_display_name(self):
        for rec in self:
            rec.display_name = 'Financial Planning Program' + ' ' + rec.batch_id.name

    def action_start(self):
        students = self.env['logic.students'].search([('batch_id', '=', self.batch_id.id)])
        for i in students:
            self.certificate_ids = [(0, 0, {
                'student_id': i.id
            })]
        self.state = 'started'

    batch_strength = fields.Integer(string='Batch Strength', compute='_compute_batch_strength', store=True)

    @api.depends('batch_id')
    def _compute_batch_strength(self):
        for rec in self:
            students = self.env['logic.students'].search_count([('batch_id', '=', rec.batch_id.id)])
            print(students)
            if rec.batch_id:
                rec.batch_strength = students
            else:
                rec.batch_strength = 0

    def action_complete(self):
        for rec in self:
            student = self.env['logic.students'].search([('batch_id', '=', rec.batch_id.id)])
            for i in student:
                if rec.finance_ids:
                    for j in rec.finance_ids:
                        if j.student_id.id == i.id:
                            i.day_one_fpp = self.scheduled_date_one
                            i.fpp_present_one = 'present'
                        else:
                            i.day_one_fpp = self.scheduled_date_one
                            i.fpp_present_one = 'absent'
                if rec.finance_sec_ids:
                    for k in rec.finance_sec_ids:
                        if k.student_id.id == i.id:
                            i.day_two_fpp = self.scheduled_date_two
                            i.fpp_present_two = 'present'
                        else:
                            i.day_two_fpp = self.scheduled_date_two
                            i.fpp_present_two = 'absent'
                if rec.certificate_ids:
                    for c in rec.certificate_ids:
                        if c.student_id.id == i.id:
                            if c.certificate_distributed == True:
                                i.fpp_certificate = True
                            else:
                                i.fpp_certificate = False

        self.state = 'completed'
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Completed',
                'type': 'rainbow_man',
            }
        }


class FinancialPlanningStudentsList(models.Model):
    _name = 'financial.planning.students.list'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_id = fields.Many2one('logic.students', string='Student')
    attendance_day_one = fields.Boolean(string='Attendance', default=True)
    certificate_distributed = fields.Boolean(string='Certificate')
    finance_id = fields.Many2one('financial.planning.form', string='Finance', ondelete='cascade')


class SecondDayForFinancialPlanning(models.Model):
    _name = 'second.day.planning'

    student_id = fields.Many2one('logic.students', string='Student')
    attendance_day_two = fields.Boolean(string='Attendance', default=True)
    certificate_distributed = fields.Boolean(string='Certificate')
    finance_sec_id = fields.Many2one('financial.planning.form', string='Finance', ondelete='cascade')


class FinancialCertificates(models.Model):
    _name = 'financial.certificate'

    student_id = fields.Many2one('logic.students', string='Student')
    certificate_distributed = fields.Boolean(string='Certificate')
    certificate_id = fields.Many2one('financial.planning.form',  ondelete='cascade', string='Certificate')
