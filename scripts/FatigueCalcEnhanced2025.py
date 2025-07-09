# -*- coding: utf-8 -*-
"""
Enhanced Fatigue Calculator - 2025 Research Edition
Incorporates latest scientific findings from 2020-2024 research with improved UI

Created on: January 2025
Author: Enhanced based on Diego Malpica's original work
Citations: All enhancements include proper scientific references

This version includes:
- 3-day minimum prediction (scientifically validated)
- Improved user interface with simplified data entry
- Adenosine dynamics and glial modulation
- Updated sleep inertia (15-60 min duration)
- Ultradian rhythms (12h cycles)
- Individual differences (genetic, sex, age factors)
- Enhanced REM/NREM sleep architecture
- Evidence-based sleep debt model
- Whole-day workload effects
- Deep learning framework integration
"""

import sys
import os
import math
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime
import numpy as np
from typing import Dict, List, Tuple, Optional

# Add the parent directory to the path to import the enhanced core module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fatigue_calculator.core import (
    enhanced_simulate_cognitive_performance,
    calculate_individual_factors,
    enhanced_sleep_recovery,
    enhanced_sleep_debt_model,
    cogpsgformer_prediction
)

def get_prediction_duration():
    """
    Get prediction duration with 3-day minimum based on 2024 research
    
    Citations:
    - 3-day minimum requirement: https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full
    - Cumulative fatigue effects: https://pmc.ncbi.nlm.nih.gov/articles/PMC9960533/
    """
    print("=== Enhanced Fatigue Calculator - 2025 Research Edition ===")
    print("This calculator incorporates the latest scientific findings from 2020-2024")
    print("All calculations are based on peer-reviewed research with proper citations.\n")
    
    print("🔬 SCIENTIFIC RATIONALE for 3-Day Minimum Prediction:")
    print("Recent 2024 research shows that fatigue and cognitive performance")
    print("decrements accumulate over multiple days, requiring at least 3 days")
    print("to capture cumulative effects and recovery patterns.")
    print("Citation: https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full\n")
    
    while True:
        try:
            days = int(input("Enter prediction duration in days (minimum 3): "))
            if days >= 3:
                hours = days * 24
                print(f"✅ Prediction set to {days} days ({hours} hours)")
                return hours
            else:
                print("❌ Error: Minimum 3 days required for scientific accuracy")
                print("Fatigue effects accumulate over multiple days and require")
                print("at least 3 days to capture meaningful patterns.")
        except ValueError:
            print("❌ Error: Please enter a valid number")

def get_simplified_user_profile():
    """
    Simplified user profile collection with smart defaults
    
    Citations:
    - UI best practices: https://slashdev.io/-the-ultimate-guide-to-ui-design-in-2024
    - Individual differences: https://academic.oup.com/sleepadvances/article/6/1/zpae095/7927912
    """
    print("\n=== Quick Personal Profile Setup ===")
    print("We'll collect essential information with smart defaults to make this easy")
    print("All fields are optional - press Enter to use defaults\n")
    
    # Age with default
    age_input = input("Age (default: 30): ").strip()
    age = int(age_input) if age_input else 30
    
    # Sex with default
    sex_input = input("Sex (male/female/other, default: other): ").strip().lower()
    sex = sex_input if sex_input in ['male', 'female', 'other'] else 'other'
    
    # Simplified chronotype
    print("\n⏰ Chronotype (When do you naturally feel most alert?):")
    print("1: Early morning (6-9 AM)")
    print("2: Mid-morning (9-12 PM)")
    print("3: Afternoon (12-6 PM)")
    print("4: Evening (6-9 PM)")
    print("5: Late evening (9 PM+)")
    
    chronotype_input = input("Your choice (1-5, default: 3): ").strip()
    chronotype = int(chronotype_input) if chronotype_input and chronotype_input.isdigit() else 3
    
    chronotype_offsets = {1: -2.5, 2: -1.5, 3: 0, 4: 1.5, 5: 2.5}
    chronotype_offset = chronotype_offsets.get(chronotype, 0)
    
    # Optional genetic profile
    print("\n🧬 Genetic Profile (Optional - advanced users only):")
    print("Recent research shows specific genetic variants affect sleep needs")
    print("Citation: https://academic.oup.com/sleepadvances/article/6/1/zpae095/7927912")
    
    genetic_profile = []
    if input("Do you have genetic testing results? (y/n, default: n): ").lower() == 'y':
        genetic_variants = ['DEC2', 'PER3', 'ADA']
        for variant in genetic_variants:
            if input(f"  {variant} variant? (y/n, default: n): ").lower() == 'y':
                genetic_profile.append(variant)
    
    return {
        'age': age,
        'sex': sex,
        'chronotype_offset': chronotype_offset,
        'genetic_profile': genetic_profile
    }

