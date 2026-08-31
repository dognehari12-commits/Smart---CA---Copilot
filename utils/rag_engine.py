"""RAG Engine - Retrieval-Augmented Generation for tax rule search.

Works entirely offline with no external API keys. Uses smart keyword matching,
phrase extraction, intent detection, and template-based answer generation
to provide accurate, context-aware answers from the loaded knowledge base
and any user-uploaded documents.
"""

import re
from typing import Optional
from data.sample_data import TAX_RULES_KB


# ── Intent Detection Patterns ────────────────────────────────
# Maps query intents to answer templates so we can give direct,
# authoritative answers even when relevance scores are low.

INTENT_PATTERNS = {
    "80C": {
        "keywords": ["80c", "section 80c", "deduction", "deductions", "ppf", "epf", "elss",
                      "nsc", "80c limit", "investments", "savings", "tuition fees"],
        "answer": (
            "**Section 80C Deductions (FY 2025-26)**\n\n"
            "Section 80C allows deductions up to **₹1,50,000** per annum from gross total income.\n\n"
            "**Eligible instruments:**\n"
            "• Life Insurance Premium\n"
            "• Public Provident Fund (PPF)\n"
            "• Employee Provident Fund (EPF)\n"
            "• National Savings Certificate (NSC)\n"
            "• Equity Linked Savings Scheme (ELSS)\n"
            "• Home Loan Principal Repayment\n"
            "• Tuition Fees (up to 2 children)\n\n"
            "**Additional:** Senior citizens can claim ₹50,000 deduction under **Section 80TTB** "
            "for interest income.\n\n"
            "📌 *Source: Income Tax Act, 1961*"
        ),
        "doc_id": "TR001",
    },
    "gst_rates": {
        "keywords": ["gst rate", "gst slab", "gst percentage", "gst %", "tax slab",
                      "5% gst", "12% gst", "18% gst", "28% gst", "exempt", "zero rated"],
        "answer": (
            "**GST Rate Structure (India)**\n\n"
            "GST rates are classified into 5 slabs:\n\n"
            "| Rate | Category | Examples |\n"
            "|------|----------|----------|\n"
            "| **0%** | Exempt | Food grains, fresh vegetables, milk |\n"
            "| **5%** | Low | Packaged food, footwear <₹1000, transport |\n"
            "| **12%** | Standard | Business services, IT services, manufactured goods |\n"
            "| **18%** | Standard | Most services, software, professional fees |\n"
            "| **28%** | Luxury | Cars, tobacco, aerated drinks + Cess |\n\n"
            "**Key rules:**\n"
            "• HSN codes mandatory on invoices if turnover > ₹5 crore\n"
            "• Reverse charge mechanism under Section 9(3) CGST Act\n\n"
            "📌 *Source: GST Council Notification 2024*"
        ),
        "doc_id": "TR002",
    },
    "tds": {
        "keywords": ["tds", "tax deducted at source", "194a", "194c", "194h", "194i",
                      "194j", "194q", "tds rate", "tds on salary", "tds on rent"],
        "answer": (
            "**TDS Rates - FY 2025-26**\n\n"
            "| Section | Nature | Rate (Individuals) | Rate (Others) |\n"
            "|---------|--------|-------------------|---------------|\n"
            "| 194A | Interest (other than on securities) | 10% | 10% |\n"
            "| 194C | Payment to contractors | 1% | 2% |\n"
            "| 194H | Commission / brokerage | 5% | 5% |\n"
            "| 194I(a) | Rent - Plant & machinery | 2% | 2% |\n"
            "| 194I(b) | Rent - Land / building | 10% | 10% |\n"
            "| 194J | Technical services / royalty | 2% | 10% |\n"
            "| 194Q | Purchase of goods > ₹50 lakh | 0.1% | 0.1% |\n\n"
            "**Important:** Non-deduction leads to **30% disallowance** of expenditure under "
            "Section 40(a)(ia).\n\n"
            "📌 *Source: CBDT Circular No. 12/2025*"
        ),
        "doc_id": "TR003",
    },
    "regime": {
        "keywords": ["new regime", "old regime", "old tax", "new tax", "regime comparison",
                      "which regime", "default regime", "rebate", "slab", "87a"],
        "answer": (
            "**New Tax Regime vs Old Tax Regime (FY 2025-26)**\n\n"
            "⚠️ The **New Regime is now the default**. Taxpayers must actively opt for Old Regime.\n\n"
            "**New Regime Slabs:**\n"
            "| Income | Rate |\n"
            "|--------|------|\n"
            "| 0 – 3L | Nil |\n"
            "| 3 – 7L | 5% |\n"
            "| 7 – 10L | 10% |\n"
            "| 10 – 12L | 15% |\n"
            "| 12 – 15L | 20% |\n"
            "| > 15L | 30% |\n\n"
            "**Old Regime Slabs:**\n"
            "| Income | Rate |\n"
            "|--------|------|\n"
            "| 0 – 2.5L | Nil |\n"
            "| 2.5 – 5L | 5% |\n"
            "| 5 – 10L | 20% |\n"
            "| > 10L | 30% |\n\n"
            "**Key differences:**\n"
            "• New Regime: Standard deduction ₹75,000 (revised from ₹50,000)\n"
            "• New Regime: Rebate u/s 87A up to ₹60,000 (income ≤ ₹12L)\n"
            "• Old Regime: Rebate u/s 87A = ₹12,500\n"
            "• Health & Education Cess: 4% on both regimes\n\n"
            "📌 *Source: Finance Act 2025*"
        ),
        "doc_id": "TR004",
    },
    "filing": {
        "keywords": ["filing deadline", "due date", "gstr-1", "gstr-3b", "gstr-9",
                      "itr", "late fee", "penalty", "filing date", "return due"],
        "answer": (
            "**GST & Income Tax Filing Deadlines**\n\n"
            "**GST Returns:**\n"
            "| Return | Deadline | Late Fee |\n"
            "|--------|----------|----------|\n"
            "| GSTR-1 (outward supplies) | 11th of following month | ₹50/day |\n"
            "| GSTR-3B (summary return) | 20th of following month | ₹50/day |\n"
            "| GSTR-9 (Annual return) | 31st December | 0.25% of turnover |\n"
            "| GSTR-9C (Reconciliation) | 31st December (turnover > ₹5Cr) | 0.25% |\n\n"
            "**Late fee cap:** 10% of tax liability or ₹10,000, whichever is higher.\n\n"
            "**Income Tax Returns:**\n"
            "| Category | Deadline | Late Fee (Section 234F) |\n"
            "|----------|----------|------------------------|\n"
            "| Non-audit | 31st July | ₹5,000 (income > ₹5L) |\n"
            "| Audit required | 30th September | ₹5,000 (income > ₹5L) |\n"
            "| Small taxpayers | 31st July | ₹1,000 (income ≤ ₹5L) |\n\n"
            "**Interest on delayed payment:** 18% p.a. (GST), 1% per month (IT Act)\n\n"
            "📌 *Source: CGST Act Section 47*"
        ),
        "doc_id": "TR005",
    },
    "transfer_pricing": {
        "keywords": ["transfer pricing", "section 92", "alp", "arm's length", "beps",
                      "transfer price", "international transaction", "cbcr"],
        "answer": (
            "**Transfer Pricing - Section 92**\n\n"
            "Transfer pricing provisions apply to:\n"
            "• **International transactions** exceeding ₹1 crore\n"
            "• **Specified domestic transactions** exceeding ₹1 crore\n\n"
            "**Methods to determine Arm's Length Price (ALP):**\n"
            "1. **Comparable Uncontrolled Price (CUP)**\n"
            "2. **Resale Price Method (RPM)**\n"
            "3. **Cost Plus Method (CPM)**\n"
            "4. **Transactional Net Margin Method (TNMM)**\n\n"
            "**Compliance requirements:**\n"
            "• Transfer pricing documentation under Section 92D\n"
            "• Form 3CEB filing\n"
            "• Country-by-Country Reporting (CbCR) for MNEs with revenue > €750M (BEPS Action 13)\n\n"
            "**Penalty for non-compliance:** 2% of transaction value under Section 271BA\n\n"
            "📌 *Source: Income Tax Act, 1961 - Chapter X*"
        ),
        "doc_id": "TR006",
    },
    "itc": {
        "keywords": ["itc", "input tax credit", "blocked credits", "rule 36",
                      "credit reversal", "section 16", "rule 42", "rule 43"],
        "answer": (
            "**Input Tax Credit (ITC) Rules - GST**\n\n"
            "**Conditions for claiming ITC (Section 16):**\n"
            "1. Possession of tax invoice or debit note\n"
            "2. Goods or services received\n"
            "3. Tax actually paid to government\n"
            "4. Return filed under Section 39\n\n"
            "**ITC Time Limit:** Within **30th November** of the year following the FY.\n\n"
            "**Rule 36(4):** ITC restricted to **105%** of eligible credit in GSTR-2B.\n\n"
            "**Blocked Credits (Section 17(5)) - NO ITC allowed for:**\n"
            "• Food & beverages, outdoor catering\n"
            "• Beauty treatment, health services, cosmetic surgery\n"
            "• Club/health/fitness centre membership\n"
            "• Travel benefits to employees on vacation\n"
            "• Works contract for immovable property (except for further supply)\n"
            "• Motor vehicles for personal use\n\n"
            "**ITC reversal** required for exempt supplies under Rule 42/43.\n\n"
            "📌 *Source: CGST Act Section 16 & Rule 36*"
        ),
        "doc_id": "TR007",
    },
    "capital_gains": {
        "keywords": ["capital gains", "stcg", "ltcg", "111a", "112a", "section 54",
                      "section 54ec", "long term", "short term", "indexation"],
        "answer": (
            "**Capital Gains Taxation (FY 2025-26)**\n\n"
            "**Equity / Equity-oriented Mutual Funds:**\n"
            "| Type | Holding | Rate | Section |\n"
            "|------|---------|------|---------|\n"
            "| STCG (listed) | ≤ 12 months | 20% + 4% cess = **20.8%** | 111A |\n"
            "| LTCG (listed) | > 12 months | 12.5% + 4% cess (above ₹1.25L) | 112A |\n\n"
            "**Unlisted Securities & Immovable Property:**\n"
            "| Type | Holding | Rate |\n"
            "|------|---------|------|\n"
            "| STCG | ≤ 24/36 months | At slab rates |\n"
            "| LTCG | > 24/36 months | 20% with indexation |\n\n"
            "**Key Exemptions:**\n"
            "• **Section 54:** Invest in 1 residential house in India — max ₹10 crore exemption\n"
            "• **Section 54EC:** Invest in NHAI/REC/IRFC bonds within 6 months — max ₹50 lakh\n\n"
            "📌 *Source: Income Tax Act, 1961 - Sections 111A, 112A*"
        ),
        "doc_id": "TR008",
    },
}

