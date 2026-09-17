async def send_budget_alert_email(ctx, user_email: str, category_name: str, spent: float, limit: float):
    import asyncio
    await asyncio.sleep(2)
    
    print("\n" + "="*50)
    print(" EMAIL ALERT SENT!")
    print(f"To: {user_email}")
    print(f"Subject: Budget Exceeded for {category_name}")
    print(f"Message: You have spent ${spent:.2f} out of your ${limit:.2f} budget.")
    print("="*50 + "\n")