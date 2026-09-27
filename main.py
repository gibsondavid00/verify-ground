import json
import os
import re

def load_evidence(path='evidence.txt'):
    if not os.path.exists(path):
        return {}
    data = {}
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or '|' not in line:
                continue
            key, value = line.split('|', 1)
            data[key.strip()] = value.strip()
    return data

def ai_claim():
    # Simulated AI generated claim
    return "The capital of France is Paris and the Eiffel Tower is 330 meters tall."

def extract_facts(claim):
    # Simple pattern: look for 'is' or 'are' key phrases
    facts = []
    sentences = re.split(r'(?<=[.!?]) ', claim)
    for s in sentences:
        m = re.search(r'(.+?)\s+is\s+(.+)', s)
        if m:
            facts.append((m.group(1).strip(), m.group(2).strip()))
    return facts

def verify_claim(claim, evidence):
    facts = extract_facts(claim)
    results = []
    for subject, value in facts:
        if subject in evidence:
            expected = evidence[subject]
            if value.lower() == expected.lower():
                results.append((subject, True, value, expected))
            else:
                results.append((subject, False, value, expected))
        else:
            results.append((subject, None, value, 'NO EVIDENCE'))
    return results

def main():
    evidence = load_evidence()
    if not evidence:
        # default evidence for demo
        evidence = {
            'capital of France': 'Paris',
            'Eiffel Tower height': '330 meters'
        }
    claim = ai_claim()
    print(f"AI Claim: {claim}")
    print("Verification results:")
    all_good = True
    for subj, ok, actual, expected in verify_claim(claim, evidence):
        status = "PASS" if ok else ("MISMATCH" if ok is False else "UNKNOWN")
        if ok is not True:
            all_good = False
        print(f"  - {subj}: {status} (got: {actual}, expected: {expected})")
    if all_good:
        print("All claims grounded in evidence.")
    else:
        print("Some claims need correction.")

if __name__ == "__main__":
    main()
