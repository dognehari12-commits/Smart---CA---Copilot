"""OCR Engine - Parses financial documents using pdfplumber/pypdf and regex extraction."""

import io
import re
from typing import Optional

try:
    import pdfplumber
except ImportError:
    pdfplumber = None

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

from data.sample_data import EXTRACTED_DOCUMENTS


class OCREngine:
    """Extracts structured data from financial documents (PDFs, text, images)."""

    # ── PDF Text Extraction ──────────────────────────────────

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from a PDF using pdfplumber (preferred) or pypdf (fallback)."""
        text = ""

        # Try pdfplumber first — better table and layout handling
        if pdfplumber is not None:
            try:
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    pages = []
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            pages.append(page_text)
                        # Also try extracting tables
                        for table in page.extract_tables() or []:
                            for row in table:
                                if row:
                                    cells = [str(c).strip() for c in row if c]
                                    pages.append(" | ".join(cells))
                    text = "\n".join(pages)
            except Exception:
                text = ""

        # Fallback to pypdf if pdfplumber returned nothing or isn't available
        if not text.strip() and PdfReader is not None:
            try:
                reader = PdfReader(io.BytesIO(file_bytes))
                pages = []
                for page in reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        pages.append(page_text)
                text = "\n".join(pages)
            except Exception:
                text = ""

        return text

    # ── Document Type Detection ───────────────────────────────

    @staticmethod
    def detect_document_type(text: str) -> str:
        """Detect document type from text content using keyword scoring."""
        text_lower = text.lower()

        scores = {
            "Invoice": 0,
            "Payroll Register": 0,
            "Bank Statement": 0,
            "GST Return": 0,
        }

        invoice_kw = ["invoice", "bill no", "vendor", "gst rate", "hsn",
                       "taxable", "subtotal", "amount due", "payment terms",
                       "billing address", "ship to"]
        payroll_kw = ["salary", "payroll", "employee", "epf", "esi",
                       "gross pay", "deduction", "net pay", "pf contribution"]
        bank_kw = ["bank statement", "account number", "opening balance",
                    "closing balance", "transaction", "debit", "credit",
                    "withdrawal", "deposit"]
        gst_kw = ["gstr", "gst return", "output tax", "input tax credit",
                   "gstin", "outward supply", "inward supply", "cgst", "sgst", "igst"]

        for kw in invoice_kw:
            if kw in text_lower:
                scores["Invoice"] += 1
        for kw in payroll_kw:
            if kw in text_lower:
                scores["Payroll Register"] += 1
        for kw in bank_kw:
            if kw in text_lower:
                scores["Bank Statement"] += 1
        for kw in gst_kw:
            if kw in text_lower:
                scores["GST Return"] += 1

        best = max(scores, key=scores.get)
        if scores[best] == 0:
            return "Unknown"
        return best

    # ── Field Extraction ──────────────────────────────────────

    @staticmethod
    def extract_invoice_number(text: str) -> Optional[str]:
        """Extract invoice/bill number with multiple pattern variants."""
        patterns = [
            # "Invoice No: ABC-123" / "Invoice #: ABC/123"
            r'(?:inv(?:oice)?|bill)[\s\-_#:]*(?:no[\.\s#:]*)?[\s]*([A-Z0-9][A-Z0-9\-/]{2,30})',
            # Standalone "INV-2025-001" on its own line
            r'^\s*((?:INV|BILL|RN)[\-/][A-Z0-9\-/]{3,25})\s*$',
            # "REF: TCS/2025-26/0412"
            r'(?:ref(?:erence)?[\s\-_#:]+)([A-Z0-9][A-Z0-9\-/]{3,30})',
        ]
        for pat in patterns:
            for m in re.finditer(pat, text, re.I | re.M):
                val = m.group(1).strip()
                # Reject values that are clearly not invoice numbers
                if val.lower() in ('no', 'number', 'num', 'invoice', 'bill'):
                    continue
                if len(val) >= 3:
                    return val
        return None

    @staticmethod
    def extract_dates(text: str) -> list[str]:
        """Extract all dates from text in various formats. Returns list of matches."""
        dates = []
        patterns = [
            # 15-Apr-2025 / 15/Apr/2025 / 15.April.2025
            r'(\d{1,2}[\s\-/.](?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?[\s\-/.]\d{2,4})',
            # 2025-04-15 / 2025/04/15
            r'(\d{4}[\-/.]\d{1,2}[\-/.]\d{1,2})',
            # 15/04/2025 / 15-04-2025 / 15.04.2025 (day-first, common in India)
            r'(\d{1,2}[\-/.]\d{1,2}[\-/.]\d{4})',
            # 15 Apr 2025 (no separator)
            r'(\d{1,2}\s+(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?\s+\d{2,4})',
        ]
        for pat in patterns:
            for m in re.finditer(pat, text, re.I):
                dates.append(m.group(1).strip())
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for d in dates:
            normalized = d.lower().strip()
            if normalized not in seen:
                seen.add(normalized)
                unique.append(d)
        return unique

    @staticmethod
    def extract_amounts(text: str) -> list[dict]:
        """Extract all monetary amounts with their context."""
        amounts = []
        patterns = [
            # ₹2,50,000.00 / Rs. 250000 / INR 2,50,000
            r'((?:₹|Rs\.?|INR|USD|\$)\s*[\d,]+\.?\d*)',
            # "Total: 250000" / "Amount Due: 2,50,000.00"
            r'((?:total|amount|sum|grand total|net amount|gross|balance|payable|due|subtotal)[:\s]+[\d,]+\.?\d*)',
        ]

        for pat in patterns:
            for m in re.finditer(pat, text, re.I):
                raw = m.group(1)
                num_str = re.sub(r'[^\d.]', '', raw.replace(',', ''))
                try:
                    value = float(num_str)
                    if value > 0:
                        amounts.append({"raw": raw.strip(), "value": value})
                except ValueError:
                    continue

        # Also look for bare numbers in amount-labeled rows
        # e.g. "CGST @ 9%: Rs. 22500" or "Subtotal: 250000"
        for m in re.finditer(
            r'(?:cgst|sgst|igst|gst|tax|vat|subtotal|sub-total|total|amount|net|gross)[^\n]{0,30}?'
            r'(?:[₹Rs]*\s*)(\d[\d,]+\.?\d*)',
            text, re.I,
        ):
            raw = m.group(1)
            num_str = raw.replace(',', '')
            try:
                value = float(num_str)
                if value > 0:
                    amounts.append({"raw": m.group(0).strip(), "value": value})
            except ValueError:
                continue

        # Deduplicate by value
        seen = set()
        unique = []
        for a in amounts:
            if a["value"] not in seen:
                seen.add(a["value"])
                unique.append(a)
        return unique

    @staticmethod
    def extract_gst_info(text: str) -> dict:
        """Extract GST-related fields: GSTIN, GST amount, GST rate, tax breakdown."""
        info = {
            "gstin": None,
            "cgst": None,
            "sgst": None,
            "igst": None,
            "total_gst": None,
            "gst_rate": None,
        }

        # GSTIN (15-character: 2-digit state + 10-char PAN + 1 char entity + Z + checksum)
        gstin_match = re.search(r'\b(\d{2}[A-Z]{5}\d{4}[A-Z]{1}[A-Z\d]{1}[Z]{1}[A-Z\d]{1})\b', text)
        if gstin_match:
            info["gstin"] = gstin_match.group(1)

        # GST rate (e.g. "@ 18%" or "GST @18%")
        rate_match = re.search(r'(?:@|gst|tax)\s*(\d{1,2}(?:\.\d+)?)\s*%', text, re.I)
        if rate_match:
            info["gst_rate"] = float(rate_match.group(1))

        # CGST / SGST / IGST amounts
        cgst_match = re.search(r'cgst[\s:]*[\₹Rs]*\s*([\d,]+\.?\d*)', text, re.I)
        if cgst_match:
            info["cgst"] = float(cgst_match.group(1).replace(',', ''))

        sgst_match = re.search(r'sgst[\s:]*[\₹Rs]*\s*([\d,]+\.?\d*)', text, re.I)
        if sgst_match:
            info["sgst"] = float(sgst_match.group(1).replace(',', ''))

        igst_match = re.search(r'igst[\s:]*[\₹Rs]*\s*([\d,]+\.?\d*)', text, re.I)
        if igst_match:
            info["igst"] = float(igst_match.group(1).replace(',', ''))

        # Total GST (look for "GST Amount: X" or "Total GST: X")
        gst_total_match = re.search(
            r'(?:total\s+)?(?:gst|tax)\s+(?:amount|total)?[\s:]*[\₹Rs]*\s*([\d,]+\.?\d*)',
            text, re.I,
        )
        if gst_total_match:
            info["total_gst"] = float(gst_total_match.group(1).replace(',', ''))
        elif info["cgst"] and info["sgst"]:
            info["total_gst"] = info["cgst"] + info["sgst"]
            if info["igst"]:
                info["total_gst"] += info["igst"]

        return info

    @staticmethod
    def extract_vendor(text: str) -> Optional[str]:
        """Extract vendor/supplier/company name."""
        patterns = [
            # "Vendor: Tata Consultancy Services\n" (stop at newline or GSTIN)
            r'(?:vendor|supplier|from|billed by|sold by|company|seller)[\s\-_:]+([A-Za-z][A-Za-z\s&.,]{3,50}?)(?:\s*(?:\n|GSTIN|GST|gstin|\d{2}[A-Z]{5}))',
            # "M/s. ABC Enterprises\n"
            r'(?:M/s\.?|Messrs?)\s+([A-Za-z][A-Za-z\s&.,]{3,50}?)(?:\s*(?:\n|GSTIN|GST|\d{2}[A-Z]{5}))',
            # Standalone line: company name followed by GSTIN on next line
            r'([A-Za-z][A-Za-z\s&.,]{5,45})\s*\n\s*\d{2}[A-Z]{5}',
            # Fallback: vendor keyword, capture to end of line
            r'(?:vendor|supplier|from|billed by|sold by|company|seller)[\s\-_:]+([A-Za-z][A-Za-z\s&.,]{3,60})',
            # M/s fallback to end of line
            r'(?:M/s\.?|Messrs?)\s+([A-Za-z][A-Za-z\s&.,]{3,60})',
        ]
        for pat in patterns:
            m = re.search(pat, text, re.I)
            if m:
                name = m.group(1).strip()
                # Clean trailing junk
                name = re.sub(r'\s{2,}', ' ', name)
                name = re.sub(r'[,\s]+$', '', name)
                # Reject if it looks like a keyword rather than a company name
                if name.lower() in ('no', 'number', 'the', 'and', 'gst'):
                    continue
                if len(name) > 3:
                    return name
        return None

    @staticmethod
    def extract_line_items(text: str) -> list[dict]:
        """Try to extract invoice line items from tabular text."""
        items = []
        # Look for lines with pattern: description ... quantity ... rate ... amount
        lines = text.split('\n')
        for line in lines:
            # Match lines that have a description followed by numbers
            item_match = re.search(
                r'(.{5,60}?)\s+(\d+)\s+[₹Rs]*\s*([\d,]+\.?\d*)\s+[₹Rs]*\s*([\d,]+\.?\d*)',
                line,
            )
            if item_match:
                desc = item_match.group(1).strip()
                # Skip header rows
                if any(kw in desc.lower() for kw in ['description', 'particulars', 'item', 'product']):
                    continue
                items.append({
                    "description": desc,
                    "quantity": int(item_match.group(2)),
                    "rate": float(item_match.group(3).replace(',', '')),
                    "amount": float(item_match.group(4).replace(',', '')),
                })
        return items

    @staticmethod
    def extract_account_info(text: str) -> dict:
        """Extract bank account details."""
        info = {
            "bank_name": None,
            "account_number": None,
            "ifsc": None,
        }

        # Bank name
        bank_match = re.search(
            r'(?:bank|branch)[\s\-:]+([A-Za-z][A-Za-z\s]{3,40})', text, re.I,
        )
        if bank_match:
            info["bank_name"] = bank_match.group(1).strip()

        # Account number (typically 9-18 digits)
        acc_match = re.search(
            r'(?:a/?c|account|acc(?:ount)?)[\s\-#:.]*(\d[\d\s\-]{7,20}\d)', text, re.I,
        )
        if acc_match:
            info["account_number"] = re.sub(r'[\s\-]', '', acc_match.group(1))

        # IFSC code (e.g. HDFC0001234)
        ifsc_match = re.search(r'\b([A-Z]{4}0[A-Z0-9]{6})\b', text)
        if ifsc_match:
            info["ifsc"] = ifsc_match.group(1)

        return info

    @staticmethod
    def extract_full(text: str) -> dict:
        """Run all extractors on the given text and return structured data."""
        doc_type = OCREngine.detect_document_type(text)
        amounts = OCREngine.extract_amounts(text)
        dates = OCREngine.extract_dates(text)
        gst_info = OCREngine.extract_gst_info(text)
        vendor = OCREngine.extract_vendor(text)
        invoice_no = OCREngine.extract_invoice_number(text)
        line_items = OCREngine.extract_line_items(text)
        account_info = OCREngine.extract_account_info(text)

        # Determine total and tax from extracted amounts
        total_amount = amounts[0]["value"] if amounts else None
        tax_amount = gst_info["total_gst"]

        # If no explicit tax found, try to infer from amount list
        if tax_amount is None and len(amounts) >= 2:
            vals = sorted([a["value"] for a in amounts], reverse=True)
            # Heuristic: largest amount is total, second might be tax
            if vals[0] > vals[1] and vals[1] < vals[0] * 0.3:
                tax_amount = vals[1]

        return {
            "doc_type": doc_type,
            "extracted_data": {
                "invoice_number": invoice_no,
                "date": dates[0] if dates else None,
                "all_dates": dates,
                "vendor_name": vendor,
                "gstin": gst_info.get("gstin"),
                "total_amount": total_amount,
                "tax_amount": tax_amount,
                "gst_rate": gst_info.get("gst_rate"),
                "cgst": gst_info.get("cgst"),
                "sgst": gst_info.get("sgst"),
                "igst": gst_info.get("igst"),
                "line_items": line_items,
                "all_amounts": [a["raw"] for a in amounts[:10]],
                "bank_name": account_info.get("bank_name"),
                "account_number": account_info.get("account_number"),
                "ifsc": account_info.get("ifsc"),
            },
        }

    # ── Simulated Extraction (for sample data) ────────────────

    @staticmethod
    def get_simulated_extraction(filename: str) -> Optional[dict]:
        """Return pre-extracted data for a known sample file."""
        for doc in EXTRACTED_DOCUMENTS:
            if doc["filename"].lower() in filename.lower() or filename.lower() in doc["filename"].lower():
                return doc
        return None

    # ── Main Entry Point ──────────────────────────────────────

    @staticmethod
    def process_upload(filename: str, file_bytes: bytes = b"", file_text: str = "") -> dict:
        """
        Process an uploaded document and return extracted data.

        Args:
            filename: Name of the uploaded file.
            file_bytes: Raw bytes of the file (used for PDF extraction).
            file_text: Pre-extracted text (for text files or paste input).
        """
        # 1. Check for simulated extraction first (sample data)
        simulated = OCREngine.get_simulated_extraction(filename)
        if simulated:
            return {
                "success": True,
                "source": "simulated",
                "filename": filename,
                "doc_type": simulated["doc_type"],
                "extracted_data": simulated["extracted_data"],
                "confidence": simulated["confidence"],
            }

        # 2. Extract text from PDF if bytes provided
        text = file_text
        if not text and file_bytes:
            if filename.lower().endswith(".pdf"):
                text = OCREngine.extract_text_from_pdf(file_bytes)
            elif filename.lower().endswith((".txt", ".csv")):
                try:
                    text = file_bytes.decode("utf-8", errors="replace")
                except Exception:
                    text = ""

        # 3. If we have text, run regex extraction
        if text and text.strip():
            result = OCREngine.extract_full(text)

            # Calculate confidence based on how many fields were extracted
            fields = result["extracted_data"]
            filled = sum(1 for v in fields.values()
                         if v is not None and v != [] and v != "")
            total = len(fields)
            confidence = min(0.5 + (filled / total) * 0.5, 0.98)

            return {
                "success": True,
                "source": "pdf_parsed" if file_bytes else "text_parsed",
                "filename": filename,
                "doc_type": result["doc_type"],
                "extracted_data": result["extracted_data"],
                "confidence": round(confidence, 2),
            }

        # 4. Nothing to extract
        return {
            "success": False,
            "filename": filename,
            "error": (
                "Unable to extract text from this document. "
                "If it's a scanned image, OCR (e.g. Tesseract) would be needed. "
                "Try uploading a text-based PDF, a .txt file, or paste text directly."
            ),
        }
