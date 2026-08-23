import asyncio
import logging
import datetime

logger = logging.getLogger("portfolio.email_service")

async def send_contact_notification(name: str, email: str, subject: str, message: str, client_ip: str | None = None):
    """
    Simulated Asynchronous Background Task:
    In production, this would integrate with SendGrid / Resend / AWS SES / SMTP.
    FastAPI executes this in the background without blocking the HTTP response.
    """
    logger.info(f"[BACKGROUND TASK INITIATED] Processing contact email from '{name}' <{email}>...")
    
    # Simulate network latency of sending an email asynchronously
    await asyncio.sleep(0.5)
    
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    notification_body = f"""
    ===============================================================
    NEW PORTFOLIO CONTACT MESSAGE RECEIVED!
    ===============================================================
    Timestamp: {timestamp}
    From:      {name}
    Email:     {email}
    IP:        {client_ip or 'Unknown'}
    Subject:   {subject}
    ---------------------------------------------------------------
    Message:
    {message}
    ===============================================================
    """
    print(notification_body)
    logger.info(f"[BACKGROUND TASK COMPLETED] Email alert successfully sent to portfolio owner for inquiry from {email}!")
