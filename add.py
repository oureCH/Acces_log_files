import os
import json
from datetime import datetime


def analyze_summary_data(summary_folder_path, save_folder_path=None):
    url_data = {}
    for filename in os.listdir(summary_folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(summary_folder_path, filename)
            date_str = filename.split('-')[-1].split('.')[0]
            date = datetime.strptime(date_str, '%Y%m%d')
            with open(file_path) as f:
                data = json.load(f)
                for url, status_counts in data.items():
                    if url not in url_data:
                        url_data[url] = {}

                    for status, count in status_counts.items():
                        if status not in url_data[url]:
                            url_data[url][status] = {'calls': 0, 'dates': set()}

                        url_data[url][status]['calls'] += count
                        url_data[url][status]['dates'].add(date)

    summary_data = []
    for url, status_counts in url_data.items():
        for status, count_and_dates in status_counts.items():
            summary_data.append({
                'endpoints': url,
                'status': status,
                'calls': count_and_dates['calls'],
                'dates': sorted(count_and_dates['dates'])
            })

    if save_folder_path:
        output_filename = os.path.join(save_folder_path, "analyzed_data.json")
        with open(output_filename, 'w') as f:
            json.dump(summary_data, f, default=str, indent=4)

    return summary_data


def display_summary_table(summary_data):
    max_url_length = max(len(data['endpoints']) for data in summary_data)
    print(f"{'Endpoints':<{max_url_length}} {'Status':<10} {'Calls':<5} {'Dates':<20}")
    for data in sorted(summary_data, key=lambda x: (x['endpoints'], x['status'], -x['calls'], x['dates'])):
        date_str = ', '.join(d.strftime('%Y-%m-%d') for d in data['dates'])
        print(f"{data['endpoints']:<{max_url_length}} {data['status']:<10} {data['calls']:<5} {date_str:<20}")


def main():
    summary_folder_path = "summary/"
    save_folder_path = "analysis/"
    summary_data = analyze_summary_data(summary_folder_path, save_folder_path)

    print("Summary data:")
    display_summary_table(summary_data)


if __name__ == "__main__":
    main()
