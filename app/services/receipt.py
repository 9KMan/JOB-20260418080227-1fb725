from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from io import BytesIO
from datetime import datetime
from typing import List, Dict, Any


class ReceiptService:
    def generate_receipt(
        self,
        donor_name: str,
        donor_email: str,
        amount: float,
        currency: str,
        payment_reference: str,
        payment_date: datetime,
        scholarship_details: List[Dict[str, Any]],
        student_name: str
    ) -> bytes:
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )

        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1
        )

        elements = []

        elements.append(Paragraph("SCHOLARSHIP DONATION RECEIPT", title_style))
        elements.append(Spacer(1, 0.5 * inch))

        receipt_info = [
            ["Receipt Date:", payment_date.strftime("%Y-%m-%d %H:%M UTC")],
            ["Reference:", payment_reference],
            ["Amount:", f"{currency} {amount:.2f}"],
            ["Donor:", f"{donor_name} ({donor_email})"],
            ["Student:", student_name],
        ]

        info_table = Table(receipt_info, colWidths=[2 * inch, 4 * inch])
        info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(info_table)
        elements.append(Spacer(1, 0.5 * inch))

        if scholarship_details:
            elements.append(Paragraph("Scholarship Items:", styles['Heading2']))
            elements.append(Spacer(1, 0.25 * inch))

            table_data = [["Description", "Amount"]]
            for item in scholarship_details:
                desc = item.get('description', 'N/A') if isinstance(item, dict) else 'N/A'
                amt = item.get('amount', 0) if isinstance(item, dict) else 0
                table_data.append([desc, f"{currency} {amt:.2f}"])

            items_table = Table(table_data, colWidths=[4 * inch, 2 * inch])
            items_table.setStyle(TableStyle([
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))
            elements.append(items_table)

        elements.append(Spacer(1, inch))
        elements.append(Paragraph(
            "Thank you for your generous donation to support education!",
            styles['Normal']
        ))

        doc.build(elements)
        buffer.seek(0)
        return buffer.read()


receipt_service = ReceiptService()