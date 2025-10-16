import smtplib
import ssl

# --- IMPORTANT: Fill in your details here ---
SENDER_EMAIL = "gowrikamahesh2025@gmail.com"
APP_PASSWORD = "whjh mrks dvil bueq"
RECIPIENT_EMAIL = "gowrikamahesh2025@gmail.com" # Sending to yourself for a test
# -----------------------------------------

# Using port 465 for a direct SSL connection
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465 

print("Attempting a direct SSL connection on port 465...")

try:
    context = ssl.create_default_context()
    # Use SMTP_SSL for a direct secure connection
    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
        print("Secure connection established. Logging in...")
        server.login(SENDER_EMAIL, APP_PASSWORD)
        
        print("Login successful! Sending test email...")
        server.sendmail(
            SENDER_EMAIL,
            RECIPIENT_EMAIL,
            "Subject: Python SSL Test (Port 465)\n\nThis is a test email."
        )
        print("✅ Email sent successfully!")

except Exception as e:
    print("\n An error occurred:")
    print(e)