# ── Broad Greeting / Generic Query Templates ─────────────────

GENERIC_TAX_TOPICS = {
    "greeting": {
        "keywords": ["hello", "hi", "hey", "good morning", "good evening", "help",
                      "what can you do", "how to use"],
        "answer": (
            "👋 **Welcome to the AI Tax Search Assistant!**\n\n"
            "I can help you with Indian tax queries across these areas:\n\n"
            "• 📋 **Income Tax** — Section 80C, New vs Old Regime, Capital Gains\n"
            "• 🏛️ **GST** — Rates, Filing Deadlines, ITC Rules\n"
            "• 💰 **TDS** — Rates, Sections 194A-194Q\n"
            "• 🔄 **Transfer Pricing** — Section 92, ALP Methods\n\n"
            "**Try asking:**\n"
            "• \"What are the GST rate slabs?\"\n"
            "• \"Compare New vs Old Tax Regime\"\n"
            "• \"TDS on contractor payments\"\n"
            "• \"Section 80C deductions\"\n\n"
            "You can also upload PDF documents, tax guidelines, or client files "
            "to expand the knowledge base!"
        ),
    },
    "gst_general": {
        "keywords": ["gst", "goods and services tax", "gst registration", "gst number",
                      "gstin", "gst council", "gst composition", "gst exemption",
                      "gst return", "gst payment"],
        "answer": (
            "**GST Overview**\n\n"
            "**Registration:** Mandatory if aggregate turnover exceeds ₹40 lakh (goods) / "
            "₹20 lakh (services) in most states.\n\n"
            "**Returns:**\n"
            "• GSTR-1: Due 11th of following month (outward supplies)\n"
            "• GSTR-3B: Due 20th of following month (summary return)\n"
            "• GSTR-9: Annual return by 31st December\n\n"
            "**Rate slabs:** 0%, 5%, 12%, 18%, 28%\n\n"
            "**GSTIN format:** 2-digit state code + 10-char PAN + 1 entity digit + Z + checksum\n\n"
            "Ask me about specific GST rates, ITC rules, or filing deadlines for more detail!"
        ),
    },
    "tax_planning": {
        "keywords": ["tax planning", "save tax", "how to reduce tax", "tax saving",
                      "minimize tax", "tax optimization", "tax efficient"],
        "answer": (
            "**Tax Planning Strategies (FY 2025-26)**\n\n"
            "**Under New Regime (default):**\n"
            "• Standard deduction of ₹75,000\n"
            "• Rebate u/s 87A: Income up to ₹12L = NIL tax\n"
            "• No deductions under 80C, 80D, HRA etc.\n\n"
            "**Under Old Regime (opt-in):**\n"
            "• Section 80C: Up to ₹1.5L (PPF, ELSS, EPF, Insurance, NSC)\n"
            "• Section 80D: Health insurance premium\n"
            "• HRA exemption if applicable\n"
            "• Home loan interest deduction\n\n"
            "**Key tip:** Compare both regimes using your actual income and "
            "investments before choosing. The New Regime is default, so "
            "you must file Form 10-IEA to opt for Old Regime.\n\n"
            "For a detailed comparison, ask: \"Compare New vs Old Tax Regime\""
        ),
    },
    "it_return": {
        "keywords": ["itr", "income tax return", "file return", "return filing",
                      "itr form", "itr-1", "itr-2", "itr-3", "itr-4", "itr due date"],
        "answer": (
            "**Income Tax Return Filing**\n\n"
            "**Deadlines:**\n"
            "• 31st July: Non-audit cases\n"
            "• 30th September: Audit required cases\n\n"
            "**Late fees (Section 234F):**\n"
            "• Income > ₹5L: ₹5,000\n"
            "• Income ≤ ₹5L: ₹1,000\n\n"
            "**Common ITR forms:**\n"
            "• ITR-1 (Sahaj): Salary, one house, other sources (income ≤ ₹50L)\n"
            "• ITR-2: Capital gains, multiple houses, foreign income\n"
            "• ITR-3: Business/profession income\n"
            "• ITR-4 (Sugam): Presumptive business income\n\n"
            "**Interest on late payment:** 1% per month under Section 234A/B/C\n\n"
            "📌 *Source: Income Tax Act, 1961*"
        ),
    },
}


