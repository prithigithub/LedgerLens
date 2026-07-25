from prometheus_client import Counter, Gauge, Histogram

DOCUMENTS_PROCESSED = Counter(
    "ledgerlens_documents_total",
    "Total documents processed",
)

REVIEW_REQUIRED = Counter(
    "ledgerlens_review_total",
    "Documents sent to human review",
)

PROCESSING_TIME = Histogram(
    "ledgerlens_processing_seconds",
    "End-to-end invoice processing duration in seconds",
)

MODERATION_TIME = Histogram(
    "ledgerlens_moderation_seconds",
    "Image moderation latency in seconds",
)

EXTRACTION_TIME = Histogram(
    "ledgerlens_extraction_seconds",
    "Invoice extraction latency in seconds",
)

API_COST = Counter(
    "ledgerlens_cost_usd_total",
    "Estimated OpenAI API cost in USD",
)

ACTIVE_REVIEWS = Gauge(
    "ledgerlens_pending_reviews",
    "Current number of pending reviews",
)

CONFIDENCE_SCORE = Histogram(
    "ledgerlens_confidence",
    "Invoice confidence distribution",
)

MODERATION_VERDICTS = Counter(
    "ledgerlens_moderation_verdicts_total",
    "Moderation verdict distribution",
    ["verdict"],
)
