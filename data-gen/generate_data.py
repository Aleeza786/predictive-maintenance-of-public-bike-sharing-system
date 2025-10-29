"""
generate_data.py

Generates realistic sample CSVs and SQL for:
 - bikes.csv
 - rides.csv
 - maintenance_records.csv
 - bike_scores.csv
 - train.csv / test.csv (for model training/evaluation)
 - sample_data.sql (INSERT statements to load into PostgreSQL)

Usage:
  python generate_data.py

Requirements:
  pip install pandas numpy
"""

import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

OUTDIR = os.path.abspath(os.path.dirname(__file__))

# Config
N_BIKES = 50
N_RIDES = 2000
START_DATE = datetime(2025, 9, 1)
END_DATE = datetime(2025, 10, 20)   # recent dates
COMPONENTS = ["brakes", "chain", "tires"]

# Utilities
def random_date(start, end):
    delta = end - start
    sec = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=sec)

def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)

def gen_bikes(n):
    rows = []
    for bike_id in range(1, n+1):
        last_serviced = START_DATE + timedelta(days=random.randint(0, 60))
        status = random.choice(["active", "maintenance_due"])
        rows.append({"bike_id": bike_id, "status": status, "last_serviced_date": last_serviced.date().isoformat()})
    return pd.DataFrame(rows)

def gen_rides(n_rides, n_bikes):
    rows = []
    for ride_id in range(1, n_rides+1):
        bike_id = random.randint(1, n_bikes)
        ride_ts = random_date(START_DATE, END_DATE)
        duration = round(random.uniform(5, 60), 2)  # minutes
        distance = round(max(0.5, duration * random.uniform(0.08, 0.15)), 2)  # km roughly proportional
        # avg_vibration higher for older bikes / noisy rides
        avg_vibration = round(random.gauss(0.15, 0.07), 3)
        if avg_vibration < 0.02: avg_vibration = 0.02
        avg_speed = round(distance / (duration/60 + 1e-6), 2)  # km/h
        # random end coords around a city (example lat/lng ~ New Delhi for realism)
        lat = round(28.60 + random.uniform(-0.03, 0.03), 6)
        lng = round(77.20 + random.uniform(-0.03, 0.03), 6)
        rows.append({
            "ride_id": ride_id,
            "bike_id": bike_id,
            "ride_timestamp": ride_ts.isoformat(),
            "ride_duration": duration,
            "distance": distance,
            "avg_vibration": avg_vibration,
            "avg_speed": avg_speed,
            "end_lat": lat,
            "end_lng": lng
        })
    return pd.DataFrame(rows)

def gen_maintenance_records(n_bikes):
    rows = []
    rec_id = 1
    # For some bikes insert recent maintenance events (so labels form realistically)
    for bike_id in range(1, n_bikes+1):
        # each bike has 0-2 maintenance records in last 60 days
        for _ in range(random.choices([0,1,2], weights=[0.6,0.3,0.1])[0]):
            days_ago = random.randint(0, 60)
            date = END_DATE - timedelta(days=days_ago)
            component = random.choice(COMPONENTS)
            rows.append({
                "record_id": rec_id,
                "bike_id": bike_id,
                "maintenance_date": date.date().isoformat(),
                "component_failed": component
            })
            rec_id += 1
    return pd.DataFrame(rows)

def compute_bike_scores(rides_df, bikes_df):
    # Aggregate recent 30-day features per bike
    cutoff = END_DATE - timedelta(days=30)
    recent = rides_df[pd.to_datetime(rides_df["ride_timestamp"]) >= cutoff]
    agg = recent.groupby("bike_id").agg(
        num_rides_30d=("ride_id", "count"),
        avg_vibration_30d=("avg_vibration", "mean"),
        max_vibration_30d=("avg_vibration", "max"),
        total_distance_30d=("distance", "sum"),
        avg_duration_30d=("ride_duration", "mean"),
        avg_speed_30d=("avg_speed", "mean")
    ).reset_index().fillna(0)
    # days_since_service
    bikes_df2 = bikes_df.copy()
    bikes_df2["last_serviced_date"] = pd.to_datetime(bikes_df2["last_serviced_date"])
    bikes_df2["days_since_service"] = (pd.Timestamp(END_DATE.date()) - bikes_df2["last_serviced_date"]).dt.days
    merged = pd.merge(bikes_df2, agg, on="bike_id", how="left").fillna(0)
    # heuristic risk score (for sample data): combine vibration, days_since_service, and low rides
    def risk_row(r):
        vib = r["avg_vibration_30d"]
        days = r["days_since_service"]
        # normalize vib roughly between 0.02 - 0.5
        vib_score = min(max((vib - 0.02) / 0.48, 0.0), 1.0)
        days_score = min(days / 90.0, 1.0)
        rides_factor = 1.0 - min(r["num_rides_30d"] / 50.0, 1.0)  # fewer recent rides can slightly increase risk?
        base = 0.5*vib_score + 0.3*days_score + 0.2*rides_factor
        # component-specific probabilities (add small randomness)
        brakes = min(max(base + random.uniform(-0.1, 0.1), 0.01), 0.99)
        chain = min(max(base*0.9 + random.uniform(-0.12, 0.12), 0.01), 0.99)
        tires = min(max(base*1.05 + random.uniform(-0.12, 0.12), 0.01), 0.99)
        risk_score = np.mean([brakes, chain, tires])
        return pd.Series({
            "bike_id": int(r["bike_id"]),
            "brakes_prob": round(brakes, 3),
            "chain_prob": round(chain, 3),
            "tires_prob": round(tires, 3),
            "risk_score": round(risk_score, 3)
        })
    scores = merged.apply(risk_row, axis=1)
    return merged, scores

