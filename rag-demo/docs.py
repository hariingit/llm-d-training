DOCUMENTS = [
    {
        "id": "inc-001",
        "text": "Incident 2026-03-01: Multiple failed login attempts detected from IP 203.0.113.44 "
                "against the VPN gateway, 47 attempts in 5 minutes. Account 'jsmith' was "
                "temporarily locked. Source IP geolocated to a known Tor exit node. "
                "Classified as brute-force credential stuffing attempt.",
    },
    {
        "id": "inc-002",
        "text": "Incident 2026-03-03: Phishing email delivered to 12 employees in the finance "
                "department, subject 'Urgent: Invoice Payment Overdue'. Link led to a fake "
                "Office 365 login page hosted on a lookalike domain. 2 employees clicked the "
                "link; no credentials were confirmed submitted. Domain has been blocked at "
                "the email gateway.",
    },
    {
        "id": "inc-003",
        "text": "Incident 2026-03-05: Unusual outbound data transfer detected from database "
                "server db-prod-03, approximately 2.3GB transferred to an external IP over "
                "port 443 outside normal business hours. Server owner confirmed no scheduled "
                "backup job at that time. Investigation ongoing, server isolated from network.",
    },
    {
        "id": "inc-004",
        "text": "Incident 2026-03-06: Ransomware indicators detected on workstation WS-0231 "
                "belonging to the accounting team. Multiple files renamed with .locked "
                "extension. Endpoint isolated automatically by EDR within 90 seconds of "
                "detection. No evidence of lateral movement found so far.",
    },
    {
        "id": "inc-005",
        "text": "Incident 2026-03-08: A misconfigured S3 bucket was found publicly accessible, "
                "containing customer support ticket exports with names and email addresses. "
                "No financial or authentication data was exposed. Bucket permissions have "
                "been corrected and access logs are being reviewed for prior unauthorized access.",
    },
]
