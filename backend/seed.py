"""CLI entry point: seed the database using the application package."""

from app.seed import SAMPLES, create_seed_data

if __name__ == "__main__":
    create_seed_data()
    print(f"Seed complete: {len(SAMPLES)} requirements and analyses are available.")