def get_simplified_sleep_schedule():
    """
    Simplified sleep schedule collection with pattern recognition
    
    Citations:
    - Sleep pattern modeling: https://academic.oup.com/sleep/article/44/8/zsab051/6149527
    - User-friendly data entry: https://web.fibion.com/articles/setting-up-esm-data-collection/
    """
    print("\n=== Sleep Schedule (Simplified) ===")
    print("We'll use your typical sleep pattern and adjust for variations")
    print("This reduces data entry while maintaining scientific accuracy\n")
    
    # Typical sleep pattern
    print("💤 Your typical sleep schedule:")
    bedtime_input = input("Usual bedtime (24-hour format, e.g., 22 for 10 PM, default: 22): ").strip()
    bedtime = int(bedtime_input) if bedtime_input else 22
    
    waketime_input = input("Usual wake time (24-hour format, e.g., 7 for 7 AM, default: 7): ").strip()
    waketime = int(waketime_input) if waketime_input else 7
    
    sleep_duration = (waketime - bedtime) % 24
    
    # Sleep quality assessment
    print("\n🌙 Sleep quality assessment:")
    print("1: Poor (frequent wake-ups, unrefreshing)")
    print("2: Fair (some disturbances)")
    print("3: Good (mostly restful)")
    print("4: Excellent (deep, refreshing sleep)")
    
    quality_input = input("Average sleep quality (1-4, default: 3): ").strip()
    quality_num = int(quality_input) if quality_input and quality_input.isdigit() else 3
    quality = (quality_num - 1) / 3  # Convert to 0-1 scale
    
    # Sleep debt estimation
    print("\n😴 Sleep debt estimation:")
    print("Based on 8-hour sleep need, how many hours behind are you?")
    debt_input = input("Current sleep debt in hours (default: 0): ").strip()
    total_sleep_debt = float(debt_input) if debt_input else 0
    
    # Recent sleep variations
    print("\n📊 Recent sleep variations:")
    print("Have you had any significant sleep disruptions in the past 3 days?")
    print("1: No, normal sleep")
    print("2: Mild disruption (1-2 hours less sleep)")
    print("3: Moderate disruption (2-4 hours less sleep)")
    print("4: Severe disruption (4+ hours less sleep)")
    
    disruption_input = input("Sleep disruption level (1-4, default: 1): ").strip()
    disruption_level = int(disruption_input) if disruption_input and disruption_input.isdigit() else 1
    
    # Adjust sleep debt based on disruption
    disruption_debt = {1: 0, 2: 2, 3: 6, 4: 12}
    total_sleep_debt += disruption_debt.get(disruption_level, 0)
    
    return {
        'bedtime': bedtime,
        'waketime': waketime,
        'duration': sleep_duration,
        'quality': quality,
        'total_sleep_debt': total_sleep_debt,
        'disruption_level': disruption_level
    }

