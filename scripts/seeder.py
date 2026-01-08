import boto3
import time

TABLE_NAME = "el-nino-2026-aws-results" 
REGION = "eu-west-1"

dynamodb = boto3.resource('dynamodb', region_name=REGION)
table = dynamodb.Table(TABLE_NAME)

def wipe_table():
    """Deletes all items in the table to start fresh."""
    print(f"🧹 Wiping table {TABLE_NAME}...")
    try:
        scan = table.scan()
        with table.batch_writer() as batch:
            for each in scan.get('Items', []):
                batch.delete_item(Key={'DrawDate': each['DrawDate']})
        print("✨ Table wiped successfully.")
    except Exception as e:
        print(f"⚠️ Error wiping table (it might be empty): {e}")

def seed_winners():
    """Uploads the OFFICIAL 2026 Prize List (Adjusted for DÉCIMO / €20 Ticket)."""
    print(f"💎 Seeding Winners...")

    # 1. MAJOR WINNERS
    winners = [
        {'DrawDate': '06703', 'Prize': '€200,000', 'Category': '1st Prize (El Gordo)'},
        {'DrawDate': '45875', 'Prize': '€75,000',  'Category': '2nd Prize'},
        {'DrawDate': '32615', 'Prize': '€25,000',  'Category': '3rd Prize'},
    ]

    # 2. TERMINATIONS
    
    # 4-Digit Terminations (€350 per decimo)
    term_4 = ['1829', '3682']
    
    # 3-Digit Terminations (€100 per decimo)
    term_3 = ['058', '156', '248', '325', '367', '400', '887']

    # 2-Digit Terminations (€40 per decimo)
    term_2 = ['27', '37', '44', '54', '94']

    # 3. REINTEGRO Examples (€20 per decimo)
    reintegros = [
        {'DrawDate': '10000', 'Prize': '€20', 'Category': 'Reintegro (Ends in 0)'},
        {'DrawDate': '11111', 'Prize': '€20', 'Category': 'Reintegro (Ends in 1)'},
        {'DrawDate': '33333', 'Prize': '€20', 'Category': 'Reintegro (Ends in 3)'}
    ]

    with table.batch_writer() as batch:
        # Upload Major Winners
        for w in winners:
            batch.put_item(Item=w)
            
        # Upload Terminations
        for t4 in term_4:
            batch.put_item(Item={'DrawDate': t4, 'Prize': '€350', 'Category': '4-Digit Termination'})
        for t3 in term_3:
            batch.put_item(Item={'DrawDate': t3, 'Prize': '€100', 'Category': '3-Digit Termination'})
        for t2 in term_2:
            batch.put_item(Item={'DrawDate': t2, 'Prize': '€40', 'Category': '2-Digit Termination'})

        # Upload Reintegros
        for r in reintegros:
            batch.put_item(Item=r)

    print(f"✅ Database seeded! Verified 1st Prize: 06703 (€200,000)")

if __name__ == '__main__':
    wipe_table()
    seed_winners()