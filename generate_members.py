import random
import csv
from datetime import datetime, timedelta

random.seed(42)

# State distribution based on elk habitat (MT, WY, ID, CO are primary)
states = [
    ('MT', 0.18), ('WY', 0.12), ('ID', 0.12), ('CO', 0.15),
    ('OR', 0.08), ('WA', 0.08), ('NM', 0.06), ('AZ', 0.05),
    ('UT', 0.05), ('NV', 0.04), ('CA', 0.04), ('TX', 0.03)
]

# RMEF membership tiers with realistic distribution
# Supporting: 45%, Team Elk: 28%, Sportsman: 15%, Heritage: 8%, Life: 4%
tiers = [
    ('Supporting', 0.45, 35),
    ('Team Elk', 0.28, 50),
    ('Sportsman', 0.15, 100),
    ('Heritage', 0.08, 250),
    ('Life', 0.04, 1500)
]

first_names = [
    'James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Joseph',
    'Thomas', 'Christopher', 'Mary', 'Patricia', 'Jennifer', 'Linda', 'Elizabeth',
    'Barbara', 'Susan', 'Jessica', 'Sarah', 'Karen', 'Mark', 'Donald', 'Steven',
    'Paul', 'Andrew', 'Joshua', 'Kenneth', 'Kevin', 'Brian', 'George', 'Nancy',
    'Lisa', 'Betty', 'Margaret', 'Sandra', 'Ashley', 'Kimberly', 'Emily', 'Donna',
    'Michelle', 'Daniel', 'Matthew', 'Anthony', 'Ryan', 'Jason', 'Justin', 'Brandon',
    'Tyler', 'Aaron', 'Scott', 'Amanda', 'Stephanie', 'Nicole', 'Rachel', 'Megan'
]

last_names = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Wilson', 'Anderson', 'Thomas',
    'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Thompson', 'White', 'Harris',
    'Clark', 'Lewis', 'Robinson', 'Walker', 'Young', 'Allen', 'King', 'Wright',
    'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores', 'Green', 'Adams', 'Nelson',
    'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell', 'Carter', 'Roberts'
]

street_types = ['Rd', 'Dr', 'Ln', 'Way', 'St', 'Ave', 'Ct', 'Trl']
street_names = ['Elk', 'Mountain', 'Ridge', 'Valley', 'Creek', 'Trail', 'Canyon',
                'Peak', 'Meadow', 'Forest', 'River', 'Lake', 'Pine', 'Aspen']

# Generate 1000 members (scaled down from 235k for demo purposes)
num_members = 1000
members = []

start_date = datetime(2015, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(1, num_members + 1):
    state = random.choices([s[0] for s in states], weights=[s[1] for s in states])[0]
    tier_name, tier_prob, tier_price = random.choices(tiers, weights=[t[1] for t in tiers])[0]
    
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    email = f'{fname.lower()}.{lname.lower()}{random.randint(1,999)}@email.com'
    phone = f'{random.randint(200,999)}-555-{random.randint(1000,9999)}'
    
    # Random join date between 2015-2024
    join_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    
    street_num = random.randint(100, 9999)
    street_name = random.choice(street_names)
    street_type = random.choice(street_types)
    
    members.append({
        'donor_id': f'D{i:04d}',
        'first_name': fname,
        'last_name': lname,
        'email': email,
        'phone': phone,
        'address': f'{street_num} {street_name} {street_type}',
        'city': 'City',
        'state': state,
        'zip_code': f'{random.randint(10000, 99999)}',
        'donor_type': 'Individual',
        'join_date': join_date.strftime('%Y-%m-%d'),
        'membership_level': tier_name
    })

# Write to CSV
with open('data/raw/donors.csv', 'w', newline='', encoding='utf-8') as f:
    fieldnames = ['donor_id', 'first_name', 'last_name', 'email', 'phone', 'address',
                  'city', 'state', 'zip_code', 'donor_type', 'join_date', 'membership_level']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(members)

print(f'Generated {num_members} members')
print(f'\nMembership Distribution:')
for tier_name, _, _ in tiers:
    count = sum(1 for m in members if m['membership_level'] == tier_name)
    pct = (count / num_members) * 100
    print(f'  {tier_name}: {count} ({pct:.1f}%)')