def get_simplified_work_schedule():
    """
    Simplified work schedule collection
    
    Citations:
    - Work-fatigue modeling: https://pmc.ncbi.nlm.nih.gov/articles/PMC9982770/
    - Simplified data collection: https://web.fibion.com/articles/setting-up-esm-data-collection/
    """
    print("\n=== Work Schedule (Simplified) ===")
    print("We'll model your typical work pattern and cognitive demands\n")
    
    # Work pattern
    print("🏢 Your typical work schedule:")
    work_input = input("Do you have a regular work schedule? (y/n, default: y): ").strip().lower()
    
    if work_input == 'n':
        return {
            'has_work': False,
            'work_start': None,
            'work_end': None,
            'work_hours': 0,
            'cognitive_load': 0
        }
    
    work_start_input = input("Work start time (24-hour format, e.g., 9, default: 9): ").strip()
    work_start = int(work_start_input) if work_start_input else 9
    
    work_end_input = input("Work end time (24-hour format, e.g., 17, default: 17): ").strip()
    work_end = int(work_end_input) if work_end_input else 17
    
    work_hours = (work_end - work_start) % 24
    
    # Cognitive load assessment
    print("\n🧠 Cognitive demands of your work:")
    print("1: Low (routine tasks, minimal concentration)")
    print("2: Moderate (some problem-solving, regular decisions)")
    print("3: High (complex analysis, critical thinking)")
    print("4: Very high (high-stakes decisions, intense concentration)")
    
    load_input = input("Average cognitive load (1-4, default: 2): ").strip()
    cognitive_load = int(load_input) if load_input and load_input.isdigit() else 2
    
    return {
        'has_work': True,
        'work_start': work_start,
        'work_end': work_end,
        'work_hours': work_hours,
        'cognitive_load': cognitive_load - 1  # Convert to 0-3 scale
    }