def build_train_test(merged_df, maintenance_df, scores_df):
    # For each bike create a row with features + targets (presence of maintenance for component in last 30 days)
    cutoff = END_DATE - timedelta(days=30)
    rows = []
    for _, r in merged_df.iterrows():
        bike_id = int(r["bike_id"])
        row = {
            "bike_id": bike_id,
            "num_rides_30d": int(r.get("num_rides_30d", 0)),
            "avg_vibration_30d": float(round(r.get("avg_vibration_30d", 0.0), 4)),
            "max_vibration_30d": float(round(r.get("max_vibration_30d", 0.0), 4)),
            "total_distance_30d": float(round(r.get("total_distance_30d", 0.0), 3)),
            "avg_duration_30d": float(round(r.get("avg_duration_30d", 0.0), 3)),
            "avg_speed_30d": float(round(r.get("avg_speed_30d", 0.0), 3)),
            "days_since_service": int(r.get("days_since_service", 0))
        }
        # targets: whether maintenance_records exist in last 30 days for that component
        for comp in COMPONENTS:
            recent = maintenance_df[
                (pd.to_datetime(maintenance_df["maintenance_date"]) >= cutoff) &
                (maintenance_df["bike_id"] == bike_id) &
                (maintenance_df["component_failed"] == comp)
            ]
            row[f"target_{comp}"] = int(len(recent) > 0)
        rows.append(row)
    df = pd.DataFrame(rows).fillna(0)
    # simple 80/20 split by bike rows
    df_shuffled = df.sample(frac=1, random_state=42).reset_index(drop=True)
    n_test = max(1, int(len(df_shuffled) * 0.2))
    test = df_shuffled.iloc[:n_test]
    train = df_shuffled.iloc[n_test:]
    return train, test

def write_csv(df, path):
    df.to_csv(path, index=False)
    print("Wrote", path)

def write_sql(bikes_df, rides_df, maint_df, scores_df, outpath):
    lines = []
    lines.append("-- sample_data.sql - inserts for bikes, rides, maintenance_records, bike_scores")
    # bikes
    for _, r in bikes_df.iterrows():
        lines.append(f"INSERT INTO bikes (bike_id, status, last_serviced_date) VALUES ({int(r.bike_id)}, '{r.status}', '{r.last_serviced_date}');")
    # rides - limit columns to match schema
    for _, r in rides_df.iterrows():
        # escape values
        ts = r["ride_timestamp"]
        lines.append(f"INSERT INTO rides (ride_id, bike_id, ride_timestamp, ride_duration, distance, avg_vibration, avg_speed, end_lat, end_lng) VALUES ({int(r.ride_id)}, {int(r.bike_id)}, '{ts}', {r.ride_duration}, {r.distance}, {r.avg_vibration}, {r.avg_speed}, {r.end_lat}, {r.end_lng});")
    # maintenance
    for _, r in maint_df.iterrows():
        lines.append(f"INSERT INTO maintenance_records (record_id, bike_id, maintenance_date, component_failed) VALUES ({int(r.record_id)}, {int(r.bike_id)}, '{r.maintenance_date}', '{r.component_failed}');")
    # bike_scores
    for _, r in scores_df.iterrows():
        lines.append(f"INSERT INTO bike_scores (bike_id, brakes_prob, chain_prob, tires_prob, risk_score) VALUES ({int(r.bike_id)}, {r.brakes_prob}, {r.chain_prob}, {r.tires_prob}, {r.risk_score});")
    with open(outpath, "w") as f:
        f.write("\n".join(lines))
    print("Wrote SQL to", outpath)

def main():
    ensure_dir(OUTDIR)
    print("Generating bikes...")
    bikes_df = gen_bikes(N_BIKES)
    print("Generating rides...")
    rides_df = gen_rides(N_RIDES, N_BIKES)
    print("Generating maintenance records...")
    maint_df = gen_maintenance_records(N_BIKES)
    print("Computing scores...")
    merged, scores_df = compute_bike_scores(rides_df, bikes_df)
    print("Building train/test CSVs...")
    train_df, test_df = build_train_test(merged, maint_df, scores_df)

    # file paths
    bikes_csv = os.path.join(OUTDIR, "bikes.csv")
    rides_csv = os.path.join(OUTDIR, "rides.csv")
    maint_csv = os.path.join(OUTDIR, "maintenance_records.csv")
    scores_csv = os.path.join(OUTDIR, "bike_scores.csv")
    train_csv = os.path.join(OUTDIR, "train.csv")
    test_csv = os.path.join(OUTDIR, "test.csv")
    sql_file = os.path.join(OUTDIR, "sample_data.sql")

    # write CSVs
    write_csv(bikes_df, bikes_csv)
    write_csv(rides_df, rides_csv)
    write_csv(maint_df, maint_csv)
    write_csv(scores_df, scores_csv)
    write_csv(train_df, train_csv)
    write_csv(test_df, test_csv)

    # write SQL file
    write_sql(bikes_df, rides_df, maint_df, scores_df, sql_file)

    print("\nSample generation complete. Files saved to:", OUTDIR)
    print(" - bikes.csv, rides.csv, maintenance_records.csv, bike_scores.csv")
    print(" - train.csv, test.csv")
    print(" - sample_data.sql  (run with psql or in pgAdmin to populate DB)")

if __name__ == "__main__":
    main()
