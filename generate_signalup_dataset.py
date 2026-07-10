import numpy as np
import pandas as pd
import json
from pathlib import Path
from sklearn.model_selection import train_test_split


RANDOM_SEED = 42
N_ROWS = 100000
OUTPUT_DIR = Path("data")

np.random.seed(RANDOM_SEED)


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate_dataset(n_rows: int = N_ROWS):
    account_ids = [f"ACC{str(i).zfill(7)}" for i in range(1, n_rows + 1)]

    account_type = np.random.choice(
        ["Individual", "Small Business", "Enterprise"],
        size=n_rows,
        p=[0.55, 0.30, 0.15]
    )

    company_size = np.random.choice(
        ["1-10", "11-50", "51-200", "201-1000", "1000+"],
        size=n_rows,
        p=[0.35, 0.25, 0.20, 0.12, 0.08]
    )

    industry = np.random.choice(
        ["Smart Home", "Healthcare IoT", "Industrial IoT", "Agriculture IoT",
         "Fleet Management", "Energy Monitoring", "Retail IoT"],
        size=n_rows
    )

    region = np.random.choice(
        ["South", "North", "West", "East", "Central"],
        size=n_rows,
        p=[0.30, 0.25, 0.20, 0.15, 0.10]
    )

    country = np.random.choice(
        ["India", "USA", "UK", "Germany", "Singapore"],
        size=n_rows,
        p=[0.45, 0.25, 0.10, 0.10, 0.10]
    )

    customer_tenure_days = np.random.randint(15, 1800, n_rows)

    current_subscription = np.random.choice(
        ["Free", "Basic", "Standard"],
        size=n_rows,
        p=[0.55, 0.30, 0.15]
    )

    subscription_age_days = np.minimum(
        customer_tenure_days,
        np.random.randint(10, 1500, n_rows)
    )

    trial_used = np.random.choice([0, 1], size=n_rows, p=[0.35, 0.65])
    trial_days_used = np.where(trial_used == 1, np.random.randint(1, 31, n_rows), 0)

    previous_upgrade_count = np.random.poisson(0.35, n_rows)
    previous_downgrade_count = np.random.poisson(0.15, n_rows)

    auto_renew_enabled = np.random.choice([0, 1], size=n_rows, p=[0.35, 0.65])

    monthly_subscription_fee = np.select(
        [
            current_subscription == "Free",
            current_subscription == "Basic",
            current_subscription == "Standard"
        ],
        [
            0,
            np.random.uniform(9, 29, n_rows),
            np.random.uniform(30, 79, n_rows)
        ]
    )

    base_hardware = np.random.choice(
        ["Starter Hub", "Smart Sensor Kit", "Industrial Gateway", "Fleet Tracker", "Energy Monitor"],
        size=n_rows
    )

    connected_device_count = np.random.poisson(4, n_rows) + 1
    connected_device_count = np.where(account_type == "Enterprise", connected_device_count + np.random.randint(5, 25, n_rows), connected_device_count)
    connected_device_count = np.where(account_type == "Small Business", connected_device_count + np.random.randint(2, 10, n_rows), connected_device_count)

    active_device_count = np.maximum(
        1,
        connected_device_count - np.random.poisson(1, n_rows)
    )

    offline_device_count = connected_device_count - active_device_count

    device_health_score = np.clip(np.random.normal(78, 14, n_rows), 20, 100)
    firmware_version = np.random.choice(["v1.0", "v1.5", "v2.0", "v2.5", "v3.0"], size=n_rows)
    avg_device_uptime_percentage = np.clip(np.random.normal(92, 7, n_rows), 50, 100)
    avg_battery_level = np.clip(np.random.normal(72, 18, n_rows), 5, 100)

    avg_monthly_data_usage_gb = np.clip(
        connected_device_count * np.random.uniform(1.5, 8.5, n_rows),
        0.5,
        500
    )

    avg_daily_usage_minutes = np.clip(
        np.random.normal(45, 25, n_rows) + connected_device_count * 2,
        1,
        240
    )

    avg_session_duration_minutes = np.clip(np.random.normal(18, 9, n_rows), 1, 90)

    weekly_login_count = np.random.poisson(4, n_rows)
    monthly_login_count = weekly_login_count * 4 + np.random.poisson(3, n_rows)

    premium_feature_usage_count = np.random.poisson(2, n_rows)
    premium_feature_usage_count = np.where(current_subscription == "Standard", premium_feature_usage_count + np.random.poisson(4, n_rows), premium_feature_usage_count)

    feature_adoption_score = np.clip(
        (premium_feature_usage_count * 6) + (monthly_login_count * 1.5) + np.random.normal(10, 8, n_rows),
        0,
        100
    )

    telemetry_event_count_30d = np.random.poisson(connected_device_count * 40)
    device_error_count_30d = np.random.poisson(np.maximum(1, (100 - device_health_score) / 15))

    data_tier_ceiling_hits_6m = np.random.poisson(
        np.clip(avg_monthly_data_usage_gb / 60, 0.1, 6)
    )

    marketing_action_segment = np.random.choice(
        ["Nurture", "Discount Offer", "Premium Trial", "Sales Outreach", "Reactivation"],
        size=n_rows,
        p=[0.30, 0.22, 0.25, 0.13, 0.10]
    )

    campaigns_received_30d = np.random.poisson(3, n_rows)
    email_open_rate = np.clip(np.random.beta(2, 5, n_rows), 0, 1)
    email_click_rate = np.clip(email_open_rate * np.random.beta(2, 8, n_rows), 0, 1)
    push_click_rate = np.clip(np.random.beta(2, 10, n_rows), 0, 1)

    upgrade_page_views_30d = np.random.poisson(1.5, n_rows)
    upgrade_page_views_30d = np.where(
        premium_feature_usage_count > 5,
        upgrade_page_views_30d + np.random.poisson(3, n_rows),
        upgrade_page_views_30d
    )

    pricing_page_views_30d = np.random.poisson(1, n_rows)
    pricing_page_views_30d = np.where(
        upgrade_page_views_30d > 3,
        pricing_page_views_30d + np.random.poisson(2, n_rows),
        pricing_page_views_30d
    )

    webinar_attendance = np.random.choice([0, 1], size=n_rows, p=[0.85, 0.15])

    last_campaign_response = np.random.choice(
        ["No Response", "Opened", "Clicked", "Converted Interest", "Unsubscribed"],
        size=n_rows,
        p=[0.45, 0.30, 0.17, 0.06, 0.02]
    )

    weather_condition = np.random.choice(
        ["Sunny", "Rainy", "Cloudy", "Stormy", "Hot", "Cold"],
        size=n_rows
    )

    average_temperature = np.clip(np.random.normal(27, 8, n_rows), -5, 45)
    economic_index = np.clip(np.random.normal(65, 12, n_rows), 20, 100)
    holiday_season = np.random.choice([0, 1], size=n_rows, p=[0.82, 0.18])
    internet_quality_index = np.clip(np.random.normal(74, 15, n_rows), 20, 100)
    region_growth_index = np.clip(np.random.normal(62, 13, n_rows), 10, 100)

    customer_engagement_score = np.clip(
        monthly_login_count * 2.2
        + email_open_rate * 20
        + email_click_rate * 35
        + upgrade_page_views_30d * 4
        + np.random.normal(5, 7, n_rows),
        0,
        100
    )

    device_usage_score = np.clip(
        avg_daily_usage_minutes * 0.35
        + active_device_count * 3
        + avg_device_uptime_percentage * 0.3
        - device_error_count_30d * 1.2,
        0,
        100
    )

    premium_interest_score = np.clip(
        premium_feature_usage_count * 8
        + upgrade_page_views_30d * 7
        + pricing_page_views_30d * 5
        + webinar_attendance * 15
        + email_click_rate * 30,
        0,
        100
    )

    customer_health_score = np.clip(
        customer_engagement_score * 0.35
        + device_usage_score * 0.35
        + device_health_score * 0.30,
        0,
        100
    )

    raw_score = (
        -3.2
        + 0.035 * customer_engagement_score
        + 0.040 * premium_interest_score
        + 0.018 * device_usage_score
        + 0.20 * data_tier_ceiling_hits_6m
        + 0.15 * upgrade_page_views_30d
        + 0.12 * pricing_page_views_30d
        + 0.45 * webinar_attendance
        + 0.35 * auto_renew_enabled
        + 0.25 * trial_used
        + 0.20 * previous_upgrade_count
        - 0.30 * previous_downgrade_count
        - 0.03 * device_error_count_30d
    )

    raw_score += np.where(current_subscription == "Free", 0.25, 0)
    raw_score += np.where(current_subscription == "Basic", 0.35, 0)
    raw_score += np.where(marketing_action_segment == "Premium Trial", 0.35, 0)
    raw_score += np.where(marketing_action_segment == "Sales Outreach", 0.25, 0)
    raw_score += np.where(last_campaign_response == "Clicked", 0.35, 0)
    raw_score += np.where(last_campaign_response == "Converted Interest", 0.60, 0)
    raw_score += np.random.normal(0, 0.65, n_rows)

    upgrade_probability_prior = sigmoid(raw_score)
    actual_upgrade_occurred = np.random.binomial(1, upgrade_probability_prior)

    df = pd.DataFrame({
        "Account_ID": account_ids,
        "Customer_Tenure_Days": customer_tenure_days,
        "Account_Type": account_type,
        "Company_Size": company_size,
        "Industry": industry,
        "Region": region,
        "Country": country,

        "Current_Subscription": current_subscription,
        "Subscription_Age_Days": subscription_age_days,
        "Trial_Used": trial_used,
        "Trial_Days_Used": trial_days_used,
        "Previous_Upgrade_Count": previous_upgrade_count,
        "Previous_Downgrade_Count": previous_downgrade_count,
        "Auto_Renew_Enabled": auto_renew_enabled,
        "Monthly_Subscription_Fee": np.round(monthly_subscription_fee, 2),

        "Base_Hardware": base_hardware,
        "Connected_Device_Count": connected_device_count,
        "Active_Device_Count": active_device_count,
        "Offline_Device_Count": offline_device_count,
        "Device_Health_Score": np.round(device_health_score, 2),
        "Firmware_Version": firmware_version,
        "Avg_Device_Uptime_Percentage": np.round(avg_device_uptime_percentage, 2),
        "Avg_Battery_Level": np.round(avg_battery_level, 2),

        "Avg_Monthly_Data_Usage_GB": np.round(avg_monthly_data_usage_gb, 2),
        "Avg_Daily_Usage_Minutes": np.round(avg_daily_usage_minutes, 2),
        "Avg_Session_Duration_Minutes": np.round(avg_session_duration_minutes, 2),
        "Weekly_Login_Count": weekly_login_count,
        "Monthly_Login_Count": monthly_login_count,
        "Premium_Feature_Usage_Count": premium_feature_usage_count,
        "Feature_Adoption_Score": np.round(feature_adoption_score, 2),
        "Telemetry_Event_Count_30D": telemetry_event_count_30d,
        "Device_Error_Count_30D": device_error_count_30d,
        "Data_Tier_Ceiling_Hits_6M": data_tier_ceiling_hits_6m,

        "Marketing_Action_Segment": marketing_action_segment,
        "Campaigns_Received_30D": campaigns_received_30d,
        "Email_Open_Rate": np.round(email_open_rate, 4),
        "Email_Click_Rate": np.round(email_click_rate, 4),
        "Push_Click_Rate": np.round(push_click_rate, 4),
        "Upgrade_Page_Views_30D": upgrade_page_views_30d,
        "Pricing_Page_Views_30D": pricing_page_views_30d,
        "Webinar_Attendance": webinar_attendance,
        "Last_Campaign_Response": last_campaign_response,

        "Weather_Condition": weather_condition,
        "Average_Temperature": np.round(average_temperature, 2),
        "Economic_Index": np.round(economic_index, 2),
        "Holiday_Season": holiday_season,
        "Internet_Quality_Index": np.round(internet_quality_index, 2),
        "Region_Growth_Index": np.round(region_growth_index, 2),

        "Customer_Engagement_Score": np.round(customer_engagement_score, 2),
        "Device_Usage_Score": np.round(device_usage_score, 2),
        "Premium_Interest_Score": np.round(premium_interest_score, 2),
        "Upgrade_Probability_Prior": np.round(upgrade_probability_prior, 4),
        "Customer_Health_Score": np.round(customer_health_score, 2),

        "Actual_Upgrade_Occurred": actual_upgrade_occurred
    })

    return df


