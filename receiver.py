import time
from tools import SynapseInterface
from config import *
import evaluate

def main():
    synapse_interface = SynapseInterface(API_KEY)

    print("Starting the evaluation loop...")
    print(f"Checking for new submissions every {CHECK_INTERVAL} seconds...")

    while True:
        print("Checking for new submissions...")
        
        for challenge_name, challenge_id in CHALLENGE_IDS.items():
            received_subs = synapse_interface.get_submission_IDs(challenge_id)
            for sub_id in received_subs:
                    print(f"Evaluating submission {sub_id} from challenge {challenge_id}, {challenge_name}")
                    evaluate.run(synapse_interface, challenge_name, sub_id)
        
        print("Evaluation cycle completed.")
        print("Waiting for the next cycle...")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()