# -*- coding: utf-8 -*-
from datetime import datetime
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class TodoChecklistLine(models.Model):
    _name = 'todo.checklist.line'
    _rec_name = 'description'
    _description = 'Todo Checklist Lines'

    #state = fields.Selection([('draft','Red'), ('done','Green')], string="State", default="draft")
    is_done = fields.Boolean(string="Done")
    description = fields.Text(string="Description")
    expected_time = fields.Datetime(string="Expected Time")
    actual_time = fields.Datetime(string="Actual Time")

    todo_checklist_id = fields.Many2one('todo.checklist', string="ToDo Checklist")

    @api.onchange('is_done')
    def onchange_is_done(self):
        for record in self:
            if record.is_done == True:
                record.actual_time = fields.datetime.now()
            else:
                record.actual_time = False

class TodoChecklist(models.Model):
    _name = 'todo.checklist'
    _description = 'Todo Checklist'

    name = fields.Char(string="Name")
    datetime = fields.Datetime(string="Assigned Time", default=lambda self: fields.datetime.now())
    deadline_datetime = fields.Datetime(string="Deadline Time")
    user_id = fields.Many2one('res.users', string="Assigned to")
    created_by = fields.Many2one('res.users', string="Assigned by", default=lambda self: self.env.user.id)
    description = fields.Text(string="Note")

    todo_type = fields.Selection([('project', 'Project'), ('task', 'Task'), ('subtask', 'Subtask'), ('personal', 'Personal')], string="Todo Type", default="personal")
    project_id = fields.Many2one('project.project', string="Project")
    task_id = fields.Many2one('project.task', string="Task")
    subtask_id = fields.Many2one('project.task', string="Subtask")
    tag_ids = fields.Many2many('todo.checklist.tags', string="Tags")
    information = fields.Selection(compute='_compute_information', string='INFO', selection=[('needToFinish', 'Finish it ASAP'), ('late', 'Late'),('in_progress','In Progress'),('draft','Draft'),('done','Done')])
    
    todo_checklist_line_ids = fields.One2many('todo.checklist.line', 'todo_checklist_id', string="ToDO Checklist Lines")
    status = fields.Selection([('draft', 'Draft'), ('in_progress', 'In Progress'), ('done', 'Done')], string="Status", default="draft")

    @api.onchange('todo_type')
    def onchange_todo_type(self):
        for record in self:
            if record.todo_type == 'project':
                record.task_id = False
                record.subtask_id = False
            elif record.todo_type == 'task':
                record.project_id = False
                record.subtask_id = False
            elif record.todo_type == 'subtask':
                record.project_id = False
                record.task_id = False
            else:
                record.project_id = False
                record.task_id = False
                record.subtask_id = False
    
    # @api.depends('')
    def _compute_information(self):
        for rec in self : 
            if rec.deadline_datetime : 
                deadline = rec.deadline_datetime
                nowadays = datetime.now()
                difference = deadline - nowadays
                if rec.status == 'draft' : 
                    rec.information = 'draft'
                elif rec.status == 'done' :
                    rec.information = 'done'
                else : 
                    if rec.status == 'in_progress':
                        if difference.days < 0 :
                            rec.information = 'late'
                        elif difference.days <= 1 :
                            rec.information = 'needToFinish'
                        else : 
                            rec.information = 'in_progress'
            else : 
                if rec.status == 'draft' : 
                    rec.information = 'draft'
                elif rec.status == 'done' :
                    rec.information = 'done'
                else : 
                    rec.information = 'in_progress' or False

        
