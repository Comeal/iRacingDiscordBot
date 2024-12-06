from iracingdataapi.client import irDataClient

import pandas as pd
import re
from config import iracing_pass, iracing_user, get_previous_tuesday

idc = irDataClient(username=iracing_user, password=iracing_pass)
latestWeek = get_previous_tuesday()


# generate df that shows this week's imsa races
def this_week_imsa_races():
    # get all recent events from a set time
    stats = idc.result_search_series(event_types=[1], start_range_begin=latestWeek)

    # flatten all nested dictionaries
    df = pd.json_normalize(stats, sep="_")
    imsa_races = []

    # extract imsa only race sessions
    for _, race in df.iterrows():
        if re.search("IMSA", race["series_name"]) and race["event_type_name"] == "Race":
            imsa_races.append(race)
        else:
            continue

    last_10_ids = imsa_races[-10:]

    df = pd.DataFrame(last_10_ids)
    df.drop(columns=["session_id", "end_time", "license_category_id", "license_category", "num_drivers", "num_cautions",
                     "num_caution_laps", "num_lead_changes", "event_laps_complete", "driver_changes", "winner_group_id",
                     "winner_ai", "official_session", "season_id", "season_year", "season_quarter", "event_type",
                     "series_id", "series_short_name", "race_week_num", "event_strength_of_field", "event_average_lap",
                     "event_best_lap_time", "track_config_name", "track_track_id"], inplace=True)

    # rename columns
    df.rename(
        columns={"subsession_id": "ID", "winner_name": "Winner", "event_type_name": "Event", "series_name": "Series",
                 "track_track_name": "Track", "start_time": "Time"}, inplace=True)

    return df

# Create function to grab all session IDs from this week's races function
def get_all_session_id():
    weekly_races = this_week_imsa_races()
    session_ids = weekly_races["ID"].tolist()

    return session_ids


def race_results():
    session_ids = get_all_session_id()
    race_result = idc.result(subsession_id=session_ids[0], include_licenses=False)

    # find results dict nested within sub dictionaries and append to a new list
    imsa_race_results = []
    imsa_sessions = []
    session_id = race_result.get("subsession_id")

    if "session_results" in race_result:
        session_result = race_result["session_results"]
        for sessions in session_result:
            imsa_sessions.append(sessions)
            if sessions.get("simsession_name") == 'RACE' and "results" in sessions:
                results = sessions["results"]
                for result in results:
                    imsa_race_results.append(result)

    df = pd.json_normalize(imsa_race_results, sep="_")
    df.drop(columns=['cust_id', 'aggregate_champ_points', 'ai', 'average_lap', 'best_lap_num', 'best_lap_time',
                     'best_nlaps_num', 'best_nlaps_time', 'best_qual_lap_at', 'best_qual_lap_num', 'best_qual_lap_time',
                     'car_class_id', 'car_class_short_name', 'car_id', 'champ_points', 'class_interval', 'club_id',
                     'club_name', 'club_points', 'club_shortname', 'country_code', 'division', 'division_name',
                     'drop_race', 'finish_position_in_class', 'friend', 'incidents', 'interval', 'laps_complete',
                     'laps_lead', 'league_agg_points', 'league_points', 'license_change_oval', 'license_change_road',
                     'max_pct_fuel_fill', 'multiplier', 'new_cpi', 'new_license_level', 'new_sub_level', 'new_ttrating',
                     'newi_rating', 'old_cpi', 'old_license_level', 'old_sub_level', 'old_ttrating', 'oldi_rating',
                     'opt_laps_complete', 'position', 'qual_lap_time', 'reason_out', 'reason_out_id',
                     'starting_position', 'starting_position_in_class', 'watched', 'weight_penalty_kg',
                     'helmet_pattern', 'helmet_color1', 'helmet_color2', 'helmet_color3', 'helmet_face_type',
                     'helmet_helmet_type', 'livery_car_id', 'livery_pattern', 'livery_color1', 'livery_color2',
                     'livery_color3', 'livery_number_font', 'livery_number_color1', 'livery_number_color2',
                     'livery_number_color3', 'livery_number_slant', 'livery_sponsor1', 'livery_sponsor2',
                     'livery_car_number', 'livery_wheel_color', 'livery_rim_type', 'suit_pattern', 'suit_color1',
                     'suit_color2', 'suit_color3'], inplace=True)

    # filter out non GTP cars
    df = df.loc[df['car_class_name'] == 'GTP']

    # rename columns
    df.rename(columns={"subsession_id": "ID", "display_name": "Driver", "car_class_name": "Class", "car_name": "Car",
                       "finish_position": "Result"}, inplace=True)

    # add session id to dataframe
    df["ID"] = session_id

    return df


print(race_results())
