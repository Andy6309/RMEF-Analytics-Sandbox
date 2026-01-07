import random
import csv
from datetime import datetime, timedelta

random.seed(42)

# Campaign IDs from campaigns.csv
campaign_ids = [f'C{str(i).zfill(3)}' for i in range(1, 16)]

# Payment methods
payment_methods = ['Credit Card', 'Wire Transfer', 'Check', 'PayPal', 'ACH Transfer']

# Generate 500 donations from the 1000 donors
num_donations = 500
donations = []

# Donor IDs from the new donors.csv (D0001 to D1000)
donor_ids = [f'D{i:04d}' for i in range(1, 1001)]

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(1, num_donations + 1):
    donor_id = random.choice(donor_ids)
    campaign_id = random.choice(campaign_ids)
    
    # Amount distribution: mostly small, some medium, few large
    rand = random.random()
    if rand < 0.6:  # 60% small donations ($25-$500)
        amount = random.uniform(25, 500)
    elif rand < 0.9:  # 30% medium donations ($500-$5000)
        amount = random.uniform(500, 5000)
    else:  # 10% large donations ($5000-$100000)
        amount = random.uniform(5000, 100000)
    
    amount = round(amount, 2)
    
    # Random donation date
    donation_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    # Payment method
    payment_method = random.choice(payment_methods)
    
    # Recurring (20% chance)
    is_recurring = random.random() < 0.2
    
    # Notes
    notes_options = [
        'Annual membership renewal',
        'Monthly donation',
        'One-time contribution',
        'Habitat restoration support',
        'Conservation project funding',
        'Youth education program',
        'Elk research funding',
        'Land acquisition support',
        'Emergency wildlife support',
        ''
    ]
    notes = random.choice(notes_options)
    
    donations.append({
        'donation_id': f'DN{i:04d}',
        'donor_id': donor_id,
        'campaign_id': campaign_id,
        'amount': f'{amount:.2f}',
        'donation_date': donation_date.strftime('%Y-%m-%d'),
        'payment_method': payment_method,
        'is_recurring': is_recurring,
        'notes': notes
    })

# Write to CSV
with open('data/raw/donations.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['donation_id', 'donor_id', 'campaign_id', 'amount', 'donation_date', 
                  'payment_method', 'is_recurring', 'notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(donations)

print(f'Generated {num_donations} donations')

# Calculate statistics
total_amount = sum(float(d['amount']) for d in donations)
avg_amount = total_amount / num_donations
large_donations = sum(1 for d in donations if float(d['amount']) > 10000)
recurring = sum(1 for d in donations if d['is_recurring'])

print(f'\nDonation Statistics:')
print(f'  Total Amount: ${total_amount:,.2f}')
print(f'  Average Donation: ${avg_amount:,.2f}')
print(f'  Large Donations (>$10k): {large_donations}')
print(f'  Recurring Donations: {recurring} ({recurring/num_donations*100:.1f}%)')