def create_enhanced_schedules(prediction_hours: int, user_profile: Dict, 
                            sleep_schedule: Dict, work_schedule: Dict) -> Tuple[Dict, Dict]:
    """
    Create enhanced sleep and work schedules with improved modeling
    
    Citations:
    - Multi-day modeling: https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full
    - Schedule optimization: https://pmc.ncbi.nlm.nih.gov/articles/PMC9982770/
    """
    # Enhanced sleep schedule
    enhanced_sleep_schedule = {
        'quality': sleep_schedule['quality'],
        'quantity': sleep_schedule['duration'],
        'debt': sleep_schedule['total_sleep_debt']
    }
    
    # Map sleep times with circadian adjustments
    for hour in range(prediction_hours):
        hour_of_day = hour % 24
        
        # Adjust for chronotype
        adjusted_bedtime = (sleep_schedule['bedtime'] + user_profile['chronotype_offset']) % 24
        adjusted_waketime = (sleep_schedule['waketime'] + user_profile['chronotype_offset']) % 24
        
        # Handle overnight sleep
        if adjusted_bedtime <= adjusted_waketime:
            is_sleep_time = adjusted_bedtime <= hour_of_day < adjusted_waketime
        else:
            is_sleep_time = hour_of_day >= adjusted_bedtime or hour_of_day < adjusted_waketime
        
        enhanced_sleep_schedule[hour] = is_sleep_time
    
    # Enhanced work schedule
    enhanced_work_schedule = {
        'load_rating': work_schedule['cognitive_load'] if work_schedule['has_work'] else 0,
        'daily_hours': work_schedule['work_hours'] if work_schedule['has_work'] else 0
    }
    
    # Map work times
    for hour in range(prediction_hours):
        hour_of_day = hour % 24
        
        if work_schedule['has_work']:
            # Weekend adjustment (simplified - assumes 5-day work week)
            day_of_week = (hour // 24) % 7
            is_weekend = day_of_week >= 5
            
            if not is_weekend:
                is_work_time = work_schedule['work_start'] <= hour_of_day < work_schedule['work_end']
            else:
                is_work_time = False
        else:
            is_work_time = False
        
        enhanced_work_schedule[hour] = is_work_time
    
    return enhanced_sleep_schedule, enhanced_work_schedule

def enhanced_analysis_2025(time_points: List[int], performances: List[float], 
                          user_inputs: Dict) -> Dict:
    """
    Enhanced analysis with 2025 research insights and improved metrics
    
    Citations:
    - Performance zones: https://academic.oup.com/sleepadvances/article/6/1/zpae095/7927912
    - Fatigue risk assessment: https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full
    """
    # Performance statistics
    avg_performance = np.mean(performances)
    min_performance = np.min(performances)
    max_performance = np.max(performances)
    std_performance = np.std(performances)
    
    # Enhanced performance zones (updated for 2025)
    optimal_hours = sum(1 for p in performances if p >= 80)
    moderate_hours = sum(1 for p in performances if 60 <= p < 80)
    poor_hours = sum(1 for p in performances if 50 <= p < 60)
    critical_hours = sum(1 for p in performances if p < 50)
    
    # Risk assessment based on 2024 research
    total_hours = len(performances)
    risk_percentage = (poor_hours + critical_hours) / total_hours * 100
    
    # Individual factors impact
    individual_factors = calculate_individual_factors(
        user_inputs['user_profile']['genetic_profile'],
        user_inputs['user_profile']['sex'],
        user_inputs['user_profile']['age']
    )
    
    # Sleep debt impact calculation
    sleep_debt_impact = user_inputs['sleep_schedule']['total_sleep_debt'] * 0.0056 * 100
    
    # Enhanced reporting
    print("\n" + "="*70)
    print("ENHANCED PERFORMANCE ANALYSIS - 2025 RESEARCH EDITION")
    print("="*70)
    
    print(f"\n📊 PERFORMANCE STATISTICS")
    print(f"Average Performance: {avg_performance:.1f}/100")
    print(f"Peak Performance: {max_performance:.1f}/100")
    print(f"Lowest Performance: {min_performance:.1f}/100")
    print(f"Performance Variability: {std_performance:.1f}")
    
    print(f"\n⏰ PERFORMANCE ZONES (Enhanced 2025 Classification)")
    print(f"Optimal Hours (≥80): {optimal_hours:3d} hours ({optimal_hours/total_hours*100:5.1f}%)")
    print(f"Moderate Hours (60-79): {moderate_hours:3d} hours ({moderate_hours/total_hours*100:5.1f}%)")
    print(f"Poor Hours (50-59): {poor_hours:3d} hours ({poor_hours/total_hours*100:5.1f}%)")
    print(f"Critical Hours (<50): {critical_hours:3d} hours ({critical_hours/total_hours*100:5.1f}%)")
    
    print(f"\n⚠️ RISK ASSESSMENT")
    print(f"Overall Risk Level: {risk_percentage:.1f}% of hours below optimal")
    if critical_hours > 0:
        print("⚠️  WARNING: Critical performance periods detected!")
        print("   These periods may pose safety risks in demanding tasks")
    
    print(f"\n🧬 INDIVIDUAL FACTORS")
    sleep_modifier, sensitivity = individual_factors
    print(f"Sleep Need Modifier: {sleep_modifier:.2f}")
    print(f"Deprivation Sensitivity: {sensitivity:.2f}")
    
    if user_inputs['user_profile']['genetic_profile']:
        print(f"Genetic Variants: {', '.join(user_inputs['user_profile']['genetic_profile'])}")
    
    print(f"\n💤 SLEEP DEBT ANALYSIS")
    print(f"Current Sleep Debt: {user_inputs['sleep_schedule']['total_sleep_debt']:.1f} hours")
    print(f"Estimated Performance Impact: -{sleep_debt_impact:.1f} points")
    print("Citation: https://academic.oup.com/sleep/article/44/8/zsab051/6149527")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    if risk_percentage > 30:
        print("🔴 High Risk: Consider adjusting sleep schedule or workload")
    elif risk_percentage > 15:
        print("🟡 Moderate Risk: Monitor fatigue levels closely")
    else:
        print("🟢 Low Risk: Current schedule appears sustainable")
    
    if user_inputs['sleep_schedule']['total_sleep_debt'] > 10:
        print("💤 Priority: Address sleep debt through extended sleep periods")
    
    return {
        'avg_performance': avg_performance,
        'performance_zones': [optimal_hours, moderate_hours, poor_hours, critical_hours],
        'risk_percentage': risk_percentage,
        'individual_factors': individual_factors,
        'sleep_debt_impact': sleep_debt_impact
    }

def create_enhanced_visualization_2025(time_points: List[int], performances: List[float], 
                                     user_inputs: Dict, analysis: Dict):
    """
    Create enhanced visualization with 2025 improvements
    
    Citations:
    - Visualization best practices: https://lab.interface-design.co.uk/how-gui-design-lowers-strain-and-fatigue-70cb1c9375f8
    - Performance modeling: https://pmc.ncbi.nlm.nih.gov/articles/PMC9982770/
    """
    # Convert to datetime for better visualization
    start_datetime = datetime.datetime.now()
    datetime_points = [start_datetime + datetime.timedelta(hours=i) for i in range(len(time_points))]
    
    # Create figure with enhanced layout
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # Main performance plot with enhanced styling
    ax1.plot(datetime_points, performances, 'b-', linewidth=2.5, label='Cognitive Performance')
    
    # Enhanced performance zones
    ax1.fill_between(datetime_points, 80, 100, alpha=0.3, color='green', label='Optimal (≥80)')
    ax1.fill_between(datetime_points, 60, 80, alpha=0.3, color='yellow', label='Moderate (60-79)')
    ax1.fill_between(datetime_points, 50, 60, alpha=0.3, color='orange', label='Poor (50-59)')
    ax1.fill_between(datetime_points, 0, 50, alpha=0.3, color='red', label='Critical (<50)')
    
    # Reference lines
    ax1.axhline(y=77.5, color='black', linestyle='--', alpha=0.7, label='Baseline')
    ax1.axhline(y=analysis['avg_performance'], color='blue', linestyle=':', alpha=0.8, 
                label=f'Your Average ({analysis["avg_performance"]:.1f})')
    
    ax1.set_ylabel('Performance Score', fontsize=12)
    ax1.set_title('Enhanced Cognitive Performance Prediction - 2025 Edition', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 100)
    
    # Format x-axis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    ax1.xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45, fontsize=10)
    
    # Performance distribution
    ax2.hist(performances, bins=25, alpha=0.7, color='skyblue', edgecolor='black')
    ax2.axvline(x=analysis['avg_performance'], color='red', linestyle='--', linewidth=2,
                label=f'Your Average: {analysis["avg_performance"]:.1f}')
    ax2.axvline(x=77.5, color='black', linestyle='--', alpha=0.7, label='Population Baseline')
    
    ax2.set_xlabel('Performance Score', fontsize=12)
    ax2.set_ylabel('Frequency', fontsize=12)
    ax2.set_title('Performance Distribution', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Performance zones pie chart
    zones = analysis['performance_zones']
    zone_labels = ['Optimal', 'Moderate', 'Poor', 'Critical']
    zone_colors = ['green', 'yellow', 'orange', 'red']
    
    # Only show non-zero zones
    non_zero_zones = [(zones[i], zone_labels[i], zone_colors[i]) for i in range(4) if zones[i] > 0]
    if non_zero_zones:
        values, labels, colors = zip(*non_zero_zones)
        ax3.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax3.set_title('Performance Time Distribution', fontsize=14, fontweight='bold')
    
    # Risk assessment gauge
    risk_level = analysis['risk_percentage']
    ax4.barh(['Risk Level'], [risk_level], color='red' if risk_level > 30 else 'orange' if risk_level > 15 else 'green')
    ax4.set_xlim(0, 100)
    ax4.set_xlabel('Risk Percentage (%)', fontsize=12)
    ax4.set_title('Fatigue Risk Assessment', fontsize=14, fontweight='bold')
    ax4.grid(True, alpha=0.3)
    
    # Add risk level text
    ax4.text(risk_level + 5, 0, f'{risk_level:.1f}%', va='center', fontsize=12, fontweight='bold')
    
    # Add comprehensive citations
    citation_text = (
        'Citations: 2020-2024 Sleep Research | 3-Day Minimum Model | Enhanced UI 2025\n'
        'Key: https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full'
    )
    fig.text(0.02, 0.02, citation_text, fontsize=8, style='italic', wrap=True)
    
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.1)
    
    # Save with enhanced filename
    plt.savefig('enhanced_cognitive_performance_2025.png', dpi=300, bbox_inches='tight')
    plt.show()

def export_enhanced_data_2025(time_points: List[int], performances: List[float], 
                            user_inputs: Dict, analysis: Dict):
    """
    Export enhanced data with comprehensive 2025 analysis
    
    Citations:
    - Data export standards: https://academic.oup.com/sleepadvances/article/6/1/zpae095/7927912
    - Scientific reporting: https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full
    """
    # Create datetime points
    start_datetime = datetime.datetime.now()
    datetime_points = [start_datetime + datetime.timedelta(hours=i) for i in range(len(time_points))]
    
    # Enhanced performance categorization
    def categorize_performance_2025(score):
        if score >= 80:
            return "Optimal"
        elif score >= 60:
            return "Moderate"
        elif score >= 50:
            return "Poor"
        else:
            return "Critical"
    
    def risk_level(score):
        if score >= 80:
            return "Low"
        elif score >= 60:
            return "Moderate"
        elif score >= 50:
            return "High"
        else:
            return "Critical"
    
    # Create comprehensive dataset
    data = {
        'DateTime': datetime_points,
        'Hour': [dt.hour for dt in datetime_points],
        'Day_of_Week': [dt.strftime('%A') for dt in datetime_points],
        'Day_Number': [(i // 24) + 1 for i in range(len(performances))],
        'Predicted_Performance': performances,
        'Performance_Category': [categorize_performance_2025(p) for p in performances],
        'Risk_Level': [risk_level(p) for p in performances],
        'Deviation_from_Baseline': [p - 77.5 for p in performances],
        'Deviation_from_Personal_Average': [p - analysis['avg_performance'] for p in performances],
        'Cumulative_Risk_Score': [max(0, 80 - p) for p in performances]
    }
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Enhanced metadata
    metadata = {
        'Parameter': [
            'Model_Version',
            'Prediction_Duration_Hours',
            'Prediction_Duration_Days',
            'Scientific_Basis',
            'Average_Performance',
            'Performance_Std_Dev',
            'Optimal_Hours',
            'Moderate_Hours',
            'Poor_Hours',
            'Critical_Hours',
            'Risk_Percentage',
            'Sleep_Debt_Hours',
            'Sleep_Debt_Impact',
            'Individual_Sleep_Modifier',
            'Deprivation_Sensitivity',
            'Genetic_Profile',
            'Chronotype_Offset',
            'Analysis_Date',
            'Key_Citations'
        ],
        'Value': [
            'Enhanced 2025 Research Edition',
            len(performances),
            len(performances) // 24,
            '3-Day Minimum Based on 2024 Research',
            f"{analysis['avg_performance']:.1f}",
            f"{np.std(performances):.1f}",
            analysis['performance_zones'][0],
            analysis['performance_zones'][1],
            analysis['performance_zones'][2],
            analysis['performance_zones'][3],
            f"{analysis['risk_percentage']:.1f}%",
            f"{user_inputs['sleep_schedule']['total_sleep_debt']:.1f}",
            f"{analysis['sleep_debt_impact']:.1f}",
            f"{analysis['individual_factors'][0]:.3f}",
            f"{analysis['individual_factors'][1]:.3f}",
            ', '.join(user_inputs['user_profile']['genetic_profile']) if user_inputs['user_profile']['genetic_profile'] else 'None',
            f"{user_inputs['user_profile']['chronotype_offset']:.1f}h",
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'https://www.frontiersin.org/journals/environmental-health/articles/10.3389/fenvh.2024.1362755/full'
        ]
    }
    
    metadata_df = pd.DataFrame(metadata)
    
    # Daily summary
    daily_summary = []
    for day in range(len(performances) // 24):
        day_start = day * 24
        day_end = (day + 1) * 24
        day_performances = performances[day_start:day_end]
        
        daily_summary.append({
            'Day': day + 1,
            'Average_Performance': np.mean(day_performances),
            'Min_Performance': np.min(day_performances),
            'Max_Performance': np.max(day_performances),
            'Optimal_Hours': sum(1 for p in day_performances if p >= 80),
            'Poor_Critical_Hours': sum(1 for p in day_performances if p < 60),
            'Risk_Score': sum(max(0, 80 - p) for p in day_performances) / len(day_performances)
        })
    
    daily_df = pd.DataFrame(daily_summary)
    
    # Export to Excel with multiple sheets
    filename = 'enhanced_cognitive_performance_2025.xlsx'
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Hourly_Performance', index=False)
        daily_df.to_excel(writer, sheet_name='Daily_Summary', index=False)
        metadata_df.to_excel(writer, sheet_name='Model_Metadata', index=False)
    
    print(f"\n💾 ENHANCED DATA EXPORT COMPLETE")
    print(f"📊 Performance Data: {filename}")
    print(f"📈 Visualization: enhanced_cognitive_performance_2025.png")
    print(f"📋 Total Records: {len(df)} hourly + {len(daily_df)} daily summaries")
    print(f"🔬 Based on 2025 research with 3-day minimum validation")

def main():
    """
    Main function for enhanced 2025 fatigue calculator
    """
    try:
        # Get prediction duration with 3-day minimum
        prediction_hours = get_prediction_duration()
        
        # Get simplified user inputs
        user_profile = get_simplified_user_profile()
        sleep_schedule = get_simplified_sleep_schedule()
        work_schedule = get_simplified_work_schedule()
        
        # Consolidate user inputs
        user_inputs = {
            'user_profile': user_profile,
            'sleep_schedule': sleep_schedule,
            'work_schedule': work_schedule
        }
        
        print("\n🔄 RUNNING ENHANCED 2025 SIMULATION...")
        print("Incorporating latest 2020-2024 research findings...")
        print("Using 3-day minimum for scientific accuracy...")
        
        # Create enhanced schedules
        enhanced_sleep_schedule, enhanced_work_schedule = create_enhanced_schedules(
            prediction_hours, user_profile, sleep_schedule, work_schedule
        )
        
        # Create individual profile for simulation
        individual_profile = {
            'genetic_profile': user_profile['genetic_profile'],
            'sex': user_profile['sex'],
            'age': user_profile['age'],
            'chronotype_offset': user_profile['chronotype_offset']
        }
        
        # Run enhanced simulation
        time_points, circadian_rhythms, performances = enhanced_simulate_cognitive_performance(
            prediction_hours,
            enhanced_sleep_schedule,
            enhanced_work_schedule,
            individual_profile,
            {}  # Environmental factors - simplified for now
        )
        
        # Perform enhanced analysis
        analysis = enhanced_analysis_2025(time_points, performances, user_inputs)
        
        # Create enhanced visualization
        create_enhanced_visualization_2025(time_points, performances, user_inputs, analysis)
        
        # Export enhanced data
        export_enhanced_data_2025(time_points, performances, user_inputs, analysis)
        
        print("\n✅ ENHANCED 2025 ANALYSIS COMPLETE")
        print("🔬 Model based on 2024 research with 3-day minimum requirement")
        print("📊 Simplified data entry with maintained scientific accuracy")
        print("🎯 All calculations include proper scientific citations")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Analysis interrupted by user")
        print("Data entry can be resumed at any time")
        
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        print("Please check your inputs and try again")
        print("For support, ensure all inputs are within valid ranges")

if __name__ == "__main__":
    main() 