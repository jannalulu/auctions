from dotenv import load_dotenv
from anthropic import Anthropic
import pandas as pd
import os

load_dotenv() 

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

def get_claude_choice(scenario, endowment=""):
    prompt = f"{endowment}\n\nYou are Person B in the following scenario:\n{scenario}\n\nWhich option do you choose, Left or Right? Do not say anything other than Left or Right."
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1024,
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    choice = response.content[0].text.strip().lower()
    print(f"Claude's response: {response.content[0].text}")
    return "Left" if "left" in choice else "Right"

scenarios = [
    ("Barc2", "Left: Person A gets 400, Person B gets 400\n\nRight: Person A gets 750, Person B gets 375"),
    ("Barc8", "Left: Person A gets 300, Person B gets 600\n\nRight: Person A gets 700, Person B gets 500"),
    ("Berk15", "Left: Person A gets 200, Person B gets 700\n\nRight: Person A gets 600, Person B gets 600"),
    ("Berk23", "Left: Person A gets 800, Person B gets 200\n\nRight: Person A gets 0, Person B gets 0"),
    ("Berk26", "Left: Person A gets 0, Person B gets 800\n\nRight: Person A gets 400, Person B gets 400"),
    ("Berk29", "Left: Person A gets 400, Person B gets 400\n\nRight: Person A gets 750, Person B gets 400"),
]

endowments = [
    "",
    "You only care about fairness between players.",
    "You only care about the total pay-off of both players.",
    "You only care about your own pay-off."
]

results = []

for endowment in endowments:
    for name, scenario in scenarios:
        choice = get_claude_choice(scenario, endowment)
        results.append({
            "Scenario": name,
            "Endowment": endowment if endowment else "None",
            "Choice": choice
        })

df = pd.DataFrame(results)
print(df)

# Calculate the fraction choosing "Left" for each scenario and endowment
summary = df.groupby(["Scenario", "Endowment"])["Choice"].apply(lambda x: (x == "Left").mean()).reset_index()
summary = summary.pivot(index="Scenario", columns="Endowment", values="Choice")
print(summary)