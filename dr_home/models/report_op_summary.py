from odoo import models, api

class AppointmentReport(models.AbstractModel):
    _name = 'report.dr_home.report_op_summary'
    _description = 'Report OP Summary'

    def _get_report_values(self, docids, data=None):
        selected_appointment = self.env['doctor.appointments'].browse(docids)
        company = self.env.company
        report_model = self.env['report.op.summary']
        records = []

        for appointment in selected_appointment:
            booking = self.env['appointment.booking'].search([
                ('reference_id', '=', appointment.reference_id),
                ('appointment_date', '=', appointment.appointment_date)
            ], limit=1)

            consultation_doctor = booking.consultation_doctor.name if booking and booking.consultation_doctor else ''

          
            report_record = report_model.create({
                'op_number': appointment.op_number,
                'appointment_date': appointment.appointment_date,
                'patient_name': appointment.name,
                'patient_id': appointment.reference_id,
                'patient_age': appointment.age,
                'gender': appointment.gender,
                'phone': appointment.phone,
                'email': appointment.email if hasattr(appointment, 'email') else '',
                'consultation_doctor': consultation_doctor,
                'chief_complaint': appointment.chief_complaint,
                'htn': appointment.htn,
                'dm': appointment.dm,
                'th': appointment.th,
                'diet': appointment.diet,
                'special_note': appointment.special_note,
                'associated_complaint': appointment.associated_complaint,
                'past_history': appointment.past_history,
                'family_history': appointment.family_history,
                'present_history': appointment.present_history,
                'diagnosis': appointment.diagnosis,
                'investigations': appointment.investigations,
                'panchakarma_advice': appointment.panchakarma_advice,
                'artava': appointment.artava,
                'nadi': appointment.nadi,
                'agni': appointment.agni,
                'mala': appointment.mala,
                'mutra': appointment.mutra,
                'nidra': appointment.nidra,
                'manas': appointment.manas,
            })
            records.append(report_record.id)

        return {
            'doc_ids': records,
            'doc_model': 'report.op.summary',
            'docs': report_model.browse(records),
            'company': company,
            'company_logo': company.logo.decode('utf-8') if company.logo else False,
        }