class RAGEngine:
    """Offline RAG pipeline for tax knowledge search with smart responses."""

    def __init__(self):
        self.documents = list(TAX_RULES_KB)
        self.user_documents: list[dict] = []  # dynamically added from uploads
        self.conversation_history: list[dict] = []

    # ── Knowledge Base Management ─────────────────────────────

    def add_document(self, title: str, content: str, source: str = "User Upload",
                     tags: Optional[list[str]] = None) -> dict:
        """Add a user-uploaded document to the dynamic knowledge base."""
        doc_id = f"USER{len(self.user_documents) + 1:03d}"
        doc = {
            "doc_id": doc_id,
            "title": title,
            "source": source,
            "content": content,
            "tags": tags or self._auto_tag(content),
        }
        self.user_documents.append(doc)
        return {"doc_id": doc_id, "title": title}

    def _auto_tag(self, content: str) -> list[str]:
        """Auto-generate tags from document content."""
        content_lower = content.lower()
        tag_map = {
            "gst": ["GST", "goods and services tax"],
            "tds": ["TDS", "tax deducted at source"],
            "income tax": ["income tax", "tax"],
            "section 80c": ["80C", "deductions"],
            "capital gains": ["capital gains", "STCG", "LTCG"],
            "invoice": ["invoice", "billing"],
            "salary": ["salary", "payroll"],
            "bank": ["bank", "banking"],
        }
        tags = set()
        for kw, tag_list in tag_map.items():
            if kw in content_lower:
                tags.update(tag_list)
        return list(tags) if tags else ["general"]

    def get_all_documents(self) -> list[dict]:
        """Return combined knowledge base (built-in + user uploads)."""
        return self.documents + self.user_documents

    # ── Relevance Scoring ─────────────────────────────────────

    def _compute_relevance(self, query: str, doc: dict) -> float:
        """Compute enhanced keyword-based relevance score."""
        query_lower = query.lower()
        query_words = set(query_lower.split())

        # Remove common stop words
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "shall", "may", "can", "could", "would", "should", "what",
            "how", "when", "where", "who", "which", "under", "about",
            "for", "in", "on", "of", "to", "and", "or", "not", "with",
            "tell", "me", "give", "show", "explain", "define",
        }
        query_words -= stop_words

        if not query_words:
            return 0.0

        searchable = (
            doc["title"].lower() + " " +
            doc["content"].lower() + " " +
            " ".join(doc.get("tags", []))
        )

        # Base score: fraction of query words found
        matches = sum(1 for w in query_words if w in searchable)
        base_score = matches / len(query_words)

        # Boost for tag matches (weighted higher)
        tag_matches = sum(1 for tag in doc.get("tags", []) if tag.lower() in query_lower)
        tag_bonus = min(tag_matches * 0.2, 0.35)

        # Boost for exact title match
        title_bonus = 0.0
        for word in query_words:
            if len(word) > 2 and word in doc["title"].lower():
                title_bonus += 0.08

        # Boost for consecutive word matches (phrase proximity)
        phrase_bonus = 0.0
        query_list = sorted(query_words)
        for i in range(len(query_list) - 1):
            w1, w2 = query_list[i], query_list[i + 1]
            if w1 in searchable and w2 in searchable:
                # Check if they appear within 50 chars of each other
                idx1 = searchable.find(w1)
                idx2 = searchable.find(w2)
                if idx1 >= 0 and idx2 >= 0 and abs(idx1 - idx2) < 50:
                    phrase_bonus += 0.05

        # Bonus for user-uploaded documents (more relevant to user context)
        user_bonus = 0.05 if doc.get("doc_id", "").startswith("USER") else 0.0

        return min(base_score + tag_bonus + title_bonus + phrase_bonus + user_bonus, 1.0)

    def search(self, query: str, top_k: int = 3) -> list[dict]:
        """Search the combined knowledge base for relevant documents."""
        all_docs = self.get_all_documents()
        scored = []
        for doc in all_docs:
            score = self._compute_relevance(query, doc)
            if score > 0.08:
                scored.append({"doc": doc, "score": round(score, 3)})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]

    # ── Intent Detection ──────────────────────────────────────

    def _detect_intent(self, query: str) -> Optional[dict]:
        """Detect user intent from query and return matching intent template."""
        query_lower = query.lower().strip()

        # Check specific tax topic intents first
        for intent_id, intent in INTENT_PATTERNS.items():
            keyword_hits = sum(1 for kw in intent["keywords"] if kw in query_lower)
            if keyword_hits >= 2 or (keyword_hits >= 1 and len(query_lower.split()) <= 5):
                return {
                    "id": intent_id,
                    "answer": intent["answer"],
                    "doc_id": intent["doc_id"],
                    "confidence": min(0.6 + keyword_hits * 0.15, 0.95),
                }

        # Check generic topic intents
        for intent_id, intent in GENERIC_TAX_TOPICS.items():
            keyword_hits = sum(1 for kw in intent["keywords"] if kw in query_lower)
            if keyword_hits >= 2 or (keyword_hits >= 1 and len(query_lower.split()) <= 5):
                return {
                    "id": intent_id,
                    "answer": intent["answer"],
                    "doc_id": None,
                    "confidence": min(0.5 + keyword_hits * 0.12, 0.85),
                }

        return None

    # ── Answer Generation ─────────────────────────────────────

    def _build_answer_from_docs(self, query: str, results: list[dict]) -> str:
        """Build a synthesized answer from retrieved documents instead of dumping raw content."""
        if not results:
            return ""

        parts = []

        # Direct answer preamble
        parts.append("Based on the tax knowledge base, here's what I found:\n")

        for i, r in enumerate(results, 1):
            doc = r["doc"]
            content = doc["content"]

            # Extract the most relevant sentences from the document
            relevant_sentences = self._extract_relevant_sentences(query, content)
            if relevant_sentences:
                summary = " ".join(relevant_sentences[:5])
            else:
                # Fallback: take first 2 sentences
                sentences = re.split(r'(?<=[.!?])\s+', content)
                summary = " ".join(sentences[:2])

            parts.append(f"**{i}. {doc['title']}**")
            parts.append(f"*Source: {doc['source']}*\n")
            parts.append(f"{summary}\n")

        if len(results) > 1:
            parts.append(
                "\n*Multiple sources matched your query. Review all references "
                "for complete guidance. For specific compliance advice, consult a qualified CA.*"
            )

        return "\n".join(parts)

    def _extract_relevant_sentences(self, query: str, content: str) -> list[str]:
        """Extract sentences from content that are most relevant to the query."""
        query_words = set(query.lower().split())
        sentences = re.split(r'(?<=[.!?])\s+', content)

        scored_sentences = []
        for sent in sentences:
            sent_lower = sent.lower()
            hits = sum(1 for w in query_words if len(w) > 2 and w in sent_lower)
            if hits > 0:
                scored_sentences.append((hits, sent.strip()))

        scored_sentences.sort(key=lambda x: x[0], reverse=True)
        return [s for _, s in scored_sentences]

    def _build_fallback_answer(self, query: str) -> str:
        """Build a helpful fallback answer when no direct match is found."""
        topics_list = (
            "Currently loaded topics include:\n"
            "• Income Tax deductions (Section 80C)\n"
            "• GST rate structure & HSN codes\n"
            "• TDS rates for FY 2025-26\n"
            "• New vs Old Tax Regime comparison\n"
            "• GST filing deadlines & penalties\n"
            "• Transfer Pricing (Section 92)\n"
            "• GST Input Tax Credit (ITC) rules\n"
            "• Capital Gains taxation (STCG/LTCG)\n"
        )

        return (
            f"I couldn't find a specific answer for: *\"{query}\"*\n\n"
            f"{topics_list}\n"
            "**Tips for better results:**\n"
            "• Use specific terms like \"Section 80C\", \"TDS rates\", \"GST slabs\"\n"
            "• Try shorter queries: \"capital gains\" instead of \"what are the capital gains rules\"\n"
            "• Upload relevant PDF documents to expand the knowledge base\n\n"
            "💡 *For specific compliance advice, always consult a qualified Chartered Accountant.*"
        )

    # ── Main Response Generator ───────────────────────────────

    def generate_response(self, query: str) -> dict:
        """
        Generate a comprehensive AI response for a tax query.

        Priority:
        1. User-uploaded documents (highest relevance)
        2. Intent detection (direct answers for common queries)
        3. Knowledge base search (keyword matching)
        4. Fallback (helpful guidance)
        """
        query = query.strip()
        if not query:
            return {
                "answer": "Please enter a tax-related question to get started.",
                "sources": [],
                "confidence": 0.0,
            }

        # 1. Check intent detection first (gives direct, authoritative answers)
        intent = self._detect_intent(query)

        # 2. Search knowledge base (including user uploads)
        results = self.search(query, top_k=3)

        # 3. Build the best possible answer

        # If we have strong search results, use them
        if results and results[0]["score"] >= 0.4:
            answer = self._build_answer_from_docs(query, results)
            confidence = results[0]["score"]
            sources = [
                {"title": r["doc"]["title"], "source": r["doc"]["source"], "relevance": r["score"]}
                for r in results
            ]
            # If intent also matched, append extra context
            if intent and intent["doc_id"] != results[0]["doc"].get("doc_id"):
                answer += f"\n\n---\n\n{intent['answer']}"

        # If intent matched but search results are weak, use intent answer
        elif intent:
            answer = intent["answer"]
            confidence = intent["confidence"]
            # Also add any search results as supplementary info
            if results:
                answer += "\n\n---\n\n**Additional references from the knowledge base:**\n"
                for r in results[:2]:
                    answer += f"\n• **{r['doc']['title']}** ({r['doc']['source']})\n"
                    relevant = self._extract_relevant_sentences(query, r["doc"]["content"])
                    if relevant:
                        answer += f"  {relevant[0]}\n"
            sources = [
                {"title": r["doc"]["title"], "source": r["doc"]["source"], "relevance": r["score"]}
                for r in results
            ] if results else []

        # If we have some results but low scores, combine them
        elif results:
            answer = self._build_answer_from_docs(query, results)
            confidence = results[0]["score"]
            sources = [
                {"title": r["doc"]["title"], "source": r["doc"]["source"], "relevance": r["score"]}
                for r in results
            ]

        # Last resort: helpful fallback
        else:
            answer = self._build_fallback_answer(query)
            confidence = 0.0
            sources = []

        return {
            "answer": answer,
            "sources": sources,
            "confidence": round(confidence, 2),
        }

    # ── Conversation History ──────────────────────────────────

    def add_to_history(self, query: str, response: str):
        """Add Q&A to conversation history."""
        self.conversation_history.append({"query": query, "response": response})

    def get_history(self) -> list[dict]:
        """Return conversation history."""
        return self.conversation_history

    def clear_history(self):
        """Clear conversation history."""
        self.conversation_history = []