def save_dataset(df: pd.DataFrame):
    OUTPUT_DIR.mkdir(exist_ok=True)

    full_path = OUTPUT_DIR / "signalup_ai_dataset.csv"
    train_path = OUTPUT_DIR / "signalup_ai_train.csv"
    test_path = OUTPUT_DIR / "signalup_ai_test.csv"
    summary_path = OUTPUT_DIR / "dataset_summary.json"

    df.to_csv(full_path, index=False)

    train_df, test_df = train_test_split(
        df,
        test_size=0.2,
        random_state=RANDOM_SEED,
        stratify=df["Actual_Upgrade_Occurred"]
    )

    train_df.to_csv(train_path, index=False)
    test_df.to_csv(test_path, index=False)

    summary = {
        "total_rows": int(len(df)),
        "total_columns": int(len(df.columns)),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "target_column": "Actual_Upgrade_Occurred",
        "upgrade_rate": float(df["Actual_Upgrade_Occurred"].mean()),
        "columns": list(df.columns)
    }

    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=4)

    print("Synthetic dataset generated successfully.")
    print(f"Full dataset: {full_path}")
    print(f"Train dataset: {train_path}")
    print(f"Test dataset: {test_path}")
    print(f"Summary: {summary_path}")
    print(f"Upgrade rate: {summary['upgrade_rate']:.2%}")


if __name__ == "__main__":
    dataset = generate_dataset(N_ROWS)
    save_dataset(dataset)