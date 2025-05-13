import os

# Define the full backend folder and file structure
folders = [
    "app/api/routes",
    "app/core",
    "app/models",
    "app/services"
]

files = [
    "app/api/routes/backtest.py",
    "app/api/routes/strategies.py",
    "app/api/endpoints.py",
    "app/core/backtest_engine.py",
    "app/core/indicator_engine.py",
    "app/core/evaluator.py",
    "app/core/data_loader.py",
    "app/core/metrics.py",
    "app/core/config.py",
    "app/models/strategy_schema.py",
    "app/services/supabase_client.py",
    "app/services/result_formatter.py",
    "app/main.py"
]

def create_structure():
    created = []

    # Create folders
    for folder in folders:
        if not os.path.exists(folder):
            os.makedirs(folder)
            created.append(f"📁 Created folder: {folder}")

    # Create files
    for file in files:
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write("# Auto-generated file\n")
            created.append(f"📄 Created file: {file}")

    # Summary
    if created:
        print("\n✅ Setup Complete. Created:")
        for item in created:
            print(item)
    else:
        print("\n✅ All folders and files already exist. Nothing to do!")

if __name__ == "__main__":
    create_structure()
