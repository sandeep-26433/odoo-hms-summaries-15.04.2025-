from odoo import models, fields, api

class AppointmentReport(models.AbstractModel):
    _name = 'report.dr_home.appointment_report_template'
    _description = 'Appointment Report'

    def _get_report_values(self, docids, data=None):
        appointments = self.env['doctor.appointments'].browse(docids)
        company = self.env.company  

        report_records = self.env['report.appointment.report']
        records = []

        for appointment in appointments:
            booking = self.env['appointment.booking'].search([
                ('reference_id', '=', appointment.reference_id)
            ], limit=1)

            # ✅ Step 1: Create the main report record (without medicine lines yet)
            report_record = report_records.create({
                'op_number': booking.op_number if booking else ' ',
                'appointment_date': booking.appointment_date if booking else False,
                'patient_name': booking.patient_id.name if booking and booking.patient_id else 'N/A',
                'patient_id': booking.reference_id if booking else 'N/A',
                'patient_age': booking.age if booking else 0,
                'gender': booking.gender if booking else '',
                'phone': booking.phone if booking else '',
                'email': booking.email if booking else '',
                'consultation_doctor': booking.consultation_doctor.name if booking.consultation_doctor else 'N/A',
                'chief_complaint': appointment.chief_complaint or '',
                'htn': appointment.htn or '',
                'dm': appointment.dm or '',
                'th': appointment.th or '',
                'diet': appointment.diet or '',
                'special_note': appointment.special_note or '',
            })

            # ✅ Step 2: Now create medicine lines linked to the report_record
            medicine_lines = []
            for medicine in appointment.medicine_line_ids:
                medicine_lines.append((0, 0, {
                    'report_id': report_record.id,
                    'medicine_name': medicine.medicine_id.medicine_name,
                    'dosage': medicine.dosage_id.dosage if medicine.dosage_id else 'N/A',
                    'days': medicine.days,
                    'quantity': medicine.quantity,
                    'usage': medicine.usage,
                    'course': medicine.course or '1',
                }))

            report_record.write({'medicine_line_ids': medicine_lines})

            records.append(report_record.id)

        return {
            'doc_ids': records,
            'doc_model': 'report.appointment.report',
            'docs': report_records.browse(records),
            'company': company,
            'company_logo': company.logo.decode('utf-8') if company.logo else False,
        }
