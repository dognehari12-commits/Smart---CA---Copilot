"""Report Generator - Creates professional PDF financial health reports."""

import io
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak,
)
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.barcharts import VerticalBarChart


# ── Color Palette ────────────────────────────────────────────
PRIMARY = colors.HexColor("#1E3A5F")
SECONDARY = colors.HexColor("#2E86C1")
ACCENT = colors.HexColor("#27AE60")
DARK_BG = colors.HexColor("#1A1A2E")
LIGHT_BG = colors.HexColor("#F4F6F9")
TEXT_COLOR = colors.HexColor("#2C3E50")
MUTED = colors.HexColor("#7F8C8D")


class ReportGenerator:
    """Generates professional PDF financial health reports."""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._register_custom_styles()

    def _register_custom_styles(self):
        """Register custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name="ReportTitle",
            parent=self.styles["Title"],
            fontSize=26,
            textColor=PRIMARY,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ))
        self.styles.add(ParagraphStyle(
            name="ReportSubtitle",
            parent=self.styles["Normal"],
            fontSize=12,
            textColor=MUTED,
            spaceAfter=20,
            fontName="Helvetica",
        ))
        self.styles.add(ParagraphStyle(
            name="SectionHeading",
            parent=self.styles["Heading2"],
            fontSize=16,
            textColor=PRIMARY,
            spaceBefore=16,
            spaceAfter=10,
            fontName="Helvetica-Bold",
        ))
        self.styles.add(ParagraphStyle(
            name="MetricLabel",
            parent=self.styles["Normal"],
            fontSize=9,
            textColor=MUTED,
            fontName="Helvetica",
        ))
        self.styles.add(ParagraphStyle(
            name="MetricValue",
            parent=self.styles["Normal"],
            fontSize=18,
            textColor=PRIMARY,
            fontName="Helvetica-Bold",
        ))
        self.styles.add(ParagraphStyle(
            name="BodyText2",
            parent=self.styles["Normal"],
            fontSize=10,
            textColor=TEXT_COLOR,
            leading=14,
            spaceAfter=6,
        ))
        self.styles.add(ParagraphStyle(
            name="SmallMuted",
            parent=self.styles["Normal"],
            fontSize=8,
            textColor=MUTED,
        ))

    def _format_currency(self, amount: float) -> str:
        """Format amount in Indian currency style."""
        if amount < 0:
            return f"-₹{abs(amount):,.0f}"
        return f"₹{amount:,.0f}"

    def _format_pct(self, value: float) -> str:
        """Format as percentage."""
        return f"{value:.1f}%"

    def _make_kpi_row(self, metrics: list[tuple[str, str]]) -> Table:
        """Create a KPI summary row."""
        cells = []
        for label, value in metrics:
            cell = [
                Paragraph(value, self.styles["MetricValue"]),
                Paragraph(label, self.styles["MetricLabel"]),
            ]
            cells.append(cell)

        table = Table([cells], colWidths=[160] * len(cells))
        table.setStyle(TableStyle([
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BG),
            ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#DEE2E6")),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        return table

    def _make_data_table(self, headers: list[str], rows: list[list], col_widths: list = None) -> Table:
        """Create a styled data table."""
        data = [headers] + rows
        if not col_widths:
            col_widths = [460 // len(headers)] * len(headers)

        table = Table(data, colWidths=col_widths)
        style_cmds = [
            ("BACKGROUND", (0, 0), (-1, 0), PRIMARY),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, 0), 9),
            ("FONTSIZE", (0, 1), (-1, -1), 8),
            ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
            ("ALIGN", (0, 0), (0, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#DEE2E6")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT_BG]),
        ]
        table.setStyle(TableStyle(style_cmds))
        return table

    def _make_pie_chart(self, title: str, data_pairs: list[tuple[str, float]], width=220, height=160) -> Drawing:
        """Create a pie chart."""
        d = Drawing(width, height)
        pie = Pie()
        pie.x = 30
        pie.y = 10
        pie.width = 120
        pie.height = 120
        pie.data = [v for _, v in data_pairs]
        pie.labels = [f"{k}\n({v:,.0f})" for k, v in data_pairs]

        palette = [
            colors.HexColor("#2E86C1"), colors.HexColor("#27AE60"),
            colors.HexColor("#E74C3C"), colors.HexColor("#F39C12"),
            colors.HexColor("#9B59B6"), colors.HexColor("#1ABC9C"),
            colors.HexColor("#E67E22"), colors.HexColor("#34495E"),
            colors.HexColor("#16A085"),
        ]
        for i in range(len(data_pairs)):
            pie.slices[i].fillColor = palette[i % len(palette)]
            pie.slices[i].strokeColor = colors.white
            pie.slices[i].strokeWidth = 1

        pie.sideLabels = True
        pie.simpleLabels = False
        pie.slices.fontName = "Helvetica"
        pie.slices.fontSize = 7

        d.add(pie)
        d.add(String(width // 2 - 30, height - 8, title, fontName="Helvetica-Bold", fontSize=9, fillColor=PRIMARY))
        return d

    def _make_bar_chart(self, title: str, categories: list[str], data_series: dict, width=460, height=180) -> Drawing:
        """Create a vertical bar chart."""
        d = Drawing(width, height)
        chart = VerticalBarChart()
        chart.x = 50
        chart.y = 30
        chart.width = width - 80
        chart.height = height - 60
        chart.data = list(data_series.values())
        chart.categoryAxis.categoryNames = categories
        chart.categoryAxis.labels.fontName = "Helvetica"
        chart.categoryAxis.labels.fontSize = 7
        chart.categoryAxis.labels.angle = 45
        chart.valueAxis.valueMin = 0
        chart.valueAxis.labels.fontName = "Helvetica"
        chart.valueAxis.labels.fontSize = 7

        palette = [colors.HexColor("#2E86C1"), colors.HexColor("#27AE60"), colors.HexColor("#E74C3C")]
        for i, key in enumerate(data_series):
            chart.bars[i].fillColor = palette[i % len(palette)]
            chart.bars[i].name = key

        d.add(chart)
        d.add(String(width // 2 - 50, height - 8, title, fontName="Helvetica-Bold", fontSize=9, fillColor=PRIMARY))
        return d

    def generate_report(
        self,
        client_info: dict,
        financial_data: dict,
        gst_returns: list,
    ) -> bytes:
        """Generate a complete PDF financial health report."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer, pagesize=A4,
            topMargin=30, bottomMargin=30,
            leftMargin=40, rightMargin=40,
        )
        story = []
        now = datetime.now()

        # ── Title Page ──────────────────────────────────────
        story.append(Spacer(1, 60))
        story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY))
        story.append(Spacer(1, 20))
        story.append(Paragraph("Financial Health Report", self.styles["ReportTitle"]))
        story.append(Paragraph(
            f"{client_info.get('name', 'Client')}  •  FY 2025-26  •  Generated {now.strftime('%d %B %Y')}",
            self.styles["ReportSubtitle"],
        ))
        story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#DEE2E6")))
        story.append(Spacer(1, 30))

        # Client info table
        info_rows = [
            ["Client Name", client_info.get("name", "N/A"), "PAN", client_info.get("pan", "N/A")],
            ["Entity Type", client_info.get("type", "N/A"), "Industry", client_info.get("industry", "N/A")],
            ["Annual Turnover", self._format_currency(client_info.get("annual_turnover", 0)),
             "Tax Regime", client_info.get("tax_regime", "N/A")],
            ["GST Registered", "Yes" if client_info.get("gst_registered") else "No",
             "Status", client_info.get("compliance_status", "N/A")],
        ]
        info_table = Table(info_rows, colWidths=[90, 130, 90, 130])
        info_table.setStyle(TableStyle([
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
            ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
            ("TEXTCOLOR", (0, 0), (0, -1), MUTED),
            ("TEXTCOLOR", (2, 0), (2, -1), MUTED),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW", (0, 0), (-1, -1), 0.5, colors.HexColor("#DEE2E6")),
        ]))
        story.append(info_table)
        story.append(Spacer(1, 30))

        # ── KPIs ────────────────────────────────────────────
        story.append(Paragraph("Executive Summary", self.styles["SectionHeading"]))

        total_revenue = sum(financial_data.get("revenue", []))
        total_expenses = sum(financial_data.get("total_expenses", []))
        total_profit = total_revenue - total_expenses
        total_tax = sum(
            sum(v) for v in financial_data.get("taxes", {}).values()
        )
        net_profit = total_profit - total_tax
        profit_margin = (total_profit / total_revenue * 100) if total_revenue else 0
        tax_burden = (total_tax / total_profit * 100) if total_profit else 0

        kpis = [
            ("Total Revenue", self._format_currency(total_revenue)),
            ("Total Expenses", self._format_currency(total_expenses)),
            ("Profit Before Tax", self._format_currency(total_profit)),
            ("Total Tax Liability", self._format_currency(total_tax)),
            ("Net Profit", self._format_currency(net_profit)),
            ("Profit Margin", self._format_pct(profit_margin)),
        ]
        story.append(self._make_kpi_row(kpis[:3]))
        story.append(Spacer(1, 8))
        story.append(self._make_kpi_row(kpis[3:]))
        story.append(Spacer(1, 20))

        # ── Revenue & Expense Chart ─────────────────────────
        story.append(Paragraph("Monthly Performance", self.styles["SectionHeading"]))
        chart_data = {
            "Revenue": financial_data.get("revenue", []),
            "Expenses": financial_data.get("total_expenses", []),
        }
        months_short = [m[:3] for m in financial_data.get("months", [])]
        story.append(self._make_bar_chart(
            "Revenue vs Expenses (₹)", months_short, chart_data,
        ))
        story.append(Spacer(1, 20))

        # ── Expense Breakdown Pie ───────────────────────────
        story.append(Paragraph("Expense Breakdown", self.styles["SectionHeading"]))
        expenses = financial_data.get("expenses", {})
        exp_pairs = [(cat, sum(vals)) for cat, vals in expenses.items()]
        exp_pairs.sort(key=lambda x: x[1], reverse=True)
        story.append(self._make_pie_chart("Annual Expense Distribution", exp_pairs))
        story.append(Spacer(1, 20))

        # ── Tax Breakdown Pie ───────────────────────────────
        story.append(Paragraph("Tax Liability Breakdown", self.styles["SectionHeading"]))
        taxes = financial_data.get("taxes", {})
        tax_pairs = [(t, sum(v)) for t, v in taxes.items()]
        tax_pairs.sort(key=lambda x: x[1], reverse=True)
        story.append(self._make_pie_chart("Tax Distribution", tax_pairs))
        story.append(Spacer(1, 20))

        # ── GST Summary Table ───────────────────────────────
        story.append(PageBreak())
        story.append(Paragraph("GST Compliance Summary", self.styles["SectionHeading"]))

        gst_headers = ["Month", "Turnover", "Output GST", "Input GST", "Net Payable", "Status"]
        gst_rows = []
        for r in gst_returns:
            gst_rows.append([
                r["month"],
                self._format_currency(r["taxable_turnover"]),
                self._format_currency(r["output_gst"]),
                self._format_currency(r["input_gst"]),
                self._format_currency(r["net_gst_payable"]),
                r["filing_status"],
            ])
        gst_table = self._make_data_table(
            gst_headers, gst_rows,
            col_widths=[65, 80, 75, 75, 80, 55],
        )
        story.append(gst_table)
        story.append(Spacer(1, 20))

        # ── Profitability Trend Chart ───────────────────────
        story.append(Paragraph("Profitability Trend", self.styles["SectionHeading"]))
        net_profit_data = financial_data.get("net_profit", [])
        profit_chart = {
            "Net Profit": net_profit_data,
            "Tax Paid": [sum(taxes[t][i] for t in taxes) for i in range(len(net_profit_data))],
        }
        story.append(self._make_bar_chart(
            "Net Profit & Tax Paid (₹)", months_short, profit_chart,
        ))
        story.append(Spacer(1, 20))

        # ── Key Observations ────────────────────────────────
        story.append(Paragraph("Key Observations & Recommendations", self.styles["SectionHeading"]))

        observations = []
        if profit_margin < 10:
            observations.append(
                "⚠️ <b>Low Profit Margin ({:.1f}%)</b>: Consider reviewing operational expenses "
                "and identifying cost optimization opportunities.".format(profit_margin)
            )
        else:
            observations.append(
                "✅ <b>Healthy Profit Margin ({:.1f}%)</b>: The business maintains a sustainable "
                "profitability ratio.".format(profit_margin)
            )

        if tax_burden > 30:
            observations.append(
                "⚠️ <b>High Tax Burden ({:.1f}%)</b>: Explore tax planning strategies including "
                "Section 80C investments, capital gains optimization, and regime comparison.".format(tax_burden)
            )

        pending_gst = [r for r in gst_returns if r["filing_status"] != "Filed"]
        if pending_gst:
            observations.append(
                f"📋 <b>Pending GST Returns</b>: {len(pending_gst)} month(s) have unfiled returns. "
                "File immediately to avoid late fees of ₹50/day per return."
            )

        observations.append(
            "📊 <b>Recommendation</b>: Maintain quarterly review cycles and ensure all "
            "compliance deadlines are tracked using the CA Copilot dashboard."
        )

        for obs in observations:
            story.append(Paragraph(obs, self.styles["BodyText2"]))
            story.append(Spacer(1, 4))

        # ── Footer / Disclaimer ─────────────────────────────
        story.append(Spacer(1, 30))
        story.append(HRFlowable(width="100%", thickness=0.5, color=MUTED))
        story.append(Spacer(1, 6))
        story.append(Paragraph(
            f"This report is generated by <b>Smart CA Copilot</b> on {now.strftime('%d %B %Y at %H:%M')}. "
            "This is an automated report for informational purposes only and does not constitute "
            "professional tax or financial advice. Please consult a qualified Chartered Accountant "
            "for compliance decisions.",
            self.styles["SmallMuted"],
        ))

        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer.read()
