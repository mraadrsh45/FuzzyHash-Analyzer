import os
from datetime import datetime, timezone
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from config import Config

class ReportService:
    """Service for generating professional digital forensics PDF reports using ReportLab."""

    @classmethod
    def generate_pdf_report(cls, analysis_data: dict, output_path: str = None) -> str:
        """Generate a complete forensic PDF report for a given analysis record."""
        an_id = analysis_data.get('analysis_id', 'AN-UNKNOWN')
        if not output_path:
            filename = f"Forensic_Report_{an_id}.pdf"
            output_path = os.path.join(Config.REPORT_FOLDER, filename)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=36,
            leftMargin=36,
            topMargin=36,
            bottomMargin=36
        )

        styles = getSampleStyleSheet()

        # Custom Dark SOC Aesthetics Styles for PDF
        primary_color = colors.HexColor('#0F172A')    # Slate dark header
        accent_cyan = colors.HexColor('#0284C7')      # Cyan accent
        bg_light = colors.HexColor('#F8FAFC')         # Crisp clean card bg
        text_dark = colors.HexColor('#1E293B')        # Body text
        text_muted = colors.HexColor('#64748B')       # Muted subtext
        border_color = colors.HexColor('#CBD5E1')     # Soft border

        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            textColor=colors.HexColor('#0F172A'),
            spaceAfter=4
        )

        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica-Bold',
            fontSize=11,
            textColor=accent_cyan,
            spaceAfter=15
        )

        section_heading = ParagraphStyle(
            'SectionHeading',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            textColor=primary_color,
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'ReportBody',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=text_dark
        )

        body_bold = ParagraphStyle(
            'ReportBodyBold',
            parent=body_style,
            fontName='Helvetica-Bold'
        )

        disclaimer_style = ParagraphStyle(
            'ReportDisclaimer',
            parent=styles['Normal'],
            fontName='Helvetica-Oblique',
            fontSize=8,
            leading=11,
            textColor=colors.HexColor('#B91C1C')  # Alert Red
        )

        story = []

        # Header Block
        story.append(Paragraph("FUZZYHASH ANALYZER", subtitle_style))
        story.append(Paragraph("Digital Forensics File Similarity Report", title_style))
        story.append(HRFlowable(width="100%", thickness=2, color=accent_cyan, spaceAfter=12))

        # Case Metadata Table
        case_info = [
            [
                Paragraph("<b>Case ID:</b>", body_style), Paragraph(analysis_data.get('case_code', 'N/A'), body_style),
                Paragraph("<b>Analysis ID:</b>", body_style), Paragraph(analysis_data.get('analysis_id', 'N/A'), body_style)
            ],
            [
                Paragraph("<b>Case Name:</b>", body_style), Paragraph(analysis_data.get('case_name', 'N/A'), body_style),
                Paragraph("<b>Timestamp:</b>", body_style), Paragraph(analysis_data.get('created_at', 'N/A'), body_style)
            ],
            [
                Paragraph("<b>Investigator:</b>", body_style), Paragraph(analysis_data.get('investigator', 'Lead Analyst'), body_style),
                Paragraph("<b>Classification:</b>", body_style), Paragraph("OFFICIAL FORENSIC RECORD", body_bold)
            ]
        ]

        t_case = Table(case_info, colWidths=[90, 180, 90, 180])
        t_case.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), bg_light),
            ('BOX', (0, 0), (-1, -1), 1, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t_case)
        story.append(Spacer(1, 12))

        # Similarity Score Highlight Box
        score = analysis_data.get('similarity_score', 0)
        assessment = analysis_data.get('assessment', 'Unknown')
        
        score_bg = colors.HexColor('#ECFDF5') if score <= 30 else (colors.HexColor('#FEF3C7') if score <= 70 else colors.HexColor('#FEF2F2'))
        score_text_color = colors.HexColor('#047857') if score <= 30 else (colors.HexColor('#B45309') if score <= 70 else colors.HexColor('#B91C1C'))

        score_p_style = ParagraphStyle('ScoreBig', fontName='Helvetica-Bold', fontSize=26, textColor=score_text_color, alignment=1)
        assess_p_style = ParagraphStyle('AssessBig', fontName='Helvetica-Bold', fontSize=14, textColor=score_text_color, alignment=1)

        sim_box_data = [
            [Paragraph(f"{score}%", score_p_style)],
            [Paragraph(assessment.upper(), assess_p_style)]
        ]
        t_sim = Table(sim_box_data, colWidths=[540])
        t_sim.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), score_bg),
            ('BOX', (0, 0), (-1, -1), 1.5, score_text_color),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('PADDING', (0, 0), (-1, -1), 10),
        ]))
        story.append(t_sim)
        story.append(Spacer(1, 15))

        # Evidence Files Section
        story.append(Paragraph("Evidence File Details", section_heading))
        
        ev_a = analysis_data.get('evidence_a') or {}
        ev_b = analysis_data.get('evidence_b') or {}

        def format_ev_rows(title, ev):
            return [
                [Paragraph(f"<b>{title} Filename:</b>", body_style), Paragraph(str(ev.get('original_filename', 'N/A')), body_bold)],
                [Paragraph("<b>File Size:</b>", body_style), Paragraph(f"{ev.get('file_size', 0):,} bytes", body_style)],
                [Paragraph("<b>MIME Type:</b>", body_style), Paragraph(str(ev.get('mime_type', 'N/A')), body_style)],
                [Paragraph("<b>MD5:</b>", body_style), Paragraph(str(ev.get('md5', 'N/A')), body_style)],
                [Paragraph("<b>SHA-256:</b>", body_style), Paragraph(str(ev.get('sha256', 'N/A')), body_style)],
                [Paragraph("<b>ssdeep Hash:</b>", body_style), Paragraph(str(ev.get('fuzzy_hash_ssdeep', 'N/A')), body_style)],
                [Paragraph("<b>TLSH Hash:</b>", body_style), Paragraph(str(ev.get('fuzzy_hash_tlsh', 'N/A')), body_style)]
            ]

        ev_table_data = [
            [Paragraph("<b>Attribute</b>", body_bold), Paragraph("<b>File A (Reference)</b>", body_bold), Paragraph("<b>File B (Target)</b>", body_bold)],
            [Paragraph("Filename", body_style), Paragraph(str(ev_a.get('original_filename', 'N/A')), body_style), Paragraph(str(ev_b.get('original_filename', 'N/A')), body_style)],
            [Paragraph("File Size", body_style), Paragraph(f"{ev_a.get('file_size', 0):,} B", body_style), Paragraph(f"{ev_b.get('file_size', 0):,} B", body_style)],
            [Paragraph("MIME Type", body_style), Paragraph(str(ev_a.get('mime_type', 'N/A')), body_style), Paragraph(str(ev_b.get('mime_type', 'N/A')), body_style)],
            [Paragraph("MD5", body_style), Paragraph(str(ev_a.get('md5', 'N/A')), body_style), Paragraph(str(ev_b.get('md5', 'N/A')), body_style)],
            [Paragraph("SHA-256", body_style), Paragraph(str(ev_a.get('sha256', 'N/A')), body_style), Paragraph(str(ev_b.get('sha256', 'N/A')), body_style)],
            [Paragraph("ssdeep", body_style), Paragraph(str(ev_a.get('fuzzy_hash_ssdeep', 'N/A')), body_style), Paragraph(str(ev_b.get('fuzzy_hash_ssdeep', 'N/A')), body_style)],
            [Paragraph("TLSH", body_style), Paragraph(str(ev_a.get('fuzzy_hash_tlsh', 'N/A')), body_style), Paragraph(str(ev_b.get('fuzzy_hash_tlsh', 'N/A')), body_style)]
        ]

        t_ev = Table(ev_table_data, colWidths=[90, 225, 225])
        t_ev.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), primary_color),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BOX', (0, 0), (-1, -1), 1, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))

        # Fix white header text for PDF table
        header_p_style = ParagraphStyle('THeader', parent=body_bold, textColor=colors.white)
        ev_table_data[0] = [
            Paragraph("Attribute", header_p_style),
            Paragraph("File A (Reference)", header_p_style),
            Paragraph("File B (Target)", header_p_style)
        ]

        story.append(t_ev)
        story.append(Spacer(1, 15))

        # Algorithm Analysis Breakdown
        story.append(Paragraph("Fuzzy Hash Breakdown", section_heading))
        algo_data = [
            [Paragraph("Algorithm", header_p_style), Paragraph("Metric / Output", header_p_style), Paragraph("Similarity Assessment", header_p_style)],
            [Paragraph("ssdeep (CTPH)", body_bold), Paragraph(f"Score: {analysis_data.get('ssdeep_score', 0)} / 100", body_style), Paragraph(f"{analysis_data.get('ssdeep_score', 0)}% structural match", body_style)],
            [Paragraph("TLSH (Locality Sensitive)", body_bold), Paragraph(f"Distance: {analysis_data.get('tlsh_score', 0)}", body_style), Paragraph(f"{analysis_data.get('tlsh_similarity_pct', 0)}% normalized similarity", body_style)]
        ]
        t_algo = Table(algo_data, colWidths=[160, 180, 200])
        t_algo.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), accent_cyan),
            ('BOX', (0, 0), (-1, -1), 1, border_color),
            ('INNERGRID', (0, 0), (-1, -1), 0.5, border_color),
            ('PADDING', (0, 0), (-1, -1), 5),
        ]))
        story.append(t_algo)
        story.append(Spacer(1, 12))

        # Analyst Notes & Findings
        story.append(Paragraph("Analyst Findings & Notes", section_heading))
        notes_text = analysis_data.get('notes') or "No additional analyst notes recorded."
        story.append(Paragraph(notes_text, body_style))
        story.append(Spacer(1, 12))

        # Methodology Summary
        story.append(Paragraph("Forensic Methodology", section_heading))
        method_text = (
            "Cryptographic hashing (MD5, SHA-256) calculates exact, tamper-evident digests where a single-bit edit "
            "results in complete avalanche divergence. Fuzzy hashing (ssdeep / CTPH and TLSH) evaluates similarity "
            "across modified, obfuscated, or variant binaries by analyzing localized byte sequence distributions and "
            "piecewise context windows."
        )
        story.append(Paragraph(method_text, body_style))
        story.append(Spacer(1, 15))

        # Mandatory Disclaimer Box
        story.append(Paragraph("Forensic Disclaimer & Investigative Guidelines", section_heading))
        disclaimer_text = (
            "<b>IMPORTANT NOTICE:</b> Similarity assessment is an investigative file-relationship indicator "
            "and DOES NOT independently establish that a file is malicious. High similarity may indicate shared code libraries, "
            "common compilation toolchains, or legitimate software derivatives. Malware determination requires additional static, "
            "dynamic, sandboxing, YARA, PE section, and threat-intelligence analysis."
        )
        t_disc = Table([[Paragraph(disclaimer_text, disclaimer_style)]], colWidths=[540])
        t_disc.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF2F2')),
            ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#FCA5A5')),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(t_disc)
        story.append(Spacer(1, 20))

        # Signature Block
        sig_data = [
            [Paragraph("<b>Investigator Signature:</b> ___________________________", body_style), Paragraph("<b>Date:</b> _____________", body_style)]
        ]
        t_sig = Table(sig_data, colWidths=[360, 180])
        story.append(t_sig)

        # Build PDF
        doc.build(story)
        return output_path
