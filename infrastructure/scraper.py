import boto3 # type: ignore
import os
import random
import time
from datetime import datetime

# Initialize DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    start_time = time.time()
    
    # --- PHASE 1: GENERATE MOCK DRAW RULES ---
    print("Phase 1: Simulating the Draw...")
    rules = generate_mock_draw()
    
    # --- PHASE 2: CALCULATE WINNING TICKETS ---
    print("Phase 2: Calculating all 37,000+ winning tickets...")
    winners_batch = []
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for i in range(100000):
        ticket_str = f"{i:05}"
        prize = 0
        category = ""

        # 1. MAIN PRIZES
        if ticket_str == rules['prize_1']:
            prize = 200000
            category = "El Gordo (1st Prize)"
        elif ticket_str == rules['prize_2']:
            prize = 75000
            category = "2nd Prize"
        elif ticket_str == rules['prize_3']:
            prize = 25000
            category = "3rd Prize"
            
        
        # 2. EXTRACTIONS
        # 4-Digit Extractions (Pays €350)
        elif any(ticket_str.endswith(t) for t in rules['term_4']):
            prize = 350
            category = "Extraction (4 Digits)"
            
        # 3-Digit Extractions (Pays €100)
        elif any(ticket_str.endswith(t) for t in rules['term_3']):
            prize = 100
            category = "Extraction (3 Digits)"
            
        # 2-Digit Extractions (Pays €40)
        elif any(ticket_str.endswith(t) for t in rules['term_2']):
            prize = 40
            category = "Extraction (2 Digits)"

        
        # Reintegro (Pays €20)
        elif any(ticket_str.endswith(t) for t in rules['reintegros']):
            prize = 20
            category = "Reintegro"

        
        # TEST TICKET
        if ticket_str == "14941": 
             prize = 200000
             category = "El Gordo (Test Mode)"

        # RECORD WINNER
        if prize > 0:
            winners_batch.append({
                'DrawDate': ticket_str,
                'Prize': f"€{prize:,}",
                'Category': category,
                'GeneratedAt': timestamp
            })

    # --- PHASE 3: WRITE WINNERS TO DYNAMODB ---
    print(f"Phase 3: Writing {len(winners_batch)} winners to DynamoDB...")
    
    with table.batch_writer() as batch:
        for item in winners_batch:
            batch.put_item(Item=item)

    duration = time.time() - start_time
    print(f"SUCCESS: Wrote {len(winners_batch)} items in {duration:.2f} seconds.")
    
    return {
        "status": "success", 
        "total_winners": len(winners_batch), 
        "duration_seconds": duration
    }

def generate_mock_draw():
    """
    Simulates the official 'El Niño' extraction structure.
    """
    return {
        "prize_1": f"{random.randint(0, 99999):05}",
        "prize_2": f"{random.randint(0, 99999):05}",
        "prize_3": f"{random.randint(0, 99999):05}",
        
        # 2 draws of 4 digits
        "term_4": [f"{random.randint(0, 9999):04}" for _ in range(2)],
        
        # 14 draws of 3 digits
        "term_3": [f"{random.randint(0, 999):03}" for _ in range(14)],
        
        # 5 draws of 2 digits
        "term_2": [f"{random.randint(0, 99):02}" for _ in range(5)],
        
        # 3 reintegros (last digit)
        "reintegros": [str(random.randint(0, 9)) for _ in range(3)]
    }