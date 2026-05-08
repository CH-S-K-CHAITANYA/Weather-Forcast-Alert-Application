"""
Visualizer - Creates weather charts using Matplotlib
"""

import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime

# Ensure output folder exists
os.makedirs("outputs", exist_ok=True)


def plot_temperature_trend(forecast_df: pd.DataFrame, city: str):
    """
    Plot 5-day temperature trend as a line chart.
    Saves PNG to outputs/ folder.
    """
    if forecast_df.empty:
        print("⚠️ No forecast data to visualize.")
        return

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    # Plot temperature line
    ax.plot(
        forecast_df["datetime"], forecast_df["temp"],
        color="#e94560", linewidth=2.5, marker="o",
        markersize=5, label="Temperature (°C)"
    )

    # Fill under the line
    ax.fill_between(
        forecast_df["datetime"], forecast_df["temp"],
        alpha=0.2, color="#e94560"
    )

    # Plot feels like
    ax.plot(
        forecast_df["datetime"], forecast_df["feels_like"],
        color="#0f3460", linewidth=1.5, linestyle="--",
        label="Feels Like (°C)"
    )

    # Formatting
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d %b\n%I%p"))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=0, color="white")
    plt.yticks(color="white")

    ax.set_title(f"5-Day Temperature Forecast — {city}", color="white", fontsize=14, pad=15)
    ax.set_xlabel("Date & Time", color="#a0a0b0")
    ax.set_ylabel("Temperature (°C)", color="#a0a0b0")
    ax.legend(facecolor="#1a1a2e", labelcolor="white")
    ax.grid(color="#2a2a4a", linestyle="--", alpha=0.5)

    # Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    path = f"outputs/temperature_forecast_{timestamp}.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  📊 Temperature chart saved: {path}")


def plot_humidity_chart(forecast_df: pd.DataFrame, city: str):
    """
    Plot humidity as bar chart over 5 days.
    Saves PNG to outputs/ folder.
    """
    if forecast_df.empty:
        return

    # Take one reading per day for clarity
    daily = forecast_df.set_index("datetime").resample("D")["humidity"].mean().reset_index()

    fig, ax = plt.subplots(figsize=(10, 5))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#16213e")

    colors = ["#e94560" if h > 85 else "#0f9b58" for h in daily["humidity"]]
    bars = ax.bar(daily["datetime"].dt.strftime("%a\n%d %b"), daily["humidity"],
                  color=colors, width=0.5, edgecolor="white", linewidth=0.5)

    # Add value labels on bars
    for bar, val in zip(bars, daily["humidity"]):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1,
                f"{val:.0f}%", ha="center", color="white", fontsize=10)

    # Alert threshold line
    ax.axhline(y=85, color="#ff4444", linestyle="--", linewidth=1.5, label="Alert Threshold (85%)")

    ax.set_title(f"Daily Average Humidity — {city}", color="white", fontsize=14, pad=15)
    ax.set_xlabel("Day", color="#a0a0b0")
    ax.set_ylabel("Humidity (%)", color="#a0a0b0")
    ax.set_ylim(0, 110)
    ax.legend(facecolor="#1a1a2e", labelcolor="white")
    ax.tick_params(colors="white")
    ax.grid(axis="y", color="#2a2a4a", linestyle="--", alpha=0.5)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M")
    path = f"outputs/humidity_chart_{timestamp}.png"
    plt.tight_layout()
    plt.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close()
    print(f"  📊 Humidity chart saved: {path}